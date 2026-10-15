"""
CropWise - ML-Based Crop Recommendation System
United Nations SDG 2: Zero Hunger | Sustainable Precision Agriculture
Author: Senior Python ML Developer
Tech Stack: Python, Streamlit, scikit-learn, pandas, numpy, matplotlib, seaborn
"""

import os
import json
import numpy as np
import pandas as pd
import streamlit as st
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from crop_info import get_crop_info, CROP_DETAILS
from generate_data import generate_dataset, CROP_PROFILES, PARAM_BOUNDS
from train_model import train_and_evaluate, FEATURE_COLS

# -----------------------------------------------------------------------------
# Streamlit App Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CropWise | SDG 2 Zero Hunger",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Green, White, and Earth-Tone Modern Palette
st.markdown("""
<style>
    /* Google Fonts & Root Theme Variables */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700&display=swap');

    :root {
        --forest-dark: #1b4332;
        --forest-green: #2d6a4f;
        --sage-green: #40916c;
        --mint-accent: #52b788;
        --mint-light: #d8f3dc;
        --earth-bg: #f8fbf8;
        --earth-sand: #f2f5f1;
        --earth-border: #d3dfd5;
        --earth-brown: #4a3525;
        --text-main: #1f2d24;
        --text-muted: #536b5c;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: var(--text-main);
    }

    /* Top Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 60%, #40916c 100%);
        color: white;
        padding: 2.2rem 2.4rem;
        border-radius: 18px;
        box-shadow: 0 10px 25px rgba(27, 67, 50, 0.18);
        margin-bottom: 1.8rem;
        position: relative;
        overflow: hidden;
    }

    .hero-banner::after {
        content: "🌾";
        position: absolute;
        right: 25px;
        bottom: -15px;
        font-size: 8rem;
        opacity: 0.12;
        pointer-events: none;
    }

    .sdg-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        color: #d8f3dc;
        padding: 4px 14px;
        border-radius: 50px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.3rem;
        font-weight: 700;
        margin: 0;
        color: #ffffff;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        color: #e2f4e8;
        font-size: 1.05rem;
        margin-top: 0.5rem;
        max-width: 850px;
        line-height: 1.5;
    }

    /* Synthetic Data Alert Banner */
    .synthetic-banner {
        background-color: #fff9e6;
        border-left: 5px solid #d4a373;
        color: #634832;
        padding: 12px 18px;
        border-radius: 8px;
        font-size: 0.88rem;
        margin-bottom: 1.6rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }

    /* Cards */
    .custom-card {
        background: #ffffff;
        border: 1px solid var(--earth-border);
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 14px rgba(45, 106, 79, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .custom-card:hover {
        box-shadow: 0 6px 18px rgba(45, 106, 79, 0.08);
    }

    .card-header {
        font-family: 'Outfit', sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--forest-dark);
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Recommended Crop Feature Card */
    .recommendation-card {
        background: linear-gradient(145deg, #ffffff 0%, #f4faf6 100%);
        border: 2px solid var(--mint-accent);
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 8px 24px rgba(82, 183, 136, 0.16);
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .crop-badge-large {
        font-size: 3.5rem;
        line-height: 1;
        margin-bottom: 0.5rem;
    }

    .crop-name-large {
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        color: var(--forest-dark);
        text-transform: capitalize;
        margin: 0.2rem 0;
    }

    .crop-scientific-name {
        font-style: italic;
        color: var(--sage-green);
        font-size: 1.05rem;
        margin-bottom: 0.8rem;
    }

    .confidence-pill {
        display: inline-block;
        background-color: var(--forest-dark);
        color: #ffffff;
        padding: 5px 16px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 0.95rem;
        margin-top: 0.4rem;
    }

    /* Metric Callout Badges */
    .metric-pill-container {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 0.8rem;
    }

    .metric-pill {
        background: #f0f7f3;
        border: 1px solid var(--mint-accent);
        border-radius: 10px;
        padding: 8px 14px;
        flex: 1;
        min-width: 130px;
        text-align: center;
    }

    .metric-pill-label {
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        font-weight: 600;
    }

    .metric-pill-value {
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--forest-dark);
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2d6a4f 0%, #1b4332 100%);
        color: white;
        font-weight: 600;
        font-size: 1.05rem;
        padding: 0.65rem 2rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 12px rgba(27, 67, 50, 0.25);
        transition: all 0.2s ease-in-out;
        width: 100%;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #40916c 0%, #2d6a4f 100%);
        box-shadow: 0 6px 16px rgba(27, 67, 50, 0.35);
        transform: translateY(-1px);
        color: white;
    }

    /* Sidebar aesthetics */
    [data-testid="stSidebar"] {
        background-color: #f7faf8;
        border-right: 1px solid #e1ebe3;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Data & Model Setup (Auto-generation & Training if missing)
# -----------------------------------------------------------------------------
DATA_DIR = "data"
MODEL_DIR = "models"
DATA_FILE = os.path.join(DATA_DIR, "crop_data.csv")
MODEL_FILE = os.path.join(MODEL_DIR, "crop_model.joblib")
METRICS_FILE = os.path.join(MODEL_DIR, "model_metrics.json")
CM_FILE = os.path.join(MODEL_DIR, "confusion_matrix.png")


def ensure_system_artifacts():
    """Ensure dataset and model exist. If not, auto-generate and train."""
    if not os.path.exists(DATA_FILE):
        with st.spinner("Initializing CropWise: Generating reproducible synthetic dataset (2,200 records)..."):
            os.makedirs(DATA_DIR, exist_ok=True)
            df = generate_dataset(samples_per_crop=100, random_seed=42)
            df.to_csv(DATA_FILE, index=False)

    if not (os.path.exists(MODEL_FILE) and os.path.exists(METRICS_FILE)):
        with st.spinner("Training Random Forest Classifier on stratified data..."):
            os.makedirs(MODEL_DIR, exist_ok=True)
            train_and_evaluate(data_path=DATA_FILE, model_output_dir=MODEL_DIR, random_seed=42)


ensure_system_artifacts()


@st.cache_resource
def load_trained_model():
    """Load cached model artifact."""
    return joblib.load(MODEL_FILE)


@st.cache_data
def load_dataset():
    """Load cached agricultural dataset."""
    return pd.read_csv(DATA_FILE)


@st.cache_data
def load_metrics():
    """Load cached test evaluation metrics."""
    with open(METRICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


model = load_trained_model()
dataset = load_dataset()
metrics = load_metrics()


# -----------------------------------------------------------------------------
# Header & Navigation
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div class="sdg-badge">🇺🇳 UN SDG 2: Zero Hunger | Target 2.4 Sustainable Agriculture</div>
    <h1 class="hero-title">CropWise — ML-Based Crop Recommendation System</h1>
    <div class="hero-subtitle">
        Empowering smallholders and agricultural planners with intelligent, data-driven crop recommendations.
        Predict optimal crops using soil macronutrients (N, P, K) and environmental parameters.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="synthetic-banner">
    <strong>⚠️ Model & Data Transparency Notice:</strong>
    This prototype utilizes <strong>synthetic agronomic data</strong> generated with realistic agronomic distributions for 22 crops.
    It is engineered for educational demonstration, research exploration, and ML benchmarking under UN SDG 2.
    It is <strong>not validated for unguided commercial farming or capital investment</strong>.
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Sidebar: Navigation & Quick Presets
# -----------------------------------------------------------------------------
st.sidebar.markdown("### 🌾 CropWise Navigator")
app_mode = st.sidebar.radio(
    "Select View:",
    [
        "🌱 Crop Recommendation Engine",
        "📊 Model Evaluation & Metrics",
        "📈 Training Dataset & Distributions",
        "🌍 SDG 2 Alignment & Ethical Framework"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Quick Ag-Presets")
st.sidebar.markdown(
    "<small style='color:#555;'>Load realistic agro-climatic conditions with a single click to test different crop scenarios:</small>",
    unsafe_allow_html=True
)

PRESETS = {
    "Custom / Manual": None,
    "🌾 Rice Paddy (Monsoon / High Rain)": {
        "N": 85, "P": 50, "K": 40, "temp": 24.5, "humidity": 83.0, "ph": 6.5, "rain": 240.0
    },
    "🍏 Apple Orchard (Cool Temperate)": {
        "N": 20, "P": 135, "K": 200, "temp": 22.0, "humidity": 92.0, "ph": 5.9, "rain": 115.0
    },
    "☕ Coffee Plantation (High Altitude)": {
        "N": 100, "P": 30, "K": 30, "temp": 25.0, "humidity": 60.0, "ph": 6.7, "rain": 165.0
    },
    "🧆 Chickpea Field (Arid / Winter)": {
        "N": 40, "P": 68, "K": 80, "temp": 19.0, "humidity": 17.0, "ph": 7.3, "rain": 80.0
    },
    "🍌 Banana Grove (Humid Tropical)": {
        "N": 102, "P": 80, "K": 50, "temp": 27.5, "humidity": 80.0, "ph": 6.0, "rain": 105.0
    },
    "🧵 Cotton Field (Warm Semi-Arid)": {
        "N": 120, "P": 45, "K": 20, "temp": 24.5, "humidity": 80.0, "ph": 6.9, "rain": 80.0
    },
    "🍉 Watermelon Patch (Warm Alluvial)": {
        "N": 100, "P": 18, "K": 50, "temp": 26.0, "humidity": 85.0, "ph": 6.5, "rain": 50.0
    }
}

selected_preset = st.sidebar.selectbox("Choose a Scenario Preset:", list(PRESETS.keys()), index=0)

# Initialize session state from preset if selected
if selected_preset != "Custom / Manual" and PRESETS[selected_preset] is not None:
    preset_data = PRESETS[selected_preset]
    st.session_state["val_n"] = preset_data["N"]
    st.session_state["val_p"] = preset_data["P"]
    st.session_state["val_k"] = preset_data["K"]
    st.session_state["val_temp"] = preset_data["temp"]
    st.session_state["val_humidity"] = preset_data["humidity"]
    st.session_state["val_ph"] = preset_data["ph"]
    st.session_state["val_rain"] = preset_data["rain"]
else:
    # Set default values if not already present
    st.session_state.setdefault("val_n", 80)
    st.session_state.setdefault("val_p", 45)
    st.session_state.setdefault("val_k", 40)
    st.session_state.setdefault("val_temp", 24.5)
    st.session_state.setdefault("val_humidity", 80.0)
    st.session_state.setdefault("val_ph", 6.5)
    st.session_state.setdefault("val_rain", 190.0)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Project Metadata:**
    - **Model:** `RandomForestClassifier` (100 trees)
    - **Supported Crops:** 22 species
    - **Test Accuracy:** `{:.2f}%`
    - **Target:** UN SDG 2 (Zero Hunger)
    """.format(metrics["accuracy"] * 100)
)


