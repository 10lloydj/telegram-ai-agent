# sniff_chat_id.py
import os, asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession

load_dotenv()
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.getenv("TELEGRAM_SESSION")  # optional session string

client = TelegramClient(StringSession(SESSION) if SESSION else "me", API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(ev):
    chat = await ev.get_chat()
    if getattr(chat, "title", None):  # groups/supergroups/channels
        print("CHAT TITLE:", chat.title)
        print("CHAT ID:", chat.id)   # <- use this value
        # For supergroups/channels you'll see: -100xxxxxxxxxx
        # For basic groups you'll see a negative int (no -100 prefix)
        # Once you see your target, Ctrl+C to stop.

async def main():
    print("Listening... send a message in the target group.")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())