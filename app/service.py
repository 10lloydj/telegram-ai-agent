import asyncio
import os

from dotenv import load_dotenv
from telethon import TelegramClient

# Load environment before importing other modules
load_dotenv()

from .db import engine, Session
from .models import Base
from .config import load_cfg

cfg = load_cfg()


def _create_client() -> TelegramClient:
    api_id = int(os.environ["API_ID"])  # ensure KeyError early if missing
    api_hash = os.environ["API_HASH"]
    return TelegramClient("me", api_id, api_hash)


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    client = _create_client()

    # Optional wiring: only if modules exist (we skip per instruction)
    try:
        import app.ingestion as ingestion  # type: ignore
        import app.notifier as notifier  # type: ignore
        ingestion.client = client
        notifier.client = client
    except Exception:
        pass

    await client.start()
    
    # Attach message listeners
    try:
        from .ingestion import attach_listeners
        attach_listeners(client, Session)
        print("Agent running with ingestion/notifier enabled")
    except Exception as e:
        print(f"Agent running without ingestion: {e}")
    
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())


