# gen_session_string.py
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("SESSION_STRING=", client.session.save())
