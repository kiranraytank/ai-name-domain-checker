import os
import requests
from dotenv import load_dotenv
import time

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_startup_names(keywords, count=5, retries=2):
    prompt = f"""Suggest exactly {count} creative, brandable startup names for this idea: "{keywords}".
Just plain list of names. No numbering, quotes, or explanations."""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a branding expert."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=20)
        response.raise_for_status()
        content = response.json()

        ai_response = content["choices"][0]["message"]["content"]
        lines = [line.strip("-•🔹 ").strip() for line in ai_response.strip().split("\n") if line.strip()]
        names = lines[:count]

        # Retry if fewer names than requested
        if len(names) < count and retries > 0:
            print("⚠️ Fewer names received. Retrying...")
            time.sleep(2)
            return generate_startup_names(keywords, count, retries=retries - 1)

        return names

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        print("🚫 Network error occurred. Retrying..." if retries > 0 else "❌ Final attempt failed.")
        if retries > 0:
            time.sleep(3)
            return generate_startup_names(keywords, count, retries=retries - 1)
        return []

    except Exception as e:
        print("❌ Other Error occurred:", e)
        return []
