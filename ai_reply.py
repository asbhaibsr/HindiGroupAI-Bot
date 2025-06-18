import random
import httpx

async def generate_ai_reply(message: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post("https://yqcloud.openai-api.xyz/v1/chat/completions", json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": message}],
            })
            data = response.json()
            return data['choices'][0]['message']['content'].strip()
    except Exception as e:
        return random.choice([
            "Kya baat kar rahe ho aap 😅", 
            "Thoda aur clearly batao na 💭", 
            "Sona samajh nahi payi 🤔"
        ])
