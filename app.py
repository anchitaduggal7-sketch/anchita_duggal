import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px

# =========================
# PAGE CONFIG (UNCHANGED)
# =========================
st.set_page_config(
    page_title="India M&A Target Screener", 
    page_icon="💼", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# GOOGLE ANALYTICS (ADDED ONLY)
# =========================
GA_ID = "G-HJPZDZB5KE"

components.html(f"""
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_ID}');
</script>
""", height=0)

# =========================
# BLOOMBERG TERMINAL UI (NEW THEME - ADDITIVE ONLY)
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* BLOOMBERG DARK TERMINAL THEME */
.stApp {
    background-color: #0b0f14;
    color: #e5e7eb;
}

/* Headings */
h1, h2, h3 {
    color: #f5f5f5 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f1720;
}

/* Metric cards */
div[data-testid="stMetricContainer"] {
    background-color: #111827;
    border: 1px solid #1f2937;
    padding: 14px;
    border-radius: 10px;
}

/* Dataframes */
div[data-testid="stDataFrame"] {
    border-radius: 10px;
    border: 1px solid #1f2937;
}

/* Buttons */
button {
    border-radius: 6px !important;
}

/* Accent (Bloomberg green) */
.css-1v0mbdj, .stMetricValue {
    color: #00ff9f !important;
}

/* Hide footer */
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =========================
# DATA ENGINE (UNCHANGED)
# =========================
@st.cache_data
def load_and_transform_data():
    try:
        df = pd.read_csv("companies.csv")
    except FileNotFoundError:
        mock_data = {
            "Company": ["Reliance Retail", "Tata Digital", "Infosys BPM", "Zomato Ltd", "Paytm Core", 
                        "Apollo Health", "Adani Power Sub", "Mahindra Logi", "Godrej Prop", "Wipro Digital"],
            "Industry": ["Retail", "Technology", "Technology", "Consumer Tech", "Consumer Tech", 
                         "Healthcare", "Energy", "Logistics", "Real Estate", "Technology"],
            "Revenue_Cr": [45000, 12000, 8500, 6200, 4100, 9800, 22000, 5100, 7400, 6800],
            "EBITDA_Margin": [8.2, -4.5, 22.1, 3.8, -12.4, 18.5, 29.0, 6.2, 14.1, 16.8],
            "Debt_Cr": [12000, 1500, 200, 0, 150, 2400, 31000, 850, 4200, 600]
        }
        df = pd.DataFrame(mock_data)

    for col in ["Revenue_Cr", "EBITDA_Margin", "Debt_Cr"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna().copy()

    df["EBITDA_Cr"] = df["Revenue_Cr"] * (df["EBITDA_Margin"] / 100)
    df["EV_Cr"] = (df["Revenue_Cr"] * 2) + df["Debt_Cr"]
    df["EV_EBITDA"] = np.where(df["EBITDA_Cr"] > 0, df["EV_Cr"] / df["EBITDA_Cr"], np.nan)

    return df

df = load_and_transform_data()

# =========================
# SIDEBAR (UNCHANGED)
# =========================
st.sidebar.markdown("### 🔍 Filter Parameters")

industry_list = ["All"] + sorted(df["Industry"].unique().tolist())
selected_industry = st.sidebar.selectbox("Target Sector", industry_list)

min_margin = st.sidebar.slider(
    "Minimum EBITDA Margin (%)",
    int(df["EBITDA_Margin"].min()),
    int(df["EBITDA_Margin"].max()),
    5
)

top_n = st.sidebar.slider("Leaderboard Display Limit (Top N)", 5, 50, 10)

# =========================
# FILTERING (UNCHANGED)
# =========================
filtered_df = df.copy()

if selected_industry != "All":
    filtered_df = filtered_df[filtered_df["Industry"] == selected_industry]

filtered_df = filtered_df[filtered_df["EBITDA_Margin"] >= min_margin]

if filtered_df.empty:
    st.error("No matching targets found.")
    st.stop()

# =========================
# CORE SCORING ENGINE (UNCHANGED)
# =========================
max_rev = filtered_df["Revenue_Cr"].max() or 1
max_margin = filtered_df["EBITDA_Margin"].max() or 1
max_debt = filtered_df["Debt_Cr"].max() or 1

filtered_df["Revenue_Score"] = filtered_df["Revenue_Cr"] / max_rev
filtered_df["Margin_Score"] = filtered_df["EBITDA_Margin"].clip(lower=0) / max_margin
filtered_df["Debt_Score"] = 1 - (filtered_df["Debt_Cr"] / max_debt)

filtered_df["Score"] = (
    filtered_df["Revenue_Score"] * 0.35 +
    filtered_df["Margin_Score"] * 0.45 +
    filtered_df["Debt_Score"] * 0.20
) * 100

filtered_df["Score"] = filtered_df["Score"].round(1)

# =========================
# 🧠 AI PE ANALYST LAYER (NEW - ADDITION ONLY)
# =========================
filtered_df["AI_Growth_Profile"] = np.where(
    filtered_df["Revenue_Cr"] > filtered_df["Revenue_Cr"].median(),
    1, 0.5
)

filtered_df["AI_Risk_Profile"] = np.where(
    filtered_df["Debt_Cr"] > filtered_df["Debt_Cr"].median(),
    0.4, 0.8
)

filtered_df["AI_Margin_Quality"] = np.where(
    filtered_df["EBITDA_Margin"] > 15,
    1, 0.6
)

filtered_df["AI_Score"] = (
    filtered_df["AI_Growth_Profile"] * 0.4 +
    filtered_df["AI_Risk_Profile"] * 0.3 +
    filtered_df["AI_Margin_Quality"] * 0.3
) * 100

filtered_df["AI_Score"] = filtered_df["AI_Score"].round(1)

# =========================
# DEAL RECOMMENDATION ENGINE (NEW - ADDITION ONLY)
# =========================
def recommend(score, ai_score):
    if score > 75 and ai_score > 70:
        return "🟢 BUY"
    elif score > 55:
        return "🟡 HOLD"
    else:
        return "🔴 PASS"

filtered_df["Deal_Action"] = filtered_df.apply(
    lambda x: recommend(x["Score"], x["AI_Score"]),
    axis=1
)

# =========================
# STRATEGIC TAGGING (UNCHANGED)
# =========================
top_quantile = filtered_df["Score"].quantile(0.85)
filtered_df["Strategic_Tag"] = np.where(
    filtered_df["Score"] >= top_quantile,
    "⭐ Tier-1 Target",
    "Standard"
)

filtered_df = filtered_df.sort_values("Score", ascending=False).reset_index(drop=True)

# =========================
# HEADER (UPGRADED VISUAL ONLY)
# =========================
st.title("MERGERFLOW GLOBAL — TERMINAL")

st.markdown("**Bloomberg-Style M&A Intelligence System | Built by Anchita Duggal**")

# =========================
# KPI (UNCHANGED + ADDITION)
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Universe", len(filtered_df))
c2.metric("Median Revenue", f"₹{filtered_df['Revenue_Cr'].median():,.0f} Cr")
c3.metric("Avg Score", f"{filtered_df['Score'].mean():.1f}")
c4.metric("BUY Signals", len(filtered_df[filtered_df["Deal_Action"] == "🟢 BUY"]))

# =========================
# TABS (UNCHANGED STRUCTURE + NEW TAB ADDED)
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Terminal Screen",
    "📊 Analytics",
    "📚 Methodology",
    "🧠 AI Analyst"
])

