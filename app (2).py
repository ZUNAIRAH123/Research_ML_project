# app.py - BEAUTIFUL FINAL VERSION
import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os

st.set_page_config(
    page_title="Research Rank Predictor",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0f1e;
    color: #e8eaf0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1528 0%, #111827 100%);
    border-right: 1px solid rgba(99,179,237,0.15);
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 18px 0 10px 0;
    margin-bottom: 6px;
}
.sidebar-logo .icon {
    font-size: 32px;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sidebar-logo .brand {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}
.sidebar-logo .sub {
    font-size: 10px;
    color: #64748b !important;
    font-weight: 400;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.sidebar-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,179,237,0.3), transparent);
    margin: 14px 0;
}

.section-label {
    font-size: 9px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #475569 !important;
    font-weight: 600;
    margin: 18px 0 8px 0;
    padding-left: 2px;
}

/* Number inputs */
[data-testid="stNumberInput"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(99,179,237,0.15) !important;
    border-radius: 10px !important;
    transition: border-color 0.2s;
}
[data-testid="stNumberInput"] > div:focus-within {
    border-color: rgba(56,189,248,0.5) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.08) !important;
}
[data-testid="stNumberInput"] input {
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
}
[data-testid="stNumberInput"] label {
    font-size: 11.5px !important;
    color: #94a3b8 !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px;
}

/* Predict button */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.4) !important;
    margin-top: 10px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(99,102,241,0.6) !important;
}

/* ── Main content ── */
.hero-section {
    padding: 48px 0 32px 0;
    position: relative;
}
.hero-tag {
    display: inline-block;
    background: rgba(56,189,248,0.1);
    border: 1px solid rgba(56,189,248,0.25);
    color: #38bdf8;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(32px, 5vw, 54px);
    font-weight: 800;
    line-height: 1.1;
    color: #f1f5f9;
    margin-bottom: 16px;
}
.hero-title span {
    background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 16px;
    color: #64748b;
    font-weight: 400;
    max-width: 540px;
    line-height: 1.7;
}

/* Stats row */
.stats-row {
    display: flex;
    gap: 20px;
    margin: 32px 0;
    flex-wrap: wrap;
}
.stat-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 18px 24px;
    flex: 1;
    min-width: 140px;
    transition: border-color 0.3s;
}
.stat-card:hover { border-color: rgba(56,189,248,0.3); }
.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-label {
    font-size: 11px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 4px;
    font-weight: 600;
}

/* Divider line */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(56,189,248,0.3), rgba(129,140,248,0.3), transparent);
    margin: 30px 0;
}

/* Result card */
.result-card {
    background: linear-gradient(135deg, rgba(14,165,233,0.12) 0%, rgba(99,102,241,0.12) 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 24px;
    padding: 48px 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.6s ease;
}
.result-card::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,102,241,0.15), transparent 70%);
    border-radius: 50%;
}
.result-card::after {
    content: '';
    position: absolute;
    bottom: -60px; left: -60px;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(56,189,248,0.12), transparent 70%);
    border-radius: 50%;
}
.result-label {
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #64748b;
    font-weight: 600;
    margin-bottom: 16px;
}
.result-value {
    font-family: 'Syne', sans-serif;
    font-size: 72px;
    font-weight: 800;
    background: linear-gradient(135deg, #38bdf8, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
    margin-bottom: 16px;
    position: relative;
    z-index: 1;
}
.result-note {
    font-size: 13px;
    color: #475569;
    font-weight: 400;
}
.result-badge {
    display: inline-block;
    background: rgba(16,185,129,0.15);
    border: 1px solid rgba(16,185,129,0.3);
    color: #10b981;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 16px;
    border-radius: 20px;
    margin-top: 16px;
    letter-spacing: 0.5px;
}

/* Idle state card */
.idle-card {
    background: rgba(255,255,255,0.02);
    border: 1px dashed rgba(255,255,255,0.1);
    border-radius: 24px;
    padding: 60px 40px;
    text-align: center;
}
.idle-icon {
    font-size: 48px;
    margin-bottom: 16px;
    opacity: 0.4;
}
.idle-text {
    font-size: 15px;
    color: #334155;
    font-weight: 400;
}

/* Input summary table */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
}
[data-testid="stExpander"] summary {
    color: #64748b !important;
    font-size: 13px !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Load artifacts ──
@st.cache_resource
def load_artifacts():
    try:
        with open('regression_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open('feature_names.pkl', 'rb') as f:
            feature_names = pickle.load(f)
        return model, scaler, feature_names
    except FileNotFoundError as e:
        st.error(f"❌ File nahi mili: {e}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.stop()

model, scaler, feature_names = load_artifacts()

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="icon">🔬</div>
        <div>
            <div class="brand">ResearchRank</div>
            <div class="sub">AI Predictor</div>
        </div>
    </div>
    <div class="sidebar-divider"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">📊 Feature Inputs</div>', unsafe_allow_html=True)

    user_inputs = {}
    for col in feature_names:
        user_inputs[col] = st.number_input(
            label=col,
            value=0.0,
            format="%.4f",
            help=f"Enter value for: {col}"
        )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    predict_button = st.button("⚡  PREDICT NOW", use_container_width=True)

    st.markdown(f"""
    <div style="margin-top:24px; padding:14px; background:rgba(56,189,248,0.06);
         border:1px solid rgba(56,189,248,0.15); border-radius:12px;">
        <div style="font-size:10px; letter-spacing:2px; color:#475569; text-transform:uppercase; margin-bottom:8px; font-weight:600;">Model Info</div>
        <div style="font-size:12px; color:#64748b; line-height:1.8;">
            🧠 Linear Regression<br>
            📐 {len(feature_names)} Features<br>
            🎯 R² Score: 0.9684
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Main ──
st.markdown("""
<div class="hero-section">
    <div class="hero-tag">AI · Regression Analysis</div>
    <div class="hero-title">Research Ranking<br><span>Predictor</span></div>
    <div class="hero-sub">
        Enter citation and publication metrics to predict a researcher's normalized global ranking using our trained regression model.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-value">96.8%</div>
        <div class="stat-label">R² Accuracy</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">6,335</div>
        <div class="stat-label">Training Rows</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">16</div>
        <div class="stat-label">Features Used</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">Linear</div>
        <div class="stat-label">Model Type</div>
    </div>
</div>
<div class="section-divider"></div>
""", unsafe_allow_html=True)

result_placeholder = st.empty()

if predict_button:
    try:
        input_df = pd.DataFrame([user_inputs])[feature_names]
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0]

        with result_placeholder.container():
            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">Predicted Rank (ns)</div>
                <div class="result-value">{prediction:,.2f}</div>
                <div class="result-note">Normalized global researcher ranking based on citation metrics</div>
                <div class="result-badge">✓ Prediction Successful</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("📋 Input Summary dekho"):
                summary_df = pd.DataFrame(
                    list(user_inputs.items()),
                    columns=["Feature", "Value"]
                )
                st.dataframe(summary_df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"❌ Prediction error: {str(e)}")

else:
    with result_placeholder.container():
        st.markdown("""
        <div class="idle-card">
            <div class="idle-icon">📡</div>
            <div class="idle-text">Sidebar mein values enter karein<br>aur <strong style="color:#38bdf8;">Predict Now</strong> click karein</div>
        </div>
        """, unsafe_allow_html=True)
