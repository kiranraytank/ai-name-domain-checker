# name_generator.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_startup_names(keywords, count=5):
    prompt = f"""Suggest {count} creative and brandable company names based on the following business idea or keywords: "{keywords}".
Return names in a plain list without numbers or quotes."""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost",  # Not mandatory on Render
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
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()  # raises error if status != 200

        content = respon
