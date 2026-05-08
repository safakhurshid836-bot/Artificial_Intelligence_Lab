#python -m pip install scikit-learn
# python -m pip install streamlit
# python -m streamlit run "Exoplanet Detection Project\app\streamlit_app.py"
import streamlit as st
import numpy as np
import pandas as pd
import pickle
import os
import shap
import matplotlib.pyplot as plt

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="NASA's Real Dataset Based Exoplanet Intelligence System",
    page_icon="🌌",
    layout="wide"
)

# =========================
# UI STYLE
# =========================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #020617, #000000);
    color: white;
}
h1, h2, h3 {
    color: #38bdf8;
}
.stButton>button {
    background: linear-gradient(90deg,#06b6d4,#6366f1);
    color:white;
    border-radius:10px;
    height:3em;
    width:100%;
}
img {
    filter: drop-shadow(0px 0px 8px rgba(56,189,248,0.6));
}
</style>
""", unsafe_allow_html=True)

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "..", "models", "rf_model.pkl")
logo_path = os.path.join(BASE_DIR, "nasa-logo.png")  # match your file name

# =========================
# LOAD MODEL
# =========================
model = pickle.load(open(model_path, "rb"))
explainer = shap.TreeExplainer(model)

feature_names = [
    "koi_period","koi_duration","koi_depth","koi_prad",
    "koi_teq","koi_insol","koi_model_snr","koi_steff",
    "koi_slogg","koi_srad","koi_kepmag"
]

# =========================
# HEADER WITH LOGO
# =========================
col1, col2 = st.columns([1, 6])

with col1:
    if os.path.exists(logo_path):
        st.image(logo_path, width=90)

with col2:
    st.markdown("""
    <h1 style='margin-bottom:0;'>🌌 NASA's Real Dataset Based Exoplanet Intelligence System</h1>
    <p style='color:#94a3b8;'>Predict • Explain • Analyze</p>
    <p style='color:lime; font-weight:bold;'>Model Accuracy: 90.45%</p>
    """, unsafe_allow_html=True)

# =========================
# DISCLAIMER (UI)
# =========================
st.markdown("""
<div style="
    margin-top:10px;
    padding:10px;
    border-radius:8px;
    background-color: rgba(255,255,255,0.05);
    border: 1px solid rgba(56,189,248,0.3);
    font-size:14px;
    color:#cbd5f5;
">
⚠️ <b>Disclaimer:</b> This is an academic project developed for an AI Lab (Semester 3) as part of a BS Artificial Intelligence program. 
It is <b>not affiliated with or endorsed by NASA</b>, and predictions are for educational purposes only.
</div>
""", unsafe_allow_html=True)

# =========================
# INPUT
# =========================
def get_float(label):
    val = st.text_input(label)
    try:
        return float(val)
    except:
        return None

st.markdown("## 🔭 Input Parameters")

col1, col2 = st.columns(2)

with col1:
    koi_period    = get_float("Orbital Period")
    koi_duration  = get_float("Transit Duration")
    koi_depth     = get_float("Transit Depth")
    koi_prad      = get_float("Planet Radius")
    koi_teq       = get_float("Equilibrium Temperature")

with col2:
    koi_insol     = get_float("Insolation Flux")
    koi_model_snr = get_float("Signal-to-Noise Ratio")
    koi_steff     = get_float("Stellar Temperature")
    koi_slogg     = get_float("Surface Gravity")
    koi_srad      = get_float("Stellar Radius")
    koi_kepmag    = get_float("Kepler Magnitude")

features = [
    koi_period, koi_duration, koi_depth, koi_prad,
    koi_teq, koi_insol, koi_model_snr, koi_steff,
    koi_slogg, koi_srad, koi_kepmag
]

# =========================
# PREDICTION
# =========================
if st.button("🚀 Analyze Exoplanet"):

    if None in features:
        st.error("⚠️ Please fill all fields correctly.")
    else:

        X = pd.DataFrame([features], columns=feature_names)

        pred = model.predict(X)[0]
        prob = model.predict_proba(X)[0]

        result = "CONFIRMED" if pred == 1 else "FALSE POSITIVE"
        confidence = max(prob) * 100

        st.subheader(f"Result: {result} ({confidence:.2f}%)")

        # Probability chart
        prob_df = pd.DataFrame({
            "Class": ["False Positive", "Confirmed"],
            "Probability": prob
        })
        st.bar_chart(prob_df.set_index("Class"))

        # Feature importance
        imp_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": model.feature_importances_
        }).sort_values(by="Importance", ascending=False)
        st.bar_chart(imp_df.set_index("Feature"))

        # =========================
        # SHAP
        # =========================
        shap_values = explainer.shap_values(X)

        if isinstance(shap_values, list):
            shap_vec = shap_values[1][0]
            base_value = explainer.expected_value[1]
        else:
            shap_vec = shap_values[0][0]
            base_value = explainer.expected_value

        shap_vec = np.array(shap_vec).reshape(-1)
        base_value = np.array(base_value).reshape(-1)[0]

        explanation = shap.Explanation(
            values=shap_vec,
            base_values=base_value,
            data=X.iloc[0].values,
            feature_names=feature_names
        )

        st.markdown("### 📊 SHAP Waterfall")

        fig, ax = plt.subplots()
        shap.plots.waterfall(explanation, show=False)

        plt.savefig("shap_plot.png", bbox_inches="tight", dpi=200)
        st.pyplot(fig)
        plt.close()

        # =========================
        # PDF REPORT
        # =========================
        pdf_file = "exoplanet_report.pdf"
        doc = SimpleDocTemplate(pdf_file)
        styles = getSampleStyleSheet()

        story = []

        # Logo
        if os.path.exists(logo_path):
            story.append(Image(logo_path, width=80, height=80))

        story.append(Spacer(1, 12))

        # Title
        story.append(Paragraph("Exoplanet Prediction Report", styles["Title"]))
        story.append(Spacer(1, 12))

        # Result
        story.append(Paragraph(f"Result: {result}", styles["Normal"]))
        story.append(Paragraph(f"Confidence: {confidence:.2f}%", styles["Normal"]))
        story.append(Spacer(1, 12))

        # SHAP Image
        story.append(Paragraph("SHAP Explainability:", styles["Heading2"]))
        story.append(Spacer(1, 10))
        story.append(Image("shap_plot.png", width=500, height=300))
        story.append(Spacer(1, 12))

        # DISCLAIMER IN PDF
        story.append(Paragraph(
            "Disclaimer: This is an academic project developed for an AI Lab (Semester 3) "
            "as part of a BS Artificial Intelligence program. It is not affiliated with or "
            "endorsed by NASA. Predictions are for educational purposes only.",
            styles["Normal"]
        ))

        doc.build(story)

        with open(pdf_file, "rb") as f:
            st.download_button(
                "📄 Download Full PDF Report",
                f,
                file_name="exoplanet_report.pdf"
            )