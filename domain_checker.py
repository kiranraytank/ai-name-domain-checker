# domain_checker.py

import requests

def check_domain_availability(name):
    extensions = ['.com', '.in', '.net', '.ai', '.co']
    results = {}

    for ext in extensions:
        domain = f"{name.lower()}{ext}"
        url = f"https://api.domainsdb.info/v1/domains/search?domain={domain}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            if 'domains' in data and any(d.get('domain') == domain for d in data['domains']):
                results[domain] = "❌ Taken"
            else:
                results[domain] = "✅ Available"

        except requests.exceptions.RequestException as e:
            results[domain] = f"⚠️ API Error"
        except Exception as e:
            results[domain] = "⚠️ Unknown Error"

    return results
