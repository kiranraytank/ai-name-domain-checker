from name_generator import generate_startup_names
from domain_checker import check_domain_availability

print("\n🔵 Welcome to AI Startup Name Generator + Domain Checker\n")
keywords = input("🔤 Enter your business idea or keywords (e.g. beauty, AI, mehndi): ")
count = input("📌 How many name suggestions do you want? (default 5): ")

count = int(count) if count.isdigit() else 5
print("\n⏳ Generating AI names...")

names = generate_startup_names(keywords, count)

print("\n✅ Suggested Names:\n")
for name in names:
    clean_name = name.strip().replace(" ", "")
    print(f"🔸 {name.strip()}")

    results = check_domain_availability(clean_name)
    for domain, status in results.items():
        print(f"   🔗 {domain}: {status}")
    print("—" * 30)
