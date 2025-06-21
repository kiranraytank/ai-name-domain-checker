# app.py
import streamlit as st
from name_generator import generate_startup_names
from domain_checker import check_domain_availability

st.set_page_config(page_title="AI Company Name + Domain Checker", layout="centered")
st.title("🤖 AI Company Name Generator + Domain Availability Checker")

st.markdown("Enter your business idea keywords to generate names and check domain status.")

keywords = st.text_input("💡 Enter keywords or niche", placeholder="e.g. mehndi, bridal, beauty, AI")
count = st.slider("📌 Number of name suggestions", 3, 10, 5)

if st.button("🔍 Generate Names + Check Domains"):
    if keywords.strip() == "":
        st.warning("Please enter some keywords.")
    else:
        with st.spinner("Generating names and checking domains..."):
            names = generate_startup_names(keywords, count)
            st.success("Here are your results:")

            for name in names:
                domain = name.strip().replace(" ", "").lower() + ".com"
                status = check_domain_availability(domain)
                st.markdown(f"🔹 **{name.strip()}** — `{domain}` → {status}")


# # app.py
# import streamlit as st
# from name_generator import generate_startup_names

# st.set_page_config(page_title="AI Company Name Generator", layout="centered")

# st.title("🤖 AI Startup Name Generator + Domain Checker (Step 1)")
# st.markdown("Enter a few keywords or your business idea. Get creative startup names.")

# keywords = st.text_input("💡 Enter business idea or keywords", placeholder="e.g. beauty, AI, mehndi")

# count = st.slider("📌 How many name suggestions?", 3, 10, 5)

# if st.button("🔍 Generate Names"):
#     if keywords.strip() == "":
#         st.warning("Please enter keywords first.")
#     else:
#         with st.spinner("Generating..."):
#             names = generate_startup_names(keywords, count)
#             st.success("Here are your AI-suggested names:")
#             for name in names:
#                 st.markdown(f"✅ **{name.strip()}**")
