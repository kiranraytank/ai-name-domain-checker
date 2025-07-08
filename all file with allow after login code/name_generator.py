# name_generator.py

import os
import requests
from dotenv import load_dotenv
import time

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_startup_names(keywords, count=5, retries=2):
    return ['kiran', 'kirandt'], ""

    prompt = f"""Give exactly {count} creative, brandable startup name suggestions for this idea: "{keywords}".
Return only the names, one per line — no numbers, no quotes, no introductions.

Then in the last line, write:
Suggested: <one best name from list>"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost",  # Optional
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
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=20
        )
        response.raise_for_status()
        content = response.json()
        ai_response = content["choices"][0]["message"]["content"]

        lines = [line.strip() for line in ai_response.strip().split("\n") if line.strip()]
        names = []
        suggested_name = ""

        for line in lines:
            # Handle Suggested line
            if line.lower().startswith("suggested:"):
                suggested_name = line.split(":", 1)[-1].strip()
            # Only clean, valid names
            elif not any(
                line.lower().startswith(prefix)
                for prefix in ["sure", "here", "1.", "2.", "note", "these"]
            ):
                clean = line.strip("-•🔹 ").strip()
                if clean:
                    names.append(clean)

        names = names[:count]

        # Retry if fewer names than requested
        if len(names) < count and retries > 0:
            print("⚠️ Fewer names received. Retrying...")
            time.sleep(2)
            return generate_startup_names(keywords, count, retries=retries - 1)

        return names, suggested_name

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        print("🚫 Network error occurred. Retrying..." if retries > 0 else "❌ Final attempt failed.")
        if retries > 0:
            time.sleep(3)
            return generate_startup_names(keywords, count, retries=retries - 1)
        return [], ""

    except Exception as e:
        print("❌ Other Error occurred:", e)
        return [], ""
