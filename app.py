import streamlit as st
from name_generator import generate_startup_names
from domain_checker import check_domain_availability

st.set_page_config(page_title="AI Startup Name Generator", layout="centered")
st.title("🤖 AI Startup Name Generator + Domain Checker")

st.markdown("Generate creative company names using AI and instantly check domain availability!")

keywords = st.text_input("💡 Enter business idea or keywords", placeholder="e.g. beauty, AI, mehndi")
count = st.slider("📌 How many name suggestions?", 3, 10, 5)

if st.button("🔍 Generate + Check Domain"):
    if keywords.strip() == "":
        st.warning("Please enter some keywords.")
    else:
        with st.spinner("Generating names using AI..."):
            names = generate_startup_names(keywords, count)
        
        st.success("✅ AI Suggested Names with Domain Status:")

        for name in names:
            clean_name = name.strip().replace(" ", "").lower()
            st.markdown(f"### 🔹 {name.strip()}")

            with st.spinner(f"Checking domain availability for: `{clean_name}`"):
                results = check_domain_availability(clean_name)
                for domain, status in results.items():
                    st.markdown(f"- 🔗 **{domain}** — {status}")
            st.markdown("---")
