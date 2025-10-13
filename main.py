import mimetypes
import json
import asyncio
from telethon import events, TelegramClient
from telethon.tl.types import PeerUser, MessageMediaPhoto, MessageMediaDocument, DocumentAttributeVideo
from telethon.tl.patched import Message
from setup_logger import setup_logger
from logging import Logger

logger: Logger = setup_logger("bot")

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
        me = await client.get_me()
        logger.info(f"Bot started as {me.username}")

        @client.on(events.NewMessage(incoming=True))
        async def handler(event: events.NewMessage.Event):
            message: Message = event.message
            if message.out: return
            if not message.is_private: return
            if not isinstance(message.peer_id, PeerUser): return
            if not message.media.ttl_seconds: return
            if not isinstance(message.media, (MessageMediaPhoto, MessageMediaDocument)): return
            if isinstance(message.media, MessageMediaDocument):
                if not any(isinstance(attr, DocumentAttributeVideo) for attr in message.media.document.attributes):
                    return
        
            sender = await event.get_sender()
            text = (
                f"Новое секретное сообщение\n"
                f"От {sender.first_name}"
            )

            media_bytes = await client.download_file(message.media, bytes)
            
            file_extension = mimetypes.guess_extension(message.media.document.mime_type) if hasattr(message.media, 'document') else '.jpg'

            print('-> [save_secret] - Сохранил секретное сообщение')
            await client.send_file(entity='me', file=await client.upload_file(file=media_bytes, file_name=f"secret{file_extension}"), caption=text, video_note=True if hasattr(message.media, 'document') else False)

        while True:
            try:
                await client.run_until_disconnected()
            except Exception as e:
                logger.warning(f"Телеграм упал жопа что делать рестарт короче!!! {e}")
                
asyncio.run(start())