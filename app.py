import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# ==========================================
# 1. PREMIUM BRANDING & SITE TITLE SETTINGS
# ==========================================
st.set_page_config(
    page_title="MergerFlow Global // M&A Target Intelligence Platform",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. GOOGLE ANALYTICS INTEGRATION
# ==========================================
GA_TRACKING_ID = "G-HJPZDZB5KE" 

ga_html = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_TRACKING_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GA_TRACKING_ID}');
    </script>
"""
st.html(ga_html) # Injects the tracking snippet seamlessly in the background

# ==========================================
# 3. HIDE CODE & PREMIUM INTERFACE CSS
# ==========================================
hide_styles = """
    <style>
    /* Vanishes the top header bar, GitHub icons, and "View Code" button */
    header {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    
    /* FIX FOR DARK MODE NUMBERS: Forces absolute high-contrast text color */
    div[data-testid="stMetricValue"] {
        color: #00FFCC !important; /* Premium high-contrast neon teal for dark mode */
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
    }
    </style>
"""
st.markdown(hide_styles, unsafe_allow_html=True)

# ==========================================
# 4. INITIAL REVEAL LOADING SEQUENCER
# ==========================================
if "initialized" not in st.session_state:
    # Shows a professional enterprise loading state the very first time it boots up
    with st.spinner("Initializing MergerFlow Algorithmic Core System..."):
        time.sleep(1.8) # Gives a realistic enterprise pipeline loading feel
    st.session_state["initialized"] = True

# ==========================================
# 5. HEADER ZONE & USER BRANDING
# ==========================================
st.title("🌐 MergerFlow Global")
st.subheader("Enterprise M&A Valuation & Target Screening Analytics")
st.caption("Engineered by **Anchita Duggal** | Corporate Development Pipeline Tool")
st.markdown("---")

# ==========================================
# 6. APP SIDEBAR UTILITIES
# ==========================================
with st.sidebar:
    st.header("⚙️ Core Controls")
    st.info("Adjust the weighting variables or upload alternative enterprise profiles below.")
    # Add any sidebar filters or configuration inputs here

# ==========================================
# 7. HIGH-CONTRAST DATA INGESTION ENGINE
# ==========================================
@st.cache_data
def load_portfolio_data():
    try:
        data = pd.read_csv("companies.csv")
        return data
    except Exception:
        # Fallback framework if companies.csv encounters an asset error
        return pd.DataFrame({
            "Company Name": ["Enterprise Tech India", "Alpha Logistics", "SaaS Flow Solutions"],
            "Revenue ($M)": [145.2, 89.4, 34.0],
            "EBITDA Margin (%)": [24.5, 12.8, 38.2],
            "Debt-to-Equity": [0.2, 1.4, 0.0]
        })

df = load_portfolio_data()

# ==========================================
# 8. THE DASHBOARD DISPLAY
# ==========================================
st.markdown("### 📊 Market Segment Overview")

# Displaying aggregate metrics using standard container blocks to protect dark mode values
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Analyzed Candidates", value=f"{len(df)} Enterprises")
with col2:
    if "Revenue ($M)" in df.columns:
        avg_rev = round(df["Revenue ($M)"].mean(), 1)
        st.metric(label="Average Revenue Asset Scale", value=f"${avg_rev}M")
    else:
        st.metric(label="Average Revenue Asset Scale", value="N/A")
with col3:
    st.metric(label="System Core Operations", value="Active / Live")

st.markdown("#### Primary Target Data Matrix")
st.dataframe(df, use_container_width=True)

# Footer signature asset
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>MergerFlow Global Platform v2.0 • Created by Anchita Duggal</p>", unsafe_allow_html=True)
        