# -----------------------------------------------------------------------------
# VIEW 1: Crop Recommendation Engine
# -----------------------------------------------------------------------------
if app_mode == "🌱 Crop Recommendation Engine":
    st.markdown("### 🧪 Soil Nutrients & Environmental Conditions")
    st.markdown(
        "Enter your field's soil nutrient analysis and localized meteorological measurements below. "
        "The trained Random Forest model will evaluate the non-linear agronomic profile and predict the most suitable crop."
    )

    with st.form("recommendation_form"):
        col_soil, col_climate = st.columns(2, gap="large")

        with col_soil:
            st.markdown("""
            <div class="custom-card">
                <div class="card-header">🧪 Soil Macronutrients (NPK)</div>
                <small style="color:#666;">Essential chemical fertility indicators measured in kilograms per hectare (kg/ha).</small>
            </div>
            """, unsafe_allow_html=True)

            val_n = st.slider(
                "Nitrogen (N) [kg/ha]:",
                min_value=0,
                max_value=145,
                value=int(st.session_state["val_n"]),
                help="Crucial for vegetative leaf and shoot growth, chlorophyll synthesis, and plant vigor."
            )

            val_p = st.slider(
                "Phosphorus (P) [kg/ha]:",
                min_value=5,
                max_value=145,
                value=int(st.session_state["val_p"]),
                help="Critical for early root development, seed formation, flowering, and energy transfer (ATP)."
            )

            val_k = st.slider(
                "Potassium (K) [kg/ha]:",
                min_value=5,
                max_value=205,
                value=int(st.session_state["val_k"]),
                help="Regulates stomatal opening, drought resilience, disease defense, and fruit quality."
            )

            val_ph = st.slider(
                "Soil Reaction (pH):",
                min_value=3.5,
                max_value=9.5,
                value=float(st.session_state["val_ph"]),
                step=0.1,
                help="Governs nutrient availability. 6.0-7.5 is optimal for most agronomic crops."
            )

        with col_climate:
            st.markdown("""
            <div class="custom-card">
                <div class="card-header">🌦️ Meteorological & Environmental Factors</div>
                <small style="color:#666;">Prevailing seasonal climatic variables governing evapotranspiration and phenology.</small>
            </div>
            """, unsafe_allow_html=True)

            val_temp = st.slider(
                "Average Temperature (°C):",
                min_value=8.0,
                max_value=45.0,
                value=float(st.session_state["val_temp"]),
                step=0.5,
                help="Seasonal average temperature. Governs crop metabolic rate, thermal time, and frost risk."
            )

            val_humidity = st.slider(
                "Relative Humidity (%):",
                min_value=10.0,
                max_value=100.0,
                value=float(st.session_state["val_humidity"]),
                step=1.0,
                help="Atmospheric moisture content. High humidity supports paddy/tropical fruits; low suits pulses."
            )

            val_rain = st.slider(
                "Seasonal Rainfall (mm):",
                min_value=20.0,
                max_value=300.0,
                value=float(st.session_state["val_rain"]),
                step=1.0,
                help="Total expected seasonal precipitation or equivalent cumulative irrigation."
            )

        submit_btn = st.form_submit_button("🌱 Recommend Suitable Crop")

    # When form is submitted or on initial load
    input_features = pd.DataFrame([{
        "N": val_n,
        "P": val_p,
        "K": val_k,
        "temperature": val_temp,
        "humidity": val_humidity,
        "ph": val_ph,
        "rainfall": val_rain
    }])

    # Model inference
    prediction = model.predict(input_features)[0]
    probabilities = model.predict_proba(input_features)[0]
    classes = model.classes_

    # Sort probabilities descending
    top_indices = np.argsort(probabilities)[::-1]
    top_crop = classes[top_indices[0]]
    top_conf = probabilities[top_indices[0]] * 100.0
    crop_info = get_crop_info(top_crop)

    st.markdown("---")
    st.markdown("### 🏆 Recommendation Results")

    res_col1, res_col2 = st.columns([1.1, 1.4], gap="large")

    with res_col1:
        st.markdown(f"""
        <div class="recommendation-card">
            <div class="crop-badge-large">{crop_info['icon']}</div>
            <div class="crop-name-large">{top_crop}</div>
            <div class="crop-scientific-name">{crop_info['scientific_name']}</div>
            <div class="confidence-pill">Model Confidence: {top_conf:.1f}%</div>
            <p style="margin-top:1rem; color:#3a5a40; font-size:0.95rem; line-height:1.45;">
                {crop_info['description']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🎯 Top Candidate Crops")
        for idx in range(min(4, len(top_indices))):
            cand_crop = classes[top_indices[idx]]
            cand_conf = probabilities[top_indices[idx]] * 100.0
            cand_info = get_crop_info(cand_crop)
            col_bar1, col_bar2 = st.columns([3, 1])
            with col_bar1:
                st.write(f"{cand_info['icon']} **{cand_crop.capitalize()}**")
                st.progress(float(cand_conf) / 100.0)
            with col_bar2:
                st.markdown(f"<div style='text-align:right; font-weight:700; padding-top:8px;'>{cand_conf:.1f}%</div>", unsafe_allow_html=True)

    with res_col2:
        st.markdown("#### 📋 Agronomic Fit Analysis")
        st.markdown(
            "Comparison between your field measurements and the typical optimal agronomic profile for **{}**:".format(top_crop.capitalize())
        )

        profile = CROP_PROFILES.get(top_crop, {})
        fit_rows = []
        user_vals = {
            "N": val_n, "P": val_p, "K": val_k,
            "temperature": val_temp, "humidity": val_humidity,
            "ph": val_ph, "rainfall": val_rain
        }

        for param in FEATURE_COLS:
            user_v = user_vals[param]
            if param in profile:
                mean, std = profile[param]
                opt_range = f"{round(mean - std, 1)} – {round(mean + std, 1)}"
                diff = abs(user_v - mean)
                if diff <= std:
                    status = "✅ Highly Optimal"
                elif diff <= 2 * std:
                    status = "⚠️ Acceptable"
                else:
                    status = "❌ Deviating"
            else:
                opt_range = "N/A"
                status = "ℹ️ Normal"

            unit = "kg/ha" if param in ["N", "P", "K"] else ("°C" if param == "temperature" else ("%" if param == "humidity" else ("mm" if param == "rainfall" else "")))
            fit_rows.append({
                "Parameter": param.upper() if len(param) <= 2 else param.capitalize(),
                "Your Field Input": f"{user_v} {unit}",
                f"Ideal Range for {top_crop.capitalize()}": f"{opt_range} {unit}",
                "Agronomic Status": status
            })

        st.dataframe(pd.DataFrame(fit_rows), use_container_width=True, hide_index=True)

        st.markdown("#### 📚 Comprehensive Crop Profile")
        st.markdown(f"""
        - **Category:** {crop_info['category']}
        - **Optimal Season:** {crop_info['season']}
        - **Duration to Harvest:** {crop_info['duration']}
        - **Soil Requirements:** {crop_info['soil_type']}
        - **Water / Irrigation:** {crop_info['water_req']}
        - **Nutritional Value:** {crop_info['nutrition']}
        - **SDG 2 Impact:** {crop_info['sdg2_impact']}
        """)


# -----------------------------------------------------------------------------
# VIEW 2: Model Evaluation & Metrics
# -----------------------------------------------------------------------------
elif app_mode == "📊 Model Evaluation & Metrics":
    st.markdown("### 📊 Supervised Machine Learning Model Performance")
    st.markdown(
        "CropWise employs an actual **RandomForestClassifier** trained on 80% of data and evaluated strictly on "
        "a held-out 20% stratified test set. All metrics and figures are calculated from genuine test predictions."
    )

    # Key metric badges
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-pill">
            <div class="metric-pill-label">Test Accuracy</div>
            <div class="metric-pill-value">{metrics['accuracy'] * 100:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-pill">
            <div class="metric-pill-label">Precision (Weighted)</div>
            <div class="metric-pill-value">{metrics['precision_weighted'] * 100:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-pill">
            <div class="metric-pill-label">Recall (Weighted)</div>
            <div class="metric-pill-value">{metrics['recall_weighted'] * 100:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-pill">
            <div class="metric-pill-label">F1-Score (Weighted)</div>
            <div class="metric-pill-value">{metrics['f1_weighted'] * 100:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_cm, col_fi = st.columns([1.3, 1.0], gap="large")

    with col_cm:
        st.markdown("#### 🎯 Test Confusion Matrix")
        st.markdown(
            "Matrix showing true vs. predicted crop labels for all 440 test samples across 22 classes. "
            "Strong diagonal concentrations indicate high multi-class precision and recall."
        )

        cm_arr = np.array(metrics["confusion_matrix"])
        classes = metrics["classes"]

        fig_cm, ax_cm = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            cm_arr,
            annot=True,
            fmt="d",
            cmap="YlGn",
            xticklabels=classes,
            yticklabels=classes,
            cbar=False,
            ax=ax_cm,
            annot_kws={"size": 8}
        )
        ax_cm.set_xlabel("Predicted Crop", fontsize=10, labelpad=8)
        ax_cm.set_ylabel("Actual Crop", fontsize=10, labelpad=8)
        plt.xticks(rotation=45, ha="right", fontsize=8)
        plt.yticks(rotation=0, fontsize=8)
        plt.title(f"Test Confusion Matrix (Accuracy: {metrics['accuracy'] * 100:.2f}%)", fontsize=12, pad=12)
        plt.tight_layout()
        st.pyplot(fig_cm)
        plt.close(fig_cm)

    with col_fi:
        st.markdown("#### 🌲 Feature Importance (MDI)")
        st.markdown(
            "Mean Decrease in Impurity (Gini importance) calculated across all 100 decision trees. "
            "Highlights which environmental parameters most heavily govern crop suitability."
        )

        fi_dict = metrics["feature_importances"]
        fi_df = pd.DataFrame(list(fi_dict.items()), columns=["Feature", "Importance"])
        fi_df = fi_df.sort_values(by="Importance", ascending=True)

        fig_fi, ax_fi = plt.subplots(figsize=(8, 6.5))
        bars = ax_fi.barh(fi_df["Feature"], fi_df["Importance"], color="#2d6a4f", edgecolor="#1b4332", height=0.6)
        ax_fi.set_xlabel("Relative Importance Score", fontsize=10)
        ax_fi.set_xlim(0, max(fi_df["Importance"]) * 1.25)
        for bar in bars:
            width = bar.get_width()
            ax_fi.text(width + 0.005, bar.get_y() + bar.get_height()/2, f"{width:.3f}",
                       va="center", ha="left", fontsize=9, color="#1b4332", fontweight="bold")
        ax_fi.grid(axis="x", linestyle="--", alpha=0.3)
        plt.title("Random Forest Feature Importances", fontsize=12, pad=12)
        plt.tight_layout()
        st.pyplot(fig_fi)
        plt.close(fig_fi)

    st.markdown("#### 📑 Per-Class Detailed Classification Report")
    report_dict = metrics.get("classification_report", {})
    if report_dict:
        report_rows = []
        for cls_name in metrics["classes"]:
            if cls_name in report_dict:
                row_data = report_dict[cls_name]
                report_rows.append({
                    "Crop Class": cls_name.capitalize(),
                    "Precision": f"{row_data['precision']:.3f}",
                    "Recall": f"{row_data['recall']:.3f}",
                    "F1-Score": f"{row_data['f1-score']:.3f}",
                    "Test Support (Samples)": int(row_data['support'])
                })
        st.dataframe(pd.DataFrame(report_rows), use_container_width=True, hide_index=True)


# -----------------------------------------------------------------------------
# VIEW 3: Training Dataset & Distributions
# -----------------------------------------------------------------------------
elif app_mode == "📈 Training Dataset & Distributions":
    st.markdown("### 📈 Training Dataset Overview & Class Distributions")
    st.markdown(
        f"The training dataset comprises **{len(dataset)} synthetic agricultural records** balanced across "
        f"**{dataset['label'].nunique()} crop categories** ({len(dataset) // dataset['label'].nunique()} samples per crop). "
        "Each record reflects Gaussian agro-climatic distributions with physical boundary clipping."
    )

    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Total Records", f"{len(dataset):,}")
    d2.metric("Input Features", len(FEATURE_COLS))
    d3.metric("Crop Classes", dataset['label'].nunique())
    d4.metric("Samples per Class", len(dataset) // dataset['label'].nunique())

    st.markdown("#### 📊 Crop Class Balance Distribution")
    class_counts = dataset["label"].value_counts().reset_index()
    class_counts.columns = ["Crop", "Count"]

    fig_bar, ax_bar = plt.subplots(figsize=(12, 4))
    sns.barplot(
        data=class_counts,
        x="Crop",
        y="Count",
        palette="Greens_d",
        ax=ax_bar,
        edgecolor="#1b4332"
    )
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.ylabel("Sample Count", fontsize=10)
    plt.xlabel("Crop Category", fontsize=10)
    plt.title("Uniform Class Distribution Across 22 Agronomic Crops (Synthetic Data)", fontsize=12, pad=10)
    plt.tight_layout()
    st.pyplot(fig_bar)
    plt.close(fig_bar)

    st.markdown("#### 🔍 Feature Descriptive Statistics")
    st.dataframe(dataset[FEATURE_COLS].describe().round(2), use_container_width=True)

    st.markdown("#### 📄 Dataset Sample Records")
    st.dataframe(dataset.head(15), use_container_width=True)


# -----------------------------------------------------------------------------
# VIEW 4: SDG 2 Alignment & Ethical Framework
# -----------------------------------------------------------------------------
elif app_mode == "🌍 SDG 2 Alignment & Ethical Framework":
    st.markdown("### 🇺🇳 United Nations Sustainable Development Goal 2: Zero Hunger")

    st.markdown("""
    <div class="custom-card">
        <div class="card-header">🎯 SDG 2 Mission & Agricultural Objectives</div>
        <p>
            The overarching ambition of <strong>SDG 2</strong> is to end hunger, achieve food security and improved nutrition,
            and promote sustainable agriculture worldwide by 2030. Agriculture is the single largest employer in the world,
            providing livelihoods for 40% of today's global population. It is the largest source of income and jobs for poor rural households.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_sdg1, col_sdg2 = st.columns(2, gap="large")

    with col_sdg1:
        st.markdown("""
        <div class="custom-card">
            <div class="card-header">🌾 Target 2.4: Sustainable Agriculture</div>
            <p>
                <em>"By 2030, ensure sustainable food production systems and implement resilient agricultural practices
                that increase productivity and production, that help maintain ecosystems, that strengthen capacity
                for adaptation to climate change, extreme weather, drought, flooding and other disasters."</em>
            </p>
            <p>
                <strong>How CropWise contributes:</strong> By matching specific crops to soil chemical properties
                (N, P, K, pH) and seasonal precipitation regimes, precision agriculture minimizes crop failure risks,
                optimizes water usage, and reduces soil salinization and fertilizer run-off.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_sdg2:
        st.markdown("""
        <div class="custom-card">
            <div class="card-header">📈 Target 2.3: Smallholder Productivity</div>
            <p>
                <em>"By 2030, double the agricultural productivity and incomes of small-scale food producers,
                in particular women, indigenous peoples, family farmers, pastoralists and fishers,
                including through secure and equal access to productive resources and inputs, knowledge, financial services,
                markets and opportunities."</em>
            </p>
            <p>
                <strong>How CropWise contributes:</strong> Democratizes algorithmic agronomic decision support.
                Smallholders lacking direct access to expensive proprietary agronomy consultancies can evaluate
                crop suitability for their specific micro-plots.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="custom-card" style="border-left: 5px solid #e76f51;">
        <div class="card-header" style="color: #9c27b0;">⚠️ Project Limitations, Synthetic Data, & Ethical Constraints</div>
        <ul>
            <li><strong>Synthetic Baseline:</strong> All 2,200 training records in this prototype are generated via controlled parametric distributions. While distributions mirror known agronomic science, they do not account for localized soil microbiomes, unforeseen pest infestations, or microclimatic anomalies.</li>
            <li><strong>Advisory Nature:</strong> CropWise is designed as an educational, planning, and benchmarking tool. It must never supersede the empirical guidance of licensed agronomists, regional agricultural extension officers, or laboratory soil assays.</li>
            <li><strong>Socio-Economic Variables:</strong> Crop selection in real-world farming must consider market liquidity, cold-chain logistics, localized seed availability, and cultural consumption patterns beyond pure biophysical suitability.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #6c757d; font-size: 0.85rem; padding: 1.5rem 0;">
        <strong>CropWise — Machine Learning for Zero Hunger (SDG 2)</strong><br>
        Built with Python, Scikit-Learn, Pandas, NumPy, and Streamlit.<br>
        Developed for educational research and precision agriculture prototyping.
    </div>
    """,
    unsafe_allow_html=True
)
