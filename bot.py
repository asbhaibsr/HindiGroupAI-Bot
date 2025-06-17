import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from flask import Flask
import threading
import random
import datetime
import aiohttp

# ENV
API_ID = 28762030
API_HASH = "918e2aa94075a7d04717b371a21fb689"
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = int(os.environ.get("OWNER_ID"))
PORT = int(os.environ.get("PORT", 8080))

# MongoDB
user_db = MongoClient("mongodb+srv://wtqf35lojv:9uhGrKZE4i0zz05x@cluster0.nmtfsys.mongodb.net/?retryWrites=true&w=majority&tls=true")["AngelBot"]["users"]
ai_memory = MongoClient("mongodb+srv://wtqf35lojv:9uhGrKZE4i0zz05x@cluster0.nmtfsys.mongodb.net/?retryWrites=true&w=majority&tls=true")["AngelBot"]["chat_memory"]

# Flask Uptime Server
app = Flask("bot")
@app.route("/")
def home():
    return "Bot is alive! 💖"
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=PORT)).start()

# AI SYSTEM with fallback
async def generate_ai_reply(prompt: str) -> str:
    try:
        # Try g4f
        from g4f.client import Client as G4FClient
        client = G4FClient()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception:
        pass
    try:
        # Try YQCloud fallback
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.yqcloud.top/ai/chatgpt?message={prompt}") as resp:
                data = await resp.json()
                return data.get("content", "😶 Mujhe samajh nahi aaya.")
    except Exception:
        return "😓 Mujhe kuch technical problem ho gayi. Thodi der baad try karo!"

# Get memory-based reply
async def get_memory_based_reply(user_id, prompt):
    previous = ai_memory.find_one({"q": prompt})
    if previous:
        return previous["a"]
    reply = await generate_ai_reply(prompt)
    ai_memory.insert_one({"q": prompt, "a": reply, "from": user_id})
    return reply

# Pyrogram Client
bot = Client("Angel", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Commands
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

# AI Chat in group
@bot.on_message(filters.text & filters.group & ~filters.bot)
async def ai_group(_, m: Message):
    if m.text.startswith("/"): return

    ai_memory.insert_one({
        "chat_id": m.chat.id,
        "user": m.from_user.first_name,
        "text": m.text,
        "time": datetime.datetime.now()
    })

    if random.randint(1, 150) == 3:
        promos = [
            "🔥 Join @asbhai_bsr – 18+ Premium Apps, Web Series & more!",
            "🎬 Movies ke liye @iStreamX group me search karo!"
        ]
        await m.reply_text(random.choice(promos))

    reply = await get_memory_based_reply(m.from_user.id, m.text)
    await m.reply_text(f"💬 {m.from_user.first_name} bol rahe ho: {reply}\n\n_Mujhe bhi kuch kehna hai?_", quote=True)

bot.run()
