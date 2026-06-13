import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="MergerFlow Global",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# GOOGLE ANALYTICS
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
# GLOBAL STYLING
# =========================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #f7f3ea;
        }

        .stApp {
            background-color: #f7f3ea;
        }

        h1 {
            font-size: 44px !important;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.5px;
        }

        .subtitle {
            font-size: 18px;
            color: #475569;
            margin-top: -10px;
            margin-bottom: 20px;
        }

        div[data-testid="stMetricContainer"] {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            padding: 14px 16px;
            border-radius: 12px;
        }

        div[data-testid="stMetricValue"] {
            font-weight: 700;
        }

        section[data-testid="stSidebar"] {
            background-color: #fbf8f1;
        }

        footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# =========================
# DATA LOADING ENGINE
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

    df.columns = df.columns.str.strip()

    for col in ["Revenue_Cr", "EBITDA_Margin", "Debt_Cr"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna().copy()

    df["EBITDA_Cr"] = df["Revenue_Cr"] * (df["EBITDA_Margin"] / 100)
    df["EV_Cr"] = (df["Revenue_Cr"] * 2) + df["Debt_Cr"]
    df["EV_EBITDA"] = np.where(df["EBITDA_Cr"] > 0, df["EV_Cr"] / df["EBITDA_Cr"], np.nan)

    return df

df = load_and_transform_data()

# =========================
# SIDEBAR FILTERS
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

top_n = st.sidebar.slider("Leaderboard Display Limit", 5, 50, 10)

# =========================
# FILTER LOGIC
# =========================
filtered_df = df.copy()

if selected_industry != "All":
    filtered_df = filtered_df[filtered_df["Industry"] == selected_industry]

filtered_df = filtered_df[filtered_df["EBITDA_Margin"] >= min_margin]

if filtered_df.empty:
    st.error("No matching targets found.")
    st.stop()

# =========================
# SCORING ENGINE
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
# HEADER
# =========================
st.title("MergerFlow Global")

st.markdown(
    '<div class="subtitle">Institutional-Grade M&A Intelligence & Target Screening Platform</div>',
    unsafe_allow_html=True
)

st.markdown("**Built by Anchita Duggal**")

# =========================
# KPI METRICS
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.metric("Universe Scope", len(filtered_df))
c2.metric("Median Revenue", f"₹{filtered_df['Revenue_Cr'].median():,.0f} Cr")
c3.metric("Avg Margin", f"{filtered_df['EBITDA_Margin'].mean():.1f}%")
c4.metric("Tier-1 Targets", len(filtered_df[filtered_df["Strategic_Tag"] == "⭐ Tier-1 Target"]))

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs([
    "📋 Leaderboard",
    "📊 Analytics",
    "📚 Methodology"
])

# =========================
# TAB 1
# =========================
with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Top M&A Targets")

        display_cols = [
            "Company", "Industry", "Revenue_Cr",
            "EBITDA_Margin", "Debt_Cr", "EV_EBITDA",
            "Score", "Strategic_Tag"
        ]

        st.dataframe(filtered_df.head(top_n)[display_cols], use_container_width=True)

        csv = filtered_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Export CSV",
            csv,
            "ma_targets.csv",
            "text/csv"
        )

    with col2:
        st.subheader("Target Insight")

        st.info("Select a company in leaderboard (future upgrade: click-based drilldown can be added).")

# =========================
# TAB 2
# =========================
with tab2:
    st.subheader("Analytics Dashboard")

    fig1 = px.scatter(
        filtered_df,
        x="Revenue_Cr",
        y="EBITDA_Margin",
        size="Debt_Cr",
        color="Score",
        hover_name="Company",
        color_continuous_scale="viridis"
    )

    st.plotly_chart(fig1, use_container_width=True)

    sector = filtered_df.groupby("Industry")["Score"].mean().reset_index()

    fig2 = px.bar(
        sector,
        x="Industry",
        y="Score",
        color="Score"
    )

    st.plotly_chart(fig2, use_container_width=True)

# =========================
# TAB 3
# =========================
with tab3:
    st.markdown("### Methodology")

    st.write("""
    Score = Weighted combination of:
    - Revenue Scale (35%)
    - EBITDA Margin Efficiency (45%)
    - Debt Efficiency (20%)
    """)

    st.success("Built using institutional M&A screening logic adapted for private equity workflows.")
