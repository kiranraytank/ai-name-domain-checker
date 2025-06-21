import requests

def check_domain_availability(name):
    extensions = ['.com', '.in', '.net', '.ai', '.co']
    results = {}

    for ext in extensions:
        domain = f"{name.lower()}{ext}"
        url = f"https://api.domainsdb.info/v1/domains/search?domain={domain}"

        try:
            res = requests.get(url)
            data = res.json()

            if 'domains' in data and any(d['domain'] == domain for d in data['domains']):
                results[domain] = "❌ Taken"
            else:
                results[domain] = "✅ Available"

        except Exception as e:
            results[domain] = f"⚠️ Error: {e}"

    return results
