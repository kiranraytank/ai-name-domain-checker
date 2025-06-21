import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_startup_names(keywords, count=5):

    print("Loaded API KEY:", API_KEY)   # Debug purpose
    prompt = f"""Suggest {count} creative and brandable company names based on the following business idea or keywords: "{keywords}".
Return names in a plain list without numbers or quotes."""

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

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        return content.strip().split("\n")
    else:
        return [f"Error: {response.status_code} - {response.text}"]
