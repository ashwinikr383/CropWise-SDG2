# 🌾 CropWise — ML-Based Crop Recommendation System

> **United Nations Sustainable Development Goal 2: Zero Hunger**  
> *Target 2.3: Double the agricultural productivity and incomes of small-scale food producers.*  
> *Target 2.4: Ensure sustainable food production systems and resilient agricultural practices.*

---

## 📌 Project Overview

**CropWise** is an end-to-end Machine Learning web application designed to recommend the most suitable crop for cultivation based on soil macronutrients and ambient environmental conditions. By leveraging supervised machine learning, CropWise provides data-driven decision support to optimize land productivity, reduce crop failure risks, and promote sustainable resource utilization.

### 🌟 Key Highlights
- **Supervised ML Model:** Employs a `RandomForestClassifier` trained on multi-dimensional agronomic profiles.
- **22 Supported Crops:** Rice, Maize, Chickpea, Kidney Beans, Pigeon Peas, Moth Beans, Mung Bean, Black Gram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Coffee, and Jute.
- **Genuine Evaluation:** Model metrics (Accuracy, Precision, Recall, F1-Score, Confusion Matrix, and Feature Importances) are computed strictly on held-out stratified test data.
- **Interactive Dashboard:** Built with Streamlit, styled with an earth-tone palette (forest greens, ivory, and sage accents), featuring instant scenario presets, agronomic comparison tables, and full crop profiles.
- **Zero Paid Dependencies:** Runs 100% locally with open-source Python libraries. No paid APIs or cloud dependencies required.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.9+ | Core programming runtime |
| **Machine Learning** | `scikit-learn` | `RandomForestClassifier`, stratified split, evaluation metrics |
| **Data Processing** | `pandas`, `numpy` | Dataset manipulation, synthetic distribution generation |
| **User Interface** | `Streamlit` | Interactive dashboard and recommendation interface |
| **Visualization** | `matplotlib`, `seaborn` | Confusion matrix heatmaps and feature importance charts |
| **Persistence** | `joblib`, `json` | Serializing trained model artifacts and performance metrics |

---

## 🔬 Machine Learning Pipeline

### 1. Input Features (7 Parameters)
1. **Nitrogen (N):** Essential for leafy vegetative growth and chlorophyll synthesis ($0 - 145 \text{ kg/ha}$).
2. **Phosphorus (P):** Critical for root development, flowering, and energy transfer ($5 - 145 \text{ kg/ha}$).
3. **Potassium (K):** Regulates stomata, drought tolerance, and disease defense ($5 - 205 \text{ kg/ha}$).
4. **Temperature:** Ambient seasonal mean temperature ($8.0 - 45.0 ^\circ\text{C}$).
5. **Relative Humidity:** Atmospheric moisture content ($10.0 - 100.0\%$).
6. **Soil pH:** Acidity/alkalinity of the soil solution ($3.5 - 9.5$).
7. **Rainfall:** Cumulative seasonal precipitation / irrigation ($20.0 - 300.0\text{ mm}$).

### 2. Synthetic Data Generation (`generate_data.py`)
- Generates **2,200 reproducible records** ($100$ records per crop across $22$ classes).
- Built on agronomic centroids derived from international agricultural literature with realistic variance (Gaussian standard deviations) and physical boundary clipping.
- Deterministic with a fixed seed (`seed=42`).
- Explicitly tagged as synthetic data to preserve scientific integrity.

### 3. Model Training & Evaluation (`train_model.py`)
- **Split:** $80\%$ Training ($1,760$ samples), $20\%$ Test ($440$ samples), stratified across all 22 classes.
- **Algorithm:** `RandomForestClassifier(n_estimators=100, max_depth=16, random_state=42)`.
- **Outputs Saved:**
  - `models/crop_model.joblib`: Serialized trained model.
  - `models/model_metrics.json`: Un-hardcoded test metrics, confusion matrix array, and classification report.
  - `models/confusion_matrix.png`: High-resolution heatmap of test set predictions.

---

## 📂 Project Directory Structure

```
CropWise_SDG2_New/
├── app.py                  # Main Streamlit web application & dashboard
├── crop_info.py            # Agronomic metadata, nutritional values, & SDG 2 profiles
├── generate_data.py        # Synthetic dataset generator (2,200 records)
├── train_model.py          # Model training, test evaluation, and metrics exporter
├── requirements.txt        # Python dependency manifest
├── run_app.bat             # Windows one-click automated execution script
├── README.md               # Comprehensive project documentation
├── data/
│   └── crop_data.csv       # Generated dataset (auto-created if missing)
└── models/
    ├── crop_model.joblib   # Trained Random Forest model (auto-created)
    ├── model_metrics.json  # Genuine test performance metrics (auto-created)
    └── confusion_matrix.png# Confusion matrix visual chart (auto-created)
```

---

## 🚀 Quickstart Guide

### Option A: One-Click Launch (Windows)
Double-click `run_app.bat` or execute in Windows Command Prompt:
```cmd
run_app.bat
```
*This batch script automatically verifies/creates a virtual environment (`.venv`), installs requirements, generates data, trains the model, and launches Streamlit.*

### Option B: Manual Terminal Execution
```bash
# 1. (Optional) Create and activate a virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate the reproducible dataset (2,200 records)
python generate_data.py

# 4. Train the Random Forest model and compute test metrics
python train_model.py

# 5. Launch the Streamlit application
streamlit run app.py
```

---

## 🖥️ Streamlit Application Features

1. **🌱 Crop Recommendation Engine:**
   - Sliders with agronomic tooltips for all 7 soil and climate inputs.
   - Quick-select scenario presets (Rice Paddy, Apple Orchard, Coffee Plantation, Chickpea Dryland, etc.).
   - Prediction card with top crop, confidence percentage, and alternative candidates.
   - Agronomic Fit Analysis table comparing input values against optimal bounds.
   - Detailed Crop Information card covering harvesting time, soil type, water requirement, nutritional profile, and SDG 2 impact.

2. **📊 Model Evaluation & Metrics:**
   - Real calculated test metrics (Accuracy, Precision, Recall, F1-Score).
   - Test confusion matrix heatmap.
   - Random Forest Feature Importance chart (MDI).
   - Complete per-class classification table.

3. **📈 Training Dataset & Distributions:**
   - Summary statistics and dataset preview.
   - Class balance chart proving uniform representation across all 22 crops.

4. **🌍 SDG 2 Alignment & Ethical Framework:**
   - Detailed breakdown of UN SDG 2 Targets 2.3 and 2.4.
   - Why precision agriculture prevents nutrient overuse and safeguards rural livelihoods.
   - Transparent prototype limitations notice.

---

## ⚠️ Limitations & Ethical Disclaimer

1. **Synthetic Data:** The dataset is generated synthetically to model real-world agronomic centroids and variations without requiring proprietary datasets. It is not field-collected empirical data.
2. **Prototype Advisory Only:** CropWise is intended as an educational, decision-support, and research prototyping tool. It must **not** replace on-site chemical soil laboratory testing, certified agricultural extension officer consultations, or local micro-climatic assessments for commercial farming investments.
3. **Socio-Economic Factors:** Practical farming decisions must also incorporate localized market prices, seed availability, storage infrastructure, and labor dynamics.

---

## 📜 License
Developed under open educational research principles in support of **UN Sustainable Development Goal 2: Zero Hunger**.
