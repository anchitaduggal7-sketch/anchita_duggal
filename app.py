import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit.components.v1 as components

# =========================
# PAGE SETUP (ORIGINAL)
# =========================
st.set_page_config(
    page_title="India M&A Target Screener", 
    page_icon="💼", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# GOOGLE ANALYTICS (OPTIONAL - SAFE ADDITION ONLY)
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
# ORIGINAL CSS (RESTORED STYLE)
# =========================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        html, body, [class*="css"], .stMarkdown {
            font-family: 'Inter', sans-serif;
        }

        div[data-testid="stMetricContainer"] {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 15px 20px;
            border-radius: 10px;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.6rem;
            font-weight: 700;
        }

        button[data-baseweb="tab"] {
            font-weight: 600;
        }
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
    st.error("❌ No matching targets found.")
    st.stop()

# =========================
# SCORING ENGINE (UNCHANGED)
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

top_quantile = filtered_df["Score"].quantile(0.85)
filtered_df["Strategic_Tag"] = np.where(
    filtered_df["Score"] >= top_quantile,
    "⭐ Tier-1 Target",
    "Standard"
)

filtered_df = filtered_df.sort_values("Score", ascending=False).reset_index(drop=True)

# =========================
# HEADER (RESTORED STYLE)
# =========================
st.title("🇮🇳 India M&A Target Strategic Screener")
st.caption("Corporate Development & Private Equity Analytics Dashboard")

st.markdown("**Built by Anchita Duggal**")

# =========================
# KPI (UNCHANGED)
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Universe Scope", len(filtered_df))
c2.metric("Median Revenue", f"₹{filtered_df['Revenue_Cr'].median():,.0f} Cr")
c3.metric("Weighted Margin", f"{filtered_df['EBITDA_Margin'].mean():.1f}%")
c4.metric("Tier-1 Pipeline", len(filtered_df[filtered_df["Strategic_Tag"] == "⭐ Tier-1 Target"]))

# =========================
# TABS (UNCHANGED)
# =========================
tab_dashboard, tab_analytics, tab_methodology = st.tabs([
    "📋 Target Leaderboard",
    "📊 Market Analytics",
    "📚 Methodology Blueprint"
])

# =========================
# DASHBOARD TAB (UNCHANGED)
# =========================
with tab_dashboard:
    st.subheader("High-Score Corporate Targets")

    display_cols = [
        "Company", "Industry", "Revenue_Cr",
        "EBITDA_Margin", "Debt_Cr", "EV_EBITDA",
        "Score", "Strategic_Tag"
    ]

    st.dataframe(filtered_df.head(top_n)[display_cols], use_container_width=True, hide_index=True)

    st.download_button(
        "📥 Export Screened Results Pipeline (.CSV)",
        filtered_df.to_csv(index=False).encode("utf-8"),
        "ma_target_screener_output.csv",
        "text/csv"
    )

# =========================
# ANALYTICS TAB (UNCHANGED)
# =========================
with tab_analytics:
    st.subheader("Market Analytics")

    fig = px.scatter(
        filtered_df,
        x="Revenue_Cr",
        y="EBITDA_Margin",
        size="Debt_Cr",
        color="Score",
        hover_name="Company"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# METHODOLOGY TAB (UNCHANGED)
# =========================
with tab_methodology:
    st.markdown("### Methodology Blueprint")

    st.write("""
    Weighted scoring model:
    - Revenue Scale (35%)
    - EBITDA Margin (45%)
    - Debt Efficiency (20%)
    """)

    st.success("Institutional screening logic preserved exactly as original.")
