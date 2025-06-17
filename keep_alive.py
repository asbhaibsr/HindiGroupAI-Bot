import httpx

async def generate_ai_reply(user_msg):
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # 1. g4f
            r1 = await client.post("https://g4f-api.com/api", json={"prompt": user_msg})
            if r1.status_code == 200 and "response" in r1.json():
                return r1.json()["response"]

            # 2. yqcloud
            r2 = await client.post("https://api.yqcloud.cn/chat", json={"message": user_msg})
            if r2.status_code == 200 and "reply" in r2.json():
                return r2.json()["reply"]

            # 3. Gemini
            r3 = await client.post("https://gemini-api.ai/open", json={"prompt": user_msg})
            if r3.status_code == 200 and "text" in r3.json():
                return r3.json()["text"]

            # 4. Phind
            r4 = await client.post("https://phind-api.pythondomain.com", json={"question": user_msg})
            if r4.status_code == 200 and "answer" in r4.json():
                return r4.json()["answer"]

    except Exception:
        pass

    return "😔 Sorry baby, abhi main thoda confused hoon... baad mein try karna 💋"
