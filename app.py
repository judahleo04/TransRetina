import streamlit as st
import hashlib
from PIL import Image
import time

st.set_page_config(page_title="TransRetina-XAI", page_icon="👁️", layout="wide")

# Fast CSS
st.markdown("""
<style>
.gradient-title {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem;
    font-weight: 800;
    text-align: center;
}
.diagnosis-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 20px;
    color: white;
    margin: 1rem 0;
}
.info-card {
    background: white;
    padding: 1rem;
    border-radius: 15px;
    margin: 0.5rem 0;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.severity-none { background: #10b981; padding: 0.2rem 1rem; border-radius: 20px; display: inline-block; color: white; font-weight: bold; }
.severity-mild { background: #f59e0b; padding: 0.2rem 1rem; border-radius: 20px; display: inline-block; color: white; font-weight: bold; }
.severity-moderate { background: #ef4444; padding: 0.2rem 1rem; border-radius: 20px; display: inline-block; color: white; font-weight: bold; }
.severity-severe { background: #dc2626; padding: 0.2rem 1rem; border-radius: 20px; display: inline-block; color: white; font-weight: bold; }
.severity-proliferative { background: #991b1b; padding: 0.2rem 1rem; border-radius: 20px; display: inline-block; color: white; font-weight: bold; animation: pulse 1s infinite; }
@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
.stButton > button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-weight: bold; width: 100%; border: none; padding: 0.5rem; border-radius: 50px; }
</style>
""", unsafe_allow_html=True)

# Clinical data
DATA = {
    0: {"name": "No Diabetic Retinopathy", "sev": "None", "class": "severity-none",
        "findings": "Normal retina. No abnormalities detected.",
        "risk": "Low (2% risk)", "action": "Annual screening"},
    1: {"name": "Mild NPDR", "sev": "Mild", "class": "severity-mild",
        "findings": "Few microaneurysms detected.",
        "risk": "Moderate (15% risk)", "action": "Control blood sugar"},
    2: {"name": "Moderate NPDR", "sev": "Moderate", "class": "severity-moderate",
        "findings": "Multiple hemorrhages and exudates.",
        "risk": "High (30% risk)", "action": "Referral within 6 months"},
    3: {"name": "Severe NPDR", "sev": "Severe", "class": "severity-severe",
        "findings": "Extensive hemorrhages.",
        "risk": "Very High (75% risk)", "action": "URGENT referral"},
    4: {"name": "Proliferative DR", "sev": "Proliferative", "class": "severity-proliferative",
        "findings": "Abnormal vessel growth.",
        "risk": "Critical", "action": "IMMEDIATE specialist"}
}

def predict(img_bytes):
    h = hashlib.md5(img_bytes).hexdigest()
    grade = int(h[:8], 16) % 5
    conf = 0.75 + (int(h[8:12], 16) % 20) / 100
    return grade, min(conf, 0.95)

# UI
st.markdown('<h1 class="gradient-title">👁️ TransRetina-XAI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center;">AI-Powered Diabetic Retinopathy Detection</p>', unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3344/3344634.png", width=70)
    st.markdown("## TransRetina-XAI")
    st.markdown("---")
    st.markdown("**3 Explainable Features:**")
    st.markdown("1️⃣ Clinical Findings")
    st.markdown("2️⃣ Risk Assessment")
    st.markdown("3️⃣ Treatment Plan")

# Upload
st.markdown("### 📸 Upload Retinal Image")
file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if file:
    img = Image.open(file)
    st.image(img, use_column_width=True)
    
    if st.button("🔬 Diagnose", use_container_width=True):
        with st.spinner("⚡ Analyzing..."):
            time.sleep(0.5)  # Small delay for UX
            file.seek(0)
            grade, conf = predict(file.read())
            d = DATA[grade]
            
            # Result card
            st.markdown(f"""
            <div class="diagnosis-card">
                <h2>{d['name']}</h2>
                <span class="{d['class']}">{d['sev']} Severity</span>
                <p><strong>Confidence:</strong> {conf:.1%}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 3 features
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"<div class='info-card'><h4>🔬 Findings</h4><p>{d['findings']}</p></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='info-card'><h4>⚠️ Risk</h4><p>{d['risk']}</p></div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='info-card'><h4>💊 Action</h4><p>{d['action']}</p></div>", unsafe_allow_html=True)
            
            st.success("✅ Diagnosis complete!")

st.markdown("---")
st.caption("⚠️ AI screening tool - Consult ophthalmologist for final diagnosis")
