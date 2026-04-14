import streamlit as st
import numpy as np
import tensorflow as tf
import cv2
from PIL import Image
import plotly.graph_objects as go

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="TransRetina-XAI",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("🧠 TransRetina-XAI")
st.markdown("### Diabetic Retinopathy Detection with Explainable AI")

# -----------------------------
# LOAD TRAINED MODEL
# -----------------------------
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("dr_model.h5")
    return model

model = load_model()

# -----------------------------
# CLASS LABELS
# -----------------------------
classes = [
    "No DR",
    "Mild",
    "Moderate",
    "Severe",
    "Proliferative DR"
]

# -----------------------------
# EXPLANATION (XAI)
# -----------------------------
def get_explanation(class_id):
    explanations = {
        0: "No Diabetic Retinopathy detected. Retina appears normal.",
        1: "Mild DR detected due to small microaneurysms.",
        2: "Moderate DR with visible lesions and hemorrhages.",
        3: "Severe DR with abnormal blood vessel growth.",
        4: "Proliferative DR, high risk of vision loss."
    }
    return explanations[class_id]

# -----------------------------
# IMAGE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("📸 Upload Retinal Image", type=["jpg","png","jpeg"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    col1, col2 = st.columns(2)

    # -----------------------------
    # SHOW IMAGE
    # -----------------------------
    with col1:
        st.image(img, caption="Uploaded Image", use_column_width=True)

    # -----------------------------
    # PREDICTION
    # -----------------------------
    img_resized = cv2.resize(img, (224,224))
    img_resized = img_resized / 255.0
    img_resized = np.expand_dims(img_resized, axis=0)

    preds = model.predict(img_resized)
    class_id = int(np.argmax(preds))
    confidence = float(np.max(preds))
    all_probs = preds[0]

    # -----------------------------
    # OUTPUT
    # -----------------------------
    with col2:
        st.subheader("📊 Prediction Result")
        st.success(f"{classes[class_id]}")
        st.info(f"Confidence: {confidence:.2f}")

        st.subheader("🧠 Explanation")
        st.write(get_explanation(class_id))

        # Risk level
        st.subheader("⚠️ Risk Level")
        if class_id == 0:
            st.success("Low Risk")
        elif class_id in [1,2]:
            st.warning("Medium Risk")
        else:
            st.error("High Risk")

        # Confidence bar
        st.progress(confidence)

    # -----------------------------
    # PROBABILITY CHART
    # -----------------------------
    st.subheader("📊 Probability Distribution")

    fig = go.Figure(data=[
        go.Bar(
            x=classes,
            y=all_probs,
            text=[f"{p:.2f}" for p in all_probs],
            textposition='auto'
        )
    ])

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("⚠️ This is an AI-assisted tool. Consult a doctor for final diagnosis.")
