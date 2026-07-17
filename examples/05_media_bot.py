"""
Example: Media Handling Bot

Demonstrates file upload/download, media processing, and media forwarding.
Users can send media and the bot will process and return information about it.
"""

import asyncio
import mimetypes
from pathlib import Path
from pyfortg import TelegramBot, Filters


async def main():
    bot = TelegramBot(token="YOUR_BOT_TOKEN")

    # Handler: Start command
    @bot.on_command("start")
    async def handle_start(bot, update, context):
        await bot.send_message(
            chat_id=update.message.chat.id,
            text="""
Welcome to Media Bot!
Send me any media and I'll help you with:
- Photo analysis
- Document information
- Video/Audio metadata
- File sharing

Try sending a photo, video, document, or audio file!
            """
        )

    # Handler: Photo messages
    @bot.on_message(Filters.photo)
    async def handle_photo(bot, update, context):
        photo = update.message.photo[-1]  # Get highest resolution
        
        # Get file info
        file_info = await bot.get_file(photo.file_id)
        
        await bot.send_message(
            chat_id=update.message.chat.id,
            text=f"""
📷 Photo Information:
File ID: {photo.file_id}
Width: {photo.width}px
Height: {photo.height}px
File Size: {file_info.get('file_size', 'Unknown')} bytes
            """
        )

    # Handler: Document messages
    @bot.on_message(Filters.document)
    async def handle_document(bot, update, context):
        document = update.message.document
        
        # Get file info
        file_info = await bot.get_file(document.file_id)
        
        # Get MIME type
        mime_type = document.mime_type or "Unknown"
        
        await bot.send_message(
            chat_id=update.message.chat.id,
            text=f"""
📄 Document Information:
Filename: {document.file_name}
MIME Type: {mime_type}
File Size: {document.file_size} bytes
File ID: {document.file_id}
            """
        )

    # Handler: Video messages
    @bot.on_message(Filters.video)
    async def handle_video(bot, update, context):
        video = update.message.video
        
        # Get file info
        file_info = await bot.get_file(video.file_id)
        
        await bot.send_message(
            chat_id=update.message.chat.id,
            text=f"""
🎬 Video Information:
Width: {video.width}px
Height: {video.height}px
Duration: {video.duration} seconds
MIME Type: {video.mime_type or 'Unknown'}
File Size: {video.file_size} bytes
            """
        )

    # Handler: Audio messages
    @bot.on_message(Filters.audio)
    async def handle_audio(bot, update, context):
        audio = update.message.audio
        
        await bot.send_message(
            chat_id=update.message.chat.id,
            text=f"""
🎵 Audio Information:
Title: {audio.title or 'Unknown'}
Performer: {audio.performer or 'Unknown'}
Duration: {audio.duration} seconds
MIME Type: {audio.mime_type or 'Unknown'}
File Size: {audio.file_size} bytes
            """
        )

    # Handler: Voice messages
    @bot.on_message(Filters.voice)
    async def handle_voice(bot, update, context):
        voice = update.message.voice
        
        await bot.send_message(
            chat_id=update.message.chat.id,
            text=f"""
🎤 Voice Message:
Duration: {voice.duration} seconds
MIME Type: {voice.mime_type}
File Size: {voice.file_size} bytes
            """
        )

    # Handler: Any media with /info command
    @bot.on_command("info")
    async def handle_info(bot, update, context):
        await bot.send_message(
            chat_id=update.message.chat.id,
            text="""
Media Information Available For:
- Photos (resolution, dimensions)
- Documents (filename, type, size)
- Videos (dimensions, duration)
- Audio (title, performer, duration)
- Voice messages (duration)

Reply to a message with /info to get more details!
            """
        )

    # Handler: Download command (example)
    @bot.on_command("download")
    async def handle_download(bot, update, context):
        if update.message.reply_to_message:
            reply = update.message.reply_to_message
            
            # Try to download different media types
            if reply.photo:
                file_id = reply.photo[-1].file_id
                media_type = "photo"
            elif reply.document:
                file_id = reply.document.file_id
                media_type = "document"
            elif reply.video:
                file_id = reply.video.file_id
                media_type = "video"
            elif reply.audio:
                file_id = reply.audio.file_id
                media_type = "audio"
            else:
                await bot.send_message(
                    chat_id=update.message.chat.id,
                    text="Please reply to a media message!"
                )
                return

            try:
                # Download file
                file_bytes = await bot.download_file(file_id)
                
                # In production, save to cloud storage or process
                await bot.send_message(
                    chat_id=update.message.chat.id,
                    text=f"""
✅ Downloaded {media_type}!
Size: {len(file_bytes)} bytes

In production, this would be saved to cloud storage or processed.
                    """
                )
            except Exception as e:
                await bot.send_message(
                    chat_id=update.message.chat.id,
                    text=f"Error downloading file: {str(e)}"
                )
        else:
            await bot.send_message(
                chat_id=update.message.chat.id,
                text="Please reply to a media message with /download"
            )

    # Run bot
    await bot.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
