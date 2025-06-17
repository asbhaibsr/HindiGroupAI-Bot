from pymongo import MongoClient
from config import MONGO_URL, DB_NAME
import random

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
memory_collection = db["user_memory"]

# तुम जो fallback वाली AI logic use करते हो उसे import करो:
from gpt_fallback import get_best_response

async def get_memory_based_reply(user_id, user_message):
    past_replies = memory_collection.find_one({"user_id": user_id})

    if past_replies and "history" in past_replies:
        for entry in past_replies["history"]:
            if entry["question"].lower() == user_message.lower():
                return entry["answer"] + "\n\n_💡 (Ye reply mujhe yaad tha!)_"

    # नया AI जवाब लो
    ai_reply = await get_best_response(user_message)

    # Database में save करो
    if past_replies:
        memory_collection.update_one(
            {"user_id": user_id},
            {"$push": {"history": {"question": user_message, "answer": ai_reply}}}
        )
    else:
        memory_collection.insert_one({
            "user_id": user_id,
            "history": [{"question": user_message, "answer": ai_reply}]
        })

    return ai_reply
