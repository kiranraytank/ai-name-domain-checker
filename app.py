import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from name_generator import generate_startup_names
from domain_checker import check_domain_availability
from PIL import Image
import os
import base64
import streamlit.components.v1 as components

# SEO and Social Meta Tags
components.html("""
<head>
    <title>AI Brand Name Generator with Domain Check</title>
    <meta name="description" content="Generate AI-based startup names and instantly check domain availability. Perfect for founders, marketers, and developers.">
    <meta property="og:title" content="AI Brand Name Generator with Domain Check" />
    <meta property="og:description" content="Generate AI-based startup names and instantly check domain availability. Perfect for startup founders, marketers, and creators." />
    <meta property="og:image" content="https://ai-name-domain-checker.onrender.com/assets/raytiklogo-main.png" />
    <meta property="og:url" content="https://ai-name-domain-checker.onrender.com/" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="robots" content="index, follow" />
</head>
""", height=0)

# Page Setup
st.set_page_config(page_title="AI Startup Name Generator", layout="centered")

# Dark Mode Toggle
dark_mode = st.toggle("🌙 Enable Dark Mode", value=False)
if dark_mode:
    st.markdown("""
        <style>
        body, .stApp { background-color: #0e1117; color: #e0e0e0; }
        input, textarea, .stTextInput input { background-color: #1e1e1e !important; color: #ffffff !important; border: 1px solid #555 !important; }
        .stButton > button { background-color: #2a2a2a; color: white; border: 1px solid #444; }
        .stDownloadButton button { background-color: #444; color: white; }
        h1, h2, h3, h4, h5, h6, p, label, span, a { color: #e0e0e0 !important; }
        .block-container { box-shadow: none !important; }
        </style>
    """, unsafe_allow_html=True)

# Logo + Title
image_path = os.path.join(os.path.dirname(__file__), "assets", "raytiklogo-main.png")
logo_html = ""
if os.path.exists(image_path):
    image = Image.open(image_path)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    logo_html = f'<img src="data:image/png;base64,{img_str}" width="100" style="display:block;margin:auto;">'

st.markdown(f"""
<div style='text-align: center;'>
    {logo_html}
    <h2 style='font-size:28px; font-weight:600;'>🤖 Instantly generate AI-powered brand names with domain availability check.</h2>
    <p style='font-size:16px;'>Generate creative company names using AI and instantly check domain availability!</p>
</div>
""", unsafe_allow_html=True)

# Session State
for key in ["button_disabled", "generated_names", "domain_results", "suggested_name", "timestamp"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "button_disabled" else [] if "names" in key else ""

# Inputs
keywords = st.text_input("💡 Enter business idea or keywords", placeholder="e.g. beauty, AI, mehndi", key="keywords")
count = st.slider("📌 How many name suggestions?", 1, 10, 5, key="count")

# Button Callback
def process_generation():
    st.session_state.button_disabled = True
    if st.session_state.keywords.strip() == "":
        st.warning("Please enter some keywords.")
        st.session_state.button_disabled = False
        return

    with st.spinner("Generating names using AI..."):
        names, suggested = generate_startup_names(st.session_state.keywords, st.session_state.count)
        st.session_state.generated_names = names
        st.session_state.suggested_name = suggested
        st.session_state.domain_results = {}
        st.session_state.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for name in names:
            clean_name = name.strip().replace(" ", "").lower()
            if name in st.session_state.domain_results:
                continue
            try:
                results = check_domain_availability(clean_name)
                st.session_state.domain_results[name] = results
            except Exception as e:
                st.session_state.domain_results[name] = {"Error": str(e)}

    st.session_state.button_disabled = False

st.button("🔍 Generate + Check Domain", on_click=process_generation, disabled=st.session_state.button_disabled)

# Output Display
if st.session_state.generated_names:
    st.success("✅ AI Suggested Names with Domain Status:")
    csv_data = []

    for name in st.session_state.generated_names:
        is_suggested = name == st.session_state.suggested_name
        label = "<span style='color:#00ffcc; font-weight:bold;'>✨ Suggested Name</span>" if is_suggested else ""
        st.markdown(f"### 🔹 {name} {label}", unsafe_allow_html=True)

        domains = st.session_state.domain_results.get(name, {})
        for domain, status in domains.items():
            st.markdown(f"<div style='overflow-wrap: break-word;'>- 🔗 <strong>{domain}</strong> — {status}</div>", unsafe_allow_html=True)
            csv_data.append({"Name": name, "Suggested": "Yes" if is_suggested else "No", "Domain": domain, "Status": status})
        st.markdown("---")

    # CSV + PDF Downloads
    df = pd.DataFrame(csv_data)
    csv = df.to_csv(index=False).encode("utf-8")

    def generate_pdf_table(keywords, data, timestamp):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = [Paragraph("AI Startup Name Suggestions", styles["Title"]), Spacer(1, 12)]
        elements.append(Paragraph(f"<para align='center'><b>Keywords:</b> {keywords}<br/><b>Generated On:</b> {timestamp}</para>", styles["Normal"]))
        elements.append(Spacer(1, 12))

        table_data = [["Name", "Suggested", "Domain", "Status"]] + [[r["Name"], r["Suggested"], r["Domain"], r["Status"]] for r in data]
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ]))
        elements.append(table)
        doc.build(elements)
        buffer.seek(0)
        return buffer

    pdf_buffer = generate_pdf_table(st.session_state.keywords, csv_data, st.session_state.timestamp)

    st.markdown("#### 📂 Download Results")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📄 Download CSV", data=csv, file_name="startup_names.csv", mime="text/csv")
    with col2:
        st.download_button("📑 Download PDF", data=pdf_buffer, file_name="startup_names.pdf", mime="application/pdf")

    # Share Buttons
    st.markdown("#### 🙌 Share or Give Feedback")
    col1, col2 = st.columns(2)
    with col1:
        twitter_link = "https://twitter.com/intent/tweet?text=Check+out+this+AI-powered+startup+name+generator+🚀+https://ai-name-domain-checker.onrender.com"
        st.markdown(f"""
            <a href="{twitter_link}" target="_blank">
                <button style='padding:10px 20px; border:none; border-radius:8px; background:#1DA1F2; color:white; font-size:16px; font-weight:bold; width:100%;'>
                    🐦 Tweet This Tool
                </button>
            </a>
        """, unsafe_allow_html=True)
    with col2:
        feedback_link = "https://forms.gle/dQSJZqtwKYuzgog68"
        st.markdown(f"""
            <a href="{feedback_link}" target="_blank">
                <button style='padding:10px 20px; border:none; border-radius:8px; background:#28a745; color:white; font-size:16px; font-weight:bold; width:100%;'>
                    ✍ Submit Feedback
                </button>
            </a>
        """, unsafe_allow_html=True)

# Footer
year = datetime.now().year
st.markdown(f"""
<hr style='margin-top: 50px; margin-bottom: 10px;'>
<div style='text-align: center; font-size:14px; color: #999;'>
<p>🚀 Made with <span style='color: #e25555;'>&#10084;&#65039;</span> by <strong>Raytik</strong></p>
<p>
<a href="https://www.linkedin.com/in/kiran-tank/" target="_blank" style='color: inherit; margin: 0 8px;'>🔗 LinkedIn</a> |
<a href="https://kirantank.my.canva.site/" target="_blank" style='color: inherit; margin: 0 8px;'>🌐 Portfolio</a> |
<a href="https://www.fiverr.com/s/EgN2x2K" target="_blank" style='color: inherit; margin: 0 8px;'>🛠 Fiverr</a>
</p>
<p style='margin-top: 6px;'>© {year} Raytik. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
