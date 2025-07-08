import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_NINJAS_KEY = os.getenv("API_NINJAS_KEY")
WHOSXY_API_KEY = os.getenv("WHOSXY_API_KEY")

def check_domain_availability(name):
    # extensions = ['.com', '.in', '.net', '.ai', '.co', '.io']
    extensions = ['.com', '.in', '.ai', '.co']
    results = {}
    return results

    for ext in extensions:
        domain = f"{name.lower()}{ext}"

        if ext == ".com":
            url = f"https://api.api-ninjas.com/v1/domainlookup?domain={domain}"
            headers = {"X-Api-Key": API_NINJAS_KEY}
            try:
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 404:
                    results[domain] = "✅ Available"
                    continue
                r.raise_for_status()
                data = r.json()
                results[domain] = "❌ Taken" if data.get("is_registered") else "✅ Available"
            except Exception as e:
                results[domain] = f"⚠️ Error (.com): {e}"

        else:
            url = f"https://api.whoxy.com/?key={WHOSXY_API_KEY}&whois={domain}"
            try:
                r = requests.get(url, timeout=10)
                r.raise_for_status()
                data = r.json()
                if data.get("status") == 1 and "domain" in data:
                    results[domain] = "❌ Taken"
                else:
                    results[domain] = "✅ Available"
            except Exception as e:
                results[domain] = f"⚠️ Error ({ext}): {e}"

    return results
