from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID
from db import collection

@filters.command("start")
async def start_cmd(client, message: Message):
    await message.reply_photo(
        photo="https://te.legra.ph/file/aa34fa4e43b0bb66d8b8d.jpg",
        caption="Hi baby! ❤️ Main ek pyari AI hoon jo sirf tumhare liye hoon 💋",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Me", url=f"https://t.me/{client.me.username}?startgroup=true")],
            [InlineKeyboardButton("🎥 Movie Group", url="https://t.me/iStreamX")],
            [InlineKeyboardButton("📢 Channel", url="https://t.me/asbhai_bsr")]
        ])
    )

@filters.command("help")
async def help_cmd(client, message: Message):
    await message.reply("Sirf group mein lagao aur AI girl se baat karo 😘")

@filters.command("stats") & filters.user(OWNER_ID)
async def stats_cmd(client, message: Message):
    count = await collection.count_documents({})
    await message.reply(f"Total messages stored: {count}")

@filters.command("clear") & filters.user(OWNER_ID)
async def clear_cmd(client, message: Message):
    await collection.delete_many({})
    await message.reply("Memory clean kar di! 🧹")
