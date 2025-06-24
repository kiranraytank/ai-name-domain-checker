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

st.set_page_config(page_title="AI Startup Name Generator", layout="centered")
st.title("🤖 AI Startup Name Generator + Domain Checker")
st.markdown("Generate creative company names using AI and instantly check domain availability!")

# --- Initialize session state ---
if "button_disabled" not in st.session_state:
    st.session_state.button_disabled = False

if "generated_names" not in st.session_state:
    st.session_state.generated_names = []

if "domain_results" not in st.session_state:
    st.session_state.domain_results = {}

if "suggested_name" not in st.session_state:
    st.session_state.suggested_name = ""

if "timestamp" not in st.session_state:
    st.session_state.timestamp = ""

# --- Input Section ---
keywords = st.text_input("💡 Enter business idea or keywords", placeholder="e.g. beauty, AI, mehndi", key="keywords")
count = st.slider("📌 How many name suggestions?", 1, 10, 5, key="count")
st.markdown(f"Count -  {count}")

# --- Main Processing ---
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
                continue  # ✅ Skip already checked
            results = check_domain_availability(clean_name)
            st.session_state.domain_results[name] = results

    st.session_state.button_disabled = False

# --- Trigger Button ---
st.button("🔍 Generate + Check Domain", on_click=process_generation, disabled=st.session_state.button_disabled)

# --- Output Section ---
if st.session_state.generated_names:
    st.success("✅ AI Suggested Names with Domain Status:")

    csv_data = []
    for name in st.session_state.generated_names:
        label = "✨ Suggested Name" if name == st.session_state.suggested_name else ""
        header_col1, header_col2 = st.columns([4, 1])
        with header_col1:
            st.markdown(f"### 🔹 {name} {label} <button onclick=\"navigator.clipboard.writeText('{name}')\">📋</button>", unsafe_allow_html=True)
        
        if name in st.session_state.domain_results:
            for domain, status in st.session_state.domain_results[name].items():
                st.markdown(f"<div style='overflow-wrap: break-word;'>- 🔗 <strong>{domain}</strong> — {status}</div>", unsafe_allow_html=True)
                csv_data.append({"Name": name, "Suggested": "Yes" if name == st.session_state.suggested_name else "No", "Domain": domain, "Status": status})
        st.markdown("---")

    # ✅ Prepare CSV DataFrame
    df = pd.DataFrame(csv_data)
    csv = df.to_csv(index=False).encode("utf-8")

    # ✅ Generate PDF Buffer
    def generate_pdf_table(keywords, data, timestamp):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph("AI Startup Name Suggestions", styles["Title"]))
        elements.append(Spacer(1, 12))
        centered_text = f"<para align='center'><b>Keywords:</b> {keywords}<br/><b>Generated On:</b> {timestamp}</para>"
        elements.append(Paragraph(centered_text, styles["Normal"]))
        elements.append(Spacer(1, 12))

        table_data = [["Name", "Suggested", "Domain", "Status"]]
        for row in data:
            table_data.append([row["Name"], row["Suggested"], row["Domain"], row["Status"]])

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

    # ✅ Download Buttons Side by Side
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("⬇️ Download CSV", data=csv, file_name="startup_names.csv", mime="text/csv")
    with col2:
        st.download_button("⬇️ Download PDF", data=pdf_buffer, file_name="startup_names.pdf", mime="application/pdf")

    # ✅ Informational Note
    st.markdown("📂 **Note:** You can download this list of AI-generated startup names and their domain availability to use or share later.")