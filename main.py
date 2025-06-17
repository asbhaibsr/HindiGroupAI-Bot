from bot import bot
from keep_alive import keep_alive
import asyncio
from pyrogram.idle import idle

keep_alive()

async def main():
    await bot.start()
    print("🤖 Bot is running...")
    await idle()
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