# =========================
# TAB 1 (UNCHANGED CORE + ADD COLUMNS ONLY)
# =========================
with tab1:
    st.subheader("M&A Target Universe")

    display_cols = [
        "Company", "Industry", "Revenue_Cr",
        "EBITDA_Margin", "Debt_Cr",
        "Score", "AI_Score", "Deal_Action", "Strategic_Tag"
    ]

    st.dataframe(filtered_df.head(top_n)[display_cols], use_container_width=True)

    st.download_button(
        "Export Terminal Sheet",
        filtered_df.to_csv(index=False).encode("utf-8"),
        "mergerflow_terminal.csv",
        "text/csv"
    )

# =========================
# TAB 2 (UNCHANGED VISUAL LOGIC)
# =========================
with tab2:
    fig = px.scatter(
        filtered_df,
        x="Revenue_Cr",
        y="EBITDA_Margin",
        size="Debt_Cr",
        color="AI_Score",
        hover_name="Company",
        color_continuous_scale="teal"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 3 (UNCHANGED)
# =========================
with tab3:
    st.markdown("### Institutional Model")
    st.write("Original scoring engine preserved + AI overlay added.")

# =========================
# TAB 4 — AI ANALYST (NEW)
# =========================
with tab4:
    st.markdown("## 🧠 AI PE Analyst View")

    st.write("This layer simulates an investment committee style evaluation.")

    st.dataframe(
        filtered_df[[
            "Company",
            "Score",
            "AI_Score",
            "Deal_Action"
        ]],
        use_container_width=True
    )

    st.success("AI layer is heuristic-based (no external API). Can be upgraded to GPT-based model later.")
