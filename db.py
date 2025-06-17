from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME
from datetime import datetime, timedelta

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

async def save_chat(user_id, msg, reply):
    await collection.insert_one({
        "user_id": user_id,
        "msg": msg,
        "reply": reply,
        "time": datetime.utcnow()
    })

async def get_similar_reply(user_msg):
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    cursor = collection.find({"time": {"$gte": one_day_ago}})
    async for doc in cursor:
        if doc["msg"].lower() in user_msg.lower():
            return doc["reply"]
    return None
