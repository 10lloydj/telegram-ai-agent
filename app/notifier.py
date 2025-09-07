import asyncio
from telethon.errors import FloodWaitError
from .schemas import Verdict

async def send_dm(client, to_username: str, v: Verdict,
                  chat_name: str, topic: str | None, link: str | None, snippet: str):
    lines = [
        f"🔔 Role detected (confidence {v.confidence:.2f})",
        f"👥 Chat: {chat_name}",
    ]
    if topic: lines.append(f"🧵 Topic: {topic}")
    if v.job:
        role = v.job.role or "Unknown role"
        ic = "Founding" if v.job.is_founding else (v.job.seniority or "IC")
        lines.append(f"🎯 {role} ({ic})")
        if v.job.company: lines.append(f"🏢 {v.job.company}")
        loc = v.job.location or ""
        if v.job.remote: loc = (loc + " (remote)").strip()
        if loc: lines.append(f"📍 {loc}")
        if v.job.stack: lines.append(f"🧰 {', '.join(v.job.stack[:8])}")
    if v.contact and (v.contact.method or v.contact.value):
        lines.append(f"📫 {v.contact.method or ''} {v.contact.value or ''}".strip())
    if link: lines.append(f"🔗 {link}")
    lines.append("—")
    lines.append((snippet or "")[:400])

    text = "\n".join(lines)
    try:
        await client.send_message(to_username or "me", text, link_preview=False)
    except FloodWaitError as e:
        await asyncio.sleep(e.seconds)
        await client.send_message(to_username or "me", text, link_preview=False)
