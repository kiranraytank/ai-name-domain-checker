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

# --- Page Setup ---
st.set_page_config(page_title="AI Startup Name Generator", layout="centered")

st.markdown("""
<style>
.modal {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-color: rgba(0,0,0,0.6);
    display: flex; align-items: center; justify-content: center;
    z-index: 1000;
}
.modal-content {
    background-color: white;
    padding: 30px;
    border-radius: 10px;
    width: 300px;
    box-shadow: 0 0 10px #00000050;
}
.modal-content input {
    width: 100%;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- Session State Init ---
for key, value in {
    "button_disabled": False,
    "generated_names": [],
    "domain_results": {},
    "suggested_name": "",
    "timestamp": "",
    "selected_name_for_logo": "",
    "is_logged_in": False,
    "show_login_modal": False,
    "show_signup_modal": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- Title ---
st.title("🤖 AI Startup Name Generator + Domain Checker")
st.markdown("Generate creative company names using AI and instantly check domain availability!")

# --- Input Section ---
keywords = st.text_input("💡 Enter business idea or keywords", placeholder="e.g. beauty, AI, mehndi", key="keywords")
count = st.slider("📌 How many name suggestions?", 1, 10, 5, key="count")

# --- Main Logic ---
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
            results = check_domain_availability(clean_name)
            st.session_state.domain_results[name] = results

    st.session_state.button_disabled = False

# --- Generate Button ---
st.button("🔍 Generate + Check Domain", on_click=process_generation, disabled=st.session_state.button_disabled)

csv_data = []

# --- Output Section ---
if st.session_state.generated_names:
    st.success("✅ AI Suggested Names with Domain Status:")

    for name in st.session_state.generated_names:
        label = "✨ Suggested Name" if name == st.session_state.suggested_name else ""
        header_col1, _ = st.columns([4, 1])
        with header_col1:
            st.markdown(f"### 🔹 {name} {label} <button onclick=\"navigator.clipboard.writeText('{name}')\">📋</button>", unsafe_allow_html=True)

        # Domain Status
        if name in st.session_state.domain_results:
            for domain, status in st.session_state.domain_results[name].items():
                st.markdown(f"<div style='overflow-wrap: break-word;'>- 🔗 <strong>{domain}</strong> — {status}</div>", unsafe_allow_html=True)
                csv_data.append({
                    "Name": name,
                    "Suggested": "Yes" if name == st.session_state.suggested_name else "No",
                    "Domain": domain,
                    "Status": status
                })

        # Logo Button
        if st.button(f"🎨 Generate Logo for {name}", key=f"logo_{name}"):
            st.session_state.selected_name_for_logo = name
            st.session_state.show_login_modal = True
            st.session_state.show_signup_modal = False

# --- Modal Login ---
if st.session_state.show_login_modal and not st.session_state.is_logged_in:
    st.markdown("""
    <div class="modal">
        <div class="modal-content">
            <h4>🔐 Login Required</h4>
            <form>
                <input type="text" name="username" placeholder="Username" id="username_input">
                <input type="password" name="password" placeholder="Password" id="password_input">
                <button type="submit" name="login_submit">Login</button>
            </form>
            <p style="text-align:center; margin-top:10px;">
                Don't have an account? <a href="#" onclick="parent.postMessage({ is_signup: true }, '*')">Sign up</a>
            </p>
        </div>
    </div>
    <script>
        const uname = window.parent.document.getElementById("username_input");
        if (uname) uname.focus();
    </script>
    """, unsafe_allow_html=True)

    username = st.text_input("Username (hidden)", key="login_username", label_visibility="collapsed")
    password = st.text_input("Password (hidden)", key="login_password", type="password", label_visibility="collapsed")

    if username and password:
        if username == "admin" and password == "1234":
            st.session_state.is_logged_in = True
            st.session_state.show_login_modal = False
            st.session_state.selected_name_for_logo = ""  # reset
            st.success("✅ Login successful!")
        else:
            st.error("❌ Invalid login credentials.")

# --- Modal Signup ---
if st.session_state.show_signup_modal and not st.session_state.is_logged_in:
    st.markdown("""
    <div class="modal">
        <div class="modal-content">
            <h4>📝 Create Account</h4>
            <form>
                <input type="text" name="new_username" placeholder="Choose a username" id="signup_username">
                <input type="password" name="new_password" placeholder="Choose a password" id="signup_password">
                <button type="submit" name="signup_submit">Sign Up</button>
            </form>
            <p style="text-align:center; margin-top:10px;">
                Already have an account? <a href="#" onclick="parent.postMessage({ is_login: true }, '*')">Log in</a>
            </p>
        </div>
    </div>
    <script>
        const uname = window.parent.document.getElementById("signup_username");
        if (uname) uname.focus();
    </script>
    """, unsafe_allow_html=True)

    new_username = st.text_input("Signup Username (hidden)", key="signup_username", label_visibility="collapsed")
    new_password = st.text_input("Signup Password (hidden)", key="signup_password", type="password", label_visibility="collapsed")

    if new_username and new_password:
        st.success(f"✅ Account created for {new_username}!")
        st.session_state.is_logged_in = True
        st.session_state.show_signup_modal = False
        st.session_state.show_login_modal = False
        st.session_state.selected_name_for_logo = ""

# --- Confirm & Generate Logo ---
if st.session_state.selected_name_for_logo and st.session_state.is_logged_in:
    st.markdown(f"✅ Selected name: **{st.session_state.selected_name_for_logo}**")
    if st.button("Confirm & Generate Logo"):
        st.success(f"🖼️ Logo generation feature coming soon for '{st.session_state.selected_name_for_logo}'!")

# --- CSV + PDF Download ---
if csv_data:
    df = pd.DataFrame(csv_data)
    csv = df.to_csv(index=False).encode("utf-8")

    def generate_pdf_table(keywords, data, timestamp):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        elements.append(Paragraph("AI Startup Name Suggestions", styles["Title"]))
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

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("⬇️ Download CSV", data=csv, file_name="startup_names.csv", mime="text/csv")
    with col2:
        st.download_button("⬇️ Download PDF", data=pdf_buffer, file_name="startup_names.pdf", mime="application/pdf")

    st.markdown("📂 **Note:** You can download this list of AI-generated startup names and their domain availability.")

# --- JS for Modal Switching ---
st.markdown("""
<script>
window.addEventListener("message", (event) => {
    const data = event.data;
    if (data.is_signup) {
        window.parent.location.href = "?show_signup=true";
    }
    if (data.is_login) {
        window.parent.location.href = "?show_login=true";
    }
});
</script>
""", unsafe_allow_html=True)

# --- Modal toggle from query params ---
params = st.query_params
if params.get("show_signup") == "true":
    st.session_state.show_signup_modal = True
    st.session_state.show_login_modal = False
if params.get("show_login") == "true":
    st.session_state.show_login_modal = True
    st.session_state.show_signup_modal = False
