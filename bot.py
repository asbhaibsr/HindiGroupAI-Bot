from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN
from keep_alive import keep_alive
from ai_reply import generate_ai_reply
from db import save_chat, get_similar_reply
import commands  # Load all commands like /start, /help etc.

keep_alive()

Bot = Client("SonaAI", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@Bot.on_message(filters.text & filters.group & ~filters.command(["start", "help", "settings"]))
async def ai_chat(client, message: Message):
    reply = await get_similar_reply(message.text)
    if not reply:
        reply = await generate_ai_reply(message.text)
        await save_chat(message.from_user.id, message.text, reply)
    await message.reply_text(reply)

Bot.run()
