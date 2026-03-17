'''import streamlit as st
import pandas as pd
import numpy as np
import requests
import joblib

# ------------------ Config ------------------ #
st.set_page_config(page_title="Smart Intrusion Detection", layout="centered")

FEATURE_DEFAULTS_PATH = 'feature_defaults.pkl'
FEATURE_NAMES_PATH = 'feature_names.pkl'
API_URL = "http://localhost:8000/predict"

# ------------------ Load Data ------------------ #
feature_defaults = np.array(joblib.load(FEATURE_DEFAULTS_PATH))
feature_names = joblib.load(FEATURE_NAMES_PATH)

# ------------------ Custom Dark Theme Styling ------------------ #
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }

        .stApp {
            background-color: #121212;
            color: #f5f5f5;
        }

        .css-18e3th9 {
            background-color: #1e1e1e;
        }

        .stButton>button {
            background-color: #0066cc;
            color: white;
            border-radius: 6px;
            padding: 10px 20px;
            border: none;
            font-weight: bold;
        }

        .stFileUploader {
            background-color: #1e1e1e;
            border: 1px dashed #444;
            padding: 1rem;
            border-radius: 10px;
        }

        .result-card {
            background-color: #2b2b2b;
            padding: 15px;
            margin: 10px 0;
            border-left: 6px solid #00bfa5;
            border-radius: 10px;
            box-shadow: 2px 2px 5px #00000033;
        }

        .result-card.danger {
            border-left: 6px solid #ff4d4d;
        }

        .footer {
            margin-top: 2rem;
            font-size: 0.85rem;
            text-align: center;
            color: #888;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------ Header ------------------ #
st.markdown("## 🛡️ Smart Intrusion Detection Dashboard")
st.markdown("Upload a KDD-format CSV log file to detect potential threats using ML.")

# ------------------ File Upload ------------------ #
uploaded_file = st.file_uploader("📂 Upload your `raw_log.csv` file here:", type="csv")

# ------------------ If File Uploaded ------------------ #
if uploaded_file:
    st.markdown("### 🔍 Raw Log Preview:")
    df = pd.read_csv(uploaded_file)
    st.dataframe(df, use_container_width=True)

    st.info("⚙️ Preprocessing: Filling missing values using defaults...")

    # Fill missing values with defaults
    for col in df.columns:
        if col in feature_names:
            idx = feature_names.index(col)
            df[col] = df[col].fillna(feature_defaults[idx])

    st.success("✅ Missing values handled. Preparing to send data to the backend...")

    entries = df.to_dict(orient='records')
    predictions = []

    # Progress
    progress_bar = st.progress(0)
    total = len(entries)

    for idx, entry in enumerate(entries, 1):
        try:
            # Clean each record
            clean_entry = {k: (None if pd.isna(v) else v) for k, v in entry.items()}
            response = requests.post(API_URL, json=clean_entry)

            if response.status_code == 200:
                result = response.json()[0]
                predictions.append(result)

                # Render prediction card
                result_style = "danger" if result['attack_detected'] else ""
                st.markdown(f"""
                    <div class="result-card {result_style}">
                        <strong>Entry {idx}</strong><br>
                        <b>Prediction:</b> {result['prediction']}<br>
                        <b>Attack Detected:</b> {"🟥 Yes" if result['attack_detected'] else "🟩 No"}<br>
                        <b>Confidence:</b> {result['confidence']}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"❌ Entry {idx} failed with status code {response.status_code}")

        except Exception as e:
            st.error(f"⚠️ Error in Entry {idx}: {e}")

        progress_bar.progress(idx / total)

    if predictions:
        st.success(f"🎉 All entries processed: {len(predictions)} total.")

        # Optional: Summary Stats
        attack_count = sum([1 for p in predictions if p['attack_detected']])
        st.markdown("---")
        st.subheader("📊 Summary")
        st.markdown(f"**Total entries:** {len(predictions)}")
        st.markdown(f"**Total attacks detected:** {attack_count}")
        st.markdown(f"**Normal entries:** {len(predictions) - attack_count}")

# ------------------ Footer ------------------ #
st.markdown('<div class="footer">Developed with ❤️ using Streamlit</div>', unsafe_allow_html=True)'''



