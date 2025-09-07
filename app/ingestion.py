import dotenv
import os, datetime as dt
import pytz
from telethon import events
from telethon.utils import get_display_name
from telethon.tl.functions.channels import GetForumTopicsRequest
from .llm import classify_text
from .models import TGMessage, Alert

dotenv.load_dotenv()

_LONDON = pytz.timezone("Europe/London")
_topic_cache: dict[tuple[int, int], str] = {}

def _in_quiet_hours(start: int, end: int) -> bool:
    now_h = dt.datetime.now(_LONDON).hour
    return (start <= now_h < end) if start <= end else (now_h >= start or now_h < end)

async def _topic_title(client, chat, topic_id: int | None) -> str | None:
    if not topic_id: return None
    key = (chat.id, topic_id)
    if key in _topic_cache: return _topic_cache[key]
    try:
        res = await client(GetForumTopicsRequest(channel=chat, offset_date=None, offset_id=0, offset_topic=0, limit=100))
        for t in res.topics:
            if getattr(t, "id", None) == topic_id:
                _topic_cache[key] = t.title
                return t.title
    except Exception:
        pass
    return None

def attach_listeners(client, Session, targets: list[int] | None = None):
    target_ids = targets or [int(os.environ["TARGET_CHAT_ID"])]
    min_conf = float(os.getenv("MIN_CONFIDENCE", "0.60"))
    self_user = os.getenv("SELF_USERNAME", "me")
    q_start = int(os.getenv("QUIET_HOURS_START", "22"))
    q_end = int(os.getenv("QUIET_HOURS_END", "8"))

    @client.on(events.NewMessage(chats=target_ids))
    async def _handler(ev: events.NewMessage.Event):
        msg = ev.message
        text = (msg.message or msg.raw_text or getattr(msg, "caption", "") or "").strip()
        if not text:
            return

        chat = await ev.get_chat()
        sender = await ev.get_sender()
        topic_id = getattr(msg, "reply_to_top_id", None)
        topic = await _topic_title(client, chat, topic_id) if getattr(chat, "forum", False) else None

        # Build message link manually (get_message_link was removed from newer Telethon)
        try:
            if hasattr(chat, 'username') and chat.username:
                link = f"https://t.me/{chat.username}/{msg.id}"
            else:
                # For private groups, use the chat ID format
                chat_id = str(chat.id).replace('-100', '')
                link = f"https://t.me/c/{chat_id}/{msg.id}"
        except Exception:
            link = None

        # LLM verdict
        verdict = await classify_text(text)

        # Upsert and optionally alert
        async with Session() as s:
            await s.merge(TGMessage(
                chat_id=ev.chat_id, message_id=msg.id, sender_id=getattr(sender, "id", None),
                topic_id=topic_id, topic_title=topic, posted_at=msg.date,
                text=text, link=link,
                is_job_post=verdict.is_job_post, is_relevant=verdict.is_relevant,
                confidence=verdict.confidence, verdict=verdict.model_dump()
            ))
            await s.commit()

            should_alert = verdict.is_relevant and verdict.confidence >= min_conf and not _in_quiet_hours(q_start, q_end)
            if should_alert:
                # DM first
                from .notifier import send_dm
                await send_dm(
                    client, self_user, verdict,
                    getattr(chat, "title", get_display_name(chat)),
                    topic, link, text
                )
                # Record alert (idempotent via UNIQUE in your schema)
                try:
                    await s.merge(Alert(
                        chat_id=ev.chat_id, message_id=msg.id,
                        delivered_to=self_user, method="telegram_dm",
                        confidence=verdict.confidence, reasons=verdict.reasons
                    ))
                    await s.commit()
                except Exception:
                    await s.rollback()
