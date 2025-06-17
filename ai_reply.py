import httpx
import random
import json

# List of fallback AI APIs
FREE_AI_APIS = [
    "https://yqcloud.openai-proxy.xyz/v1/chat/completions",
    "https://api.aichat.io/v1/chat/completions",
    "https://ai.fakeopen.com/v1/chat/completions",
]

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer pk-thisisfake"  # free endpoints don't need real key
}

async def generate_ai_reply(message: str) -> str:
    system_prompt = "You are a cute and smart Hindi girl AI who gives flirty, funny, romantic, emotional and smart replies."

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "temperature": 0.7,
    }

    for api_url in FREE_AI_APIS:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.post(api_url, json=payload, headers=HEADERS)
                if r.status_code == 200:
                    data = r.json()
                    return data["choices"][0]["message"]["content"]
        except Exception:
            continue

    return "😓 Mujhe kuch technical problem ho gayi. Thodi der baad try karo!"
