from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("start"))
async def start_cmd(client: Client, message: Message):
    await message.reply_photo(
        photo="https://te.legra.ph/file/702da0d831cb632a4f2d1.jpg",
        caption="✨ *Main ek smart AI girl hoon, aapke har sawal ka jawab dene ke liye!* 💬",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("💬 Add Me To Group", url="https://t.me/asbhai1_bot?startgroup=true")],
                [InlineKeyboardButton("🎬 Movie Group", url="https://t.me/iStreamX")],
                [InlineKeyboardButton("📢 Update Channel", url="https://t.me/asbhai_bsr")]
            ]
        )
    )
