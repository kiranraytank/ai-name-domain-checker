import streamlit as st
from name_generator import generate_startup_names
from domain_checker import check_domain_availability

# --- Page config ---
st.set_page_config(page_title="AI Startup Name Generator", layout="centered")
st.title("🤖 AI Startup Name Generator + Domain Checker")
st.markdown("Generate creative company names using AI and instantly check domain availability!")

# --- Session state init ---
if "button_disabled" not in st.session_state:
    st.session_state.button_disabled = False

if "generated_names" not in st.session_state:
    st.session_state.generated_names = []

if "domain_results" not in st.session_state:
    st.session_state.domain_results = {}

# --- Input fields ---
keywords = st.text_input("💡 Enter business idea or keywords", placeholder="e.g. beauty, AI, mehndi", key="keywords")
count = st.slider("📌 How many name suggestions?", 1, 10, 5, key="count")
st.markdown(f"Count -  {count}")

# --- Generate logic ---
def process_generation():
    st.session_state.button_disabled = True

    if st.session_state.keywords.strip() == "":
        st.warning("Please enter some keywords.")
        st.session_state.button_disabled = False
        return

    with st.spinner("Generating names using AI..."):
        names = generate_startup_names(st.session_state.keywords, st.session_state.count)
        st.session_state.generated_names = names
        st.session_state.domain_results = {}  # Reset domain results

        for name in names:
            clean_name = name.strip().replace(" ", "").lower()
            results = check_domain_availability(clean_name)
            st.session_state.domain_results[name] = results

    st.session_state.button_disabled = False

# --- Actual Button ---
st.button("🔍 Generate + Check Domain", on_click=process_generation, disabled=st.session_state.button_disabled)

# ✅ Output Section: Show only if names exist
if st.session_state.generated_names:
    st.success("✅ AI Suggested Names with Domain Status:")

    for name in st.session_state.generated_names:
        st.markdown(f"### 🔹 {name.strip()}")

        if name in st.session_state.domain_results:
            for domain, status in st.session_state.domain_results[name].items():
                st.markdown(f"- 🔗 **{domain}** — {status}")
        st.markdown("---")
