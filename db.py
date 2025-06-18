from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client.sona_ai
collection = db.user_chats

async def save_chat(user_id, user_message, bot_reply):
    await collection.insert_one({
        "user_id": user_id,
        "message": user_message,
        "reply": bot_reply
    })

async def get_similar_reply(message):
    result = await collection.find_one({"message": message})
    return result['reply'] if result else None
