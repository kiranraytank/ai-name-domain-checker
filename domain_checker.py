# domain_checker.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

DOMAINR_CLIENT_ID = os.getenv("DOMAINR_CLIENT_ID")

def check_domain_availability(domain):
    url = f"https://api.domainr.com/v2/status?mashape-key={DOMAINR_CLIENT_ID}&domain={domain}"
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        results = response.json().get("status", [])
        for item in results:
            if item["domain"] == domain:
                return "✅ Available" if "active" not in item["status"] else "❌ Taken"
    return "⚠️ Error checking domain"
