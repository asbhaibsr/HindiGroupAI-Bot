import random
import httpx

async def generate_ai_reply(user_message: str) -> str:
    user_message = user_message.strip()

    if not user_message:
        return "😅 Tumne to kuch likha hi nahi! Pehle kuch to bolo 💬"

    backends = [
        ask_g4f,
        ask_phind,
        ask_gemini,
        ask_yqcloud
    ]

    for backend in backends:
        try:
            response = await backend(user_message)
            if response and len(response.strip()) > 0:
                return response.strip()
        except Exception:
            continue

    return "😓 Mujhe kuch technical problem ho gayi. Thodi der baad try karo!"

# ---- BACKEND 1: g4f (fake ChatGPT)
async def ask_g4f(prompt: str) -> str:
    url = "https://gpt4chat.loca.lt/api"
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json={"prompt": prompt})
        return r.json().get("response", "")

# ---- BACKEND 2: phind
async def ask_phind(prompt: str) -> str:
    url = "https://phind-api.vercel.app/api"
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json={"prompt": prompt})
        return r.json().get("text", "")

# ---- BACKEND 3: Gemini API (fake)
async def ask_gemini(prompt: str) -> str:
    url = "https://gemini-api-nu.vercel.app/api/gemini"
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json={"message": prompt})
        return r.json().get("text", "")

# ---- BACKEND 4: yqcloud (Chinese free ChatGPT)
async def ask_yqcloud(prompt: str) -> str:
    url = "https://freegptapi.vercel.app/api/openai"
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json={"prompt": prompt})
        return r.json().get("response", "")
