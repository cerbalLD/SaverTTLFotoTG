import json
import asyncio
from telethon import  TelegramClient

with open('config.json') as f:
    config = json.load(f)

session_name = config['session_name']
api_id = config['api_id']
api_hash = config['api_hash']

client = TelegramClient(
            session_name,
            api_id,
            api_hash,
            system_version='4.16.30-vxCUSTOM',
            auto_reconnect=True,
            connection_retries=5,
            request_retries=5,
            timeout=120,
        )

async def start():
    await client.start()
    await client.run_until_disconnected()
    
asyncio.run(start())