import os

API_ID = int(os.environ.get("API_ID", "29970536"))
API_HASH = os.environ.get("API_HASH", "f4bfdcdd4a5c1b7328a7e4f25f024a09"))
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token_here")
OWNER_ID = int(os.environ.get("OWNER_ID", "7315805581"))

# ✅ AI Memory MongoDB URL:
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://wtqf35lojv:9uhGrKZE4i0zz05x@cluster0.nmtfsys.mongodb.net/?retryWrites=true&w=majority&tls=true")

DB_NAME = "ai_memory"
