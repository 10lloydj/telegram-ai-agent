# dump_dialogs.py
import os, asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Channel, Chat

import dotenv

dotenv.load_dotenv()

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION = os.getenv("TELEGRAM_SESSION")

client = TelegramClient(StringSession(SESSION) if SESSION else "me", API_ID, API_HASH)

async def main():
    await client.start()
    async for d in client.iter_dialogs():
        ent = d.entity
        title = getattr(ent, "title", None)
        if isinstance(ent, (Channel, Chat)) and title:
            print(f"{title:40}  id={ent.id}  type={type(ent).__name__}  forum={getattr(ent,'forum',False)}")
            # Supergroups/channels: id like -1001234567890
            # Basic groups: negative id without -100 prefix
    print("\nPick the exact title line above and use its id (negative).")

with client:
    client.loop.run_until_complete(main())