import streamlit as st
import pandas as pd
import numpy as np
import requests
import joblib

# ------------------ Config ------------------ #
st.set_page_config(page_title="Smart IDS", layout="wide")

FEATURE_DEFAULTS_PATH = 'feature_defaults.pkl'
FEATURE_NAMES_PATH = 'feature_names.pkl'
API_URL = "http://localhost:8000/predict"

# ------------------ Load Data ------------------ #
feature_defaults = np.array(joblib.load(FEATURE_DEFAULTS_PATH))
feature_names = joblib.load(FEATURE_NAMES_PATH)

# ------------------ Styling ------------------ #
st.markdown("""
<style>
.stApp {
    background: #0e1117;
    color: #e6edf3;
}

.header-box {
    background: linear-gradient(90deg, #0066cc, #00bfa5);
    padding: 20px;
    border-radius: 12px;
    color: white;
    margin-bottom: 20px;
}

.result-card {
    background-color: #1e1e1e;
    padding: 18px;
    margin: 12px 0;
    border-radius: 12px;
    border-left: 6px solid #00bfa5;
    box-shadow: 0 4px 10px rgba(0,0,0,0.4);
}

.result-card.danger {
    border-left: 6px solid #ff4d4d;
}

.metric-box {
    background-color: #1e1e1e;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

.footer {
    margin-top: 40px;
    text-align: center;
    color: #888;
}
</style>
""", unsafe_allow_html=True)

# ------------------ Header ------------------ #
st.markdown("""
<div class="header-box">
<h2>🛡️ Smart Intrusion Detection System</h2>
<p>Detect malicious network activity using Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# ------------------ File Upload ------------------ #
uploaded_file = st.file_uploader("📂 Upload your network log CSV", type="csv")

# ------------------ If File Uploaded ------------------ #
if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Raw Log Preview")
    st.dataframe(df, use_container_width=True)

    st.info("⚙️ Preprocessing data...")

    # Fill missing values
    for col in df.columns:
        if col in feature_names:
            idx = feature_names.index(col)
            df[col] = df[col].fillna(feature_defaults[idx])

    st.success("✅ Data ready for prediction")

    entries = df.to_dict(orient='records')
    predictions = []

    progress_bar = st.progress(0)
    total = len(entries)

    st.subheader("🚀 Predictions")

    for idx, entry in enumerate(entries, 1):
        try:
            clean_entry = {k: (None if pd.isna(v) else v) for k, v in entry.items()}
            response = requests.post(API_URL, json=clean_entry)

            if response.status_code == 200:
                result = response.json()[0]
                predictions.append(result)

                result_style = "danger" if result['attack_detected'] else ""

                st.markdown(f"""
                <div class="result-card {result_style}">
                    <h4>Entry {idx}</h4>
                    <p><b>Prediction:</b> {result['prediction']}</p>
                    <p><b>Attack:</b> {"🔴 Yes" if result['attack_detected'] else "🟢 No"}</p>
                    <p><b>Confidence:</b> {result['confidence']}</p>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.error(f"Entry {idx} failed ({response.status_code})")

        except Exception as e:
            st.error(f"Error in Entry {idx}: {e}")

        progress_bar.progress(idx / total)

    # ------------------ Summary Dashboard ------------------ #
    if predictions:
        attack_count = sum([1 for p in predictions if p['attack_detected']])
        normal_count = len(predictions) - attack_count

        st.markdown("---")
        st.subheader("📊 Summary Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.markdown(f"""
        <div class="metric-box">
        <h3>{len(predictions)}</h3>
        <p>Total Entries</p>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="metric-box">
        <h3 style="color:#ff4d4d;">{attack_count}</h3>
        <p>Attacks Detected</p>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div class="metric-box">
        <h3 style="color:#00bfa5;">{normal_count}</h3>
        <p>Normal Traffic</p>
        </div>
        """, unsafe_allow_html=True)

# ------------------ Footer ------------------ #
st.markdown('<div class="footer">Built using Streamlit • ML Powered IDS</div>', unsafe_allow_html=True)