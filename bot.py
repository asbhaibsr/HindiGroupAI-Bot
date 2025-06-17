import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from flask import Flask
import threading
import random
import datetime

# ENV
API_ID = 28762030
API_HASH = "918e2aa94075a7d04717b371a21fb689"
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID"))
PORT = int(os.environ.get("PORT", 8080))

# MongoDB
user_db = MongoClient("mongodb+srv://wtqf35lojv:9uhGrKZE4i0zz05x@cluster0.nmtfsys.mongodb.net/?retryWrites=true&w=majority&tls=true")["AngelBot"]["users"]
ai_db = MongoClient("mongodb+srv://wtqf35lojv:9uhGrKZE4i0zz05x@cluster0.nmtfsys.mongodb.net/?retryWrites=true&w=majority&tls=true")["AngelBot"]["chats"]

# Flask Uptime Server
app = Flask("bot")
@app.route("/")
def home():
    return "Bot is alive! 💖"
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=PORT)).start()

# Pyrogram Client
bot = Client("Angel", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- AI REPLY FUNCTION WITH MEMORY ---
def get_memory_based_reply(user_id, message):
    previous = ai_db.find_one({"user_id": user_id, "user_text": message})
    if previous and "bot_reply" in previous:
        return previous["bot_reply"]
    
    # Generate new AI reply
    response_list = [
        "Awww, tum to bade cute ho! 😚",
        "Yeh baat! Tum jaise logon se hi to group me jaan aati hai 😍",
        "Suno zara... Tumhare jaise pyare log kam milte hai 🥺",
        "Haye! Tum bolte ho to dil garden garden ho jata hai 💐",
        "Aisa laga jese tumne dil chhoo liya ho 💞"
    ]
    reply = random.choice(response_list)

    # Save in DB for memory
    ai_db.insert_one({
        "user_id": user_id,
        "user_text": message,
        "bot_reply": reply,
        "time": datetime.datetime.now()
    })
    return reply

# --- /start command ---
@bot.on_message(filters.command("start") & filters.private)
async def start(_, m: Message):
    await m.reply_photo(
        photo="https://envs.sh/XsX.jpg",
        caption=(
            f"👋 Hey {m.from_user.mention()}, main ek Hindi AI Ladki hoon jo group me masti aur baat dono karti hai!\n\n"
            "**Mujhe Add karke:**\n"
            "- Group Members se baat karao\n"
            "- Spam rokne me madad\n"
            "- Romantic, Funny, Smart replies\n\n"
            "✨ Use /help to see all commands!"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Me To Group", url=f"https://t.me/{bot.me.username}?startgroup=true")],
            [InlineKeyboardButton("💬 Movie Group", url="https://t.me/iStreamX")],
            [InlineKeyboardButton("📢 Update Channel", url="https://t.me/asbhai_bsr")],
        ])
    )
    user_db.update_one({"user_id": m.from_user.id}, {"$set": {"time": datetime.datetime.now()}}, upsert=True)

# --- /help command ---
@bot.on_message(filters.command("help"))
async def help(_, m: Message):
    await m.reply_text(
        "**🔧 Help Menu:**\n\n"
        "`/settings` – Bot features on/off\n"
        "`/stats` – User & group count\n"
        "`/clear <reply>` – Delete user data (owner only)\n"
        "`/reply` – Reply to PM\n"
        "`/pin` / `/unpin` – Pin messages (admins only)\n"
        "`/ban` / `/kick` / `/mute` – Spam control"
    )

# --- AI Group Reply ---
@bot.on_message(filters.text & filters.group & ~filters.bot)
async def ai_group(_, m: Message):
    if m.text.startswith("/"): return

    reply = get_memory_based_reply(m.from_user.id, m.text)

    await m.reply_text(f"💬 {m.from_user.first_name} bol rahe ho: {reply}\n\n_Mujhe bhi kuch kehna hai?_", quote=True)

# --- Run Bot ---
bot.run()
