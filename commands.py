from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    await message.reply_text(
        "🌸 Hello! Main hoon Sona AI, aapki dosti, pyaar, aur madad ke liye 💖\n\n"
        "🧠 Mera kaam hai smart aur funny baatein karna.\n"
        "➕ Mujhe group mein add karo aur maza lo!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Me to Group", url=f"https://t.me/{client.me.username}?startgroup=true")],
            [InlineKeyboardButton("📽 Movie Group", url="https://t.me/iStreamX")],
            [InlineKeyboardButton("📢 Update Channel", url="https://t.me/asbhai_bsr")]
        ])
    )

@Client.on_message(filters.command("help"))
async def help_cmd(client, message: Message):
    await message.reply_text("💡 Help:\n/start - Intro\n/help - Help\n/settings - (Coming soon)")

@Client.on_message(filters.command("settings"))
async def settings_cmd(client, message: Message):
    await message.reply_text("⚙ Settings feature coming soon!")
