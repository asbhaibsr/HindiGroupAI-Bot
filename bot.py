from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID
from ai_reply import generate_ai_reply
from db import save_chat, get_similar_reply
from commands import *

bot = Client("Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.private & ~filters.command(["start", "help", "stats", "clear"]))
async def private_msg(bot, message: Message):
    await bot.send_message(
        OWNER_ID,
        f"💌 Message from [{message.from_user.first_name}](tg://user?id={message.from_user.id}):\n\n{message.text}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✉️ Reply", callback_data=f"reply_{message.from_user.id}")]
        ])
    )
    await message.reply("💖 Tumhara message owner tak pahuch gaya... reply aayega 😘")

@bot.on_callback_query(filters.regex("reply_"))
async def handle_reply(bot, query):
    user_id = int(query.data.split("_")[1])
    await query.message.reply(f"✍️ Reply to user {user_id}:", quote=True)

@bot.on_message(filters.reply & filters.user(OWNER_ID))
async def send_reply(bot, message: Message):
    if message.reply_to_message:
        try:
            user_id = int(message.reply_to_message.text.split()[-1][:-1])
            await bot.send_message(user_id, f"📬 Owner reply:\n\n{message.text}")
            await message.reply("✅ Sent!")
        except Exception:
            pass

@bot.on_message(filters.group & ~filters.command(["start", "help", "stats", "clear"]))
async def group_ai(bot, message: Message):
    if message.text:
        reply = await get_similar_reply(message.text)
        if not reply:
            reply = await generate_ai_reply(message.text)
            await save_chat(message.from_user.id, message.text, reply)
        await message.reply(reply)
