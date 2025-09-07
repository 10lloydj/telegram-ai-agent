# verify_chat_id.py
import os, asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
import dotenv

dotenv.load_dotenv()

API_ID    = int(os.environ["API_ID"])
API_HASH  = os.environ["API_HASH"]
SESSION   = os.getenv("TELEGRAM_SESSION")  # if you're using a session string

client = TelegramClient(StringSession(SESSION) if SESSION else "me", API_ID, API_HASH)

RAW = 1934547608  # <-- the number you have

async def main():
    # Try the raw positive number
    try:
        ent = await client.get_entity(RAW)
        print("RAW entity:", ent.id, type(ent).__name__, getattr(ent, "title", None))
    except Exception as e:
        print("RAW failed:", e)

    # Try with -100 prefix (typical for supergroups/channels)
    try:
        ent = await client.get_entity(-100 * 10**9 + RAW if RAW < 10**12 else -RAW)  # safe prefixing
        # simpler if you know it's a t.me/c inner id: just do -100{RAW}:
        # ent = await client.get_entity(int(f"-100{RAW}"))
        print("NEG entity:", ent.id, type(ent).__name__, getattr(ent, "title", None))
    except Exception as e:
        print("NEG failed:", e)

with client:
    client.loop.run_until_complete(main())
