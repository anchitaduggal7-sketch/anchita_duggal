import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. PAGE SETUP & THEME INITIALIZATION
st.set_page_config(
    page_title="MergerFlow Global // Enterprise M&A Target Intelligence", 
    page_icon="💼", 
    layout="wide",
    initial_sidebar_state="expanded"
)
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-HJPZDZB5KE"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-HJPZDZB5KE');
</script>

# Premium Custom CSS injection for styling tables, fonts, and metrics
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        /* Global typography overrides */
        html, body, [class*="css"], .stMarkdown {
            font-family: 'Inter', sans-serif;
        }
        
        /* Metric card container styling */
        div[data-testid="stMetricContainer"] {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        div[data-testid="stMetricLabel"] > div {
            font-size: 0.85rem !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748b !important;
            font-weight: 600;
        }
        div[data-testid="stMetricValue"] > div {
            font-size: 1.8rem !important;
            font-weight: 700;
            color: #0f172a;
        }
        
        /* Streamlit native tab styling override */
        button[data-baseweb="tab"] {
            font-size: 1rem;
            font-weight: 600;
            color: #64748b;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #0f172a;
            border-bottom-color: #0f172a;
        }
    </style>
""", unsafe_allow_html=True)

# 2. DATA LOAD ENGINE WITH CACHING
@st.cache_data
def load_and_transform_data():
    try:
        df = pd.read_csv("companies.csv")
    except FileNotFoundError:
        # Fallback Mock Data Engine to ensure immediate execution/testing
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
    
    # Data Cleaning pipeline
    for col in ["Revenue_Cr", "EBITDA_Margin", "Debt_Cr"]:
        df[col] = df[col].astype(str).str.replace(",", "", regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    df = df.dropna(subset=["Revenue_Cr", "EBITDA_Margin", "Debt_Cr"]).copy()
    
    # Financial Analytics Pre-calculations
    df["EBITDA_Cr"] = df["Revenue_Cr"] * (df["EBITDA_Margin"] / 100)
    df["EV_Cr"] = (df["Revenue_Cr"] * 2) + df["Debt_Cr"]
    df["EV_EBITDA"] = np.where(df["EBITDA_Cr"] > 0, (df["EV_Cr"] / df["EBITDA_Cr"]).round(1), np.nan)
    
    return df

df = load_and_transform_data()

# 3. INTERACTIVE CONTROL SIDEBAR
st.sidebar.markdown("### 🔍 Filter Parameters")
industry_list = ["All"] + sorted(df["Industry"].unique().tolist())
selected_industry = st.sidebar.selectbox("Target Sector", industry_list)

min_margin = st.sidebar.slider("Minimum EBITDA Margin (%)", int(df["EBITDA_Margin"].min()), int(df["EBITDA_Margin"].max()), 5)
top_n = st.sidebar.slider("Leaderboard Display Limit (Top N)", 5, 50, 10)

# 4. ALGORITHMIC SCORING ENGINE (Dynamic Context Scaling)
filtered_df = df.copy()
if selected_industry != "All":
    filtered_df = filtered_df[filtered_df["Industry"] == selected_industry]
filtered_df = filtered_df[filtered_df["EBITDA_Margin"] >= min_margin]

if not filtered_df.empty:
    # Scale variables dynamically relative to filtered scope bounds
    max_rev = filtered_df["Revenue_Cr"].max() if filtered_df["Revenue_Cr"].max() > 0 else 1
    max_margin = filtered_df["EBITDA_Margin"].max() if filtered_df["EBITDA_Margin"].max() > 0 else 1
    max_debt = filtered_df["Debt_Cr"].max() if filtered_df["Debt_Cr"].max() > 0 else 1

    filtered_df["Revenue_Score"] = filtered_df["Revenue_Cr"] / max_rev
    filtered_df["Margin_Score"] = (filtered_df["EBITDA_Margin"].clip(lower=0)) / max_margin
    filtered_df["Debt_Score"] = 1 - (filtered_df["Debt_Cr"] / max_debt)
    
    # Composite proprietary algorithm weighting
    filtered_df["Score"] = (
        filtered_df["Revenue_Score"] * 0.35 +
        filtered_df["Margin_Score"] * 0.45 +
        filtered_df["Debt_Score"] * 0.20
    ).clip(0, 1) * 100
    filtered_df["Score"] = filtered_df["Score"].round(1)

    # Statistical outlier classification (85th percentile elite cohort)
    top_quantile = filtered_df["Score"].quantile(0.85) if len(filtered_df) > 1 else filtered_df["Score"].max()
    filtered_df["Strategic_Tag"] = np.where(filtered_df["Score"] >= top_quantile, "⭐ Tier-1 Target", "Standard")
    filtered_df = filtered_df.sort_values("Score", ascending=False).reset_index(drop=True)
else:
    st.error("❌ No matching targets found within the specified financial filters.")
    st.stop()

# 5. CORE LAYOUT HEADER & KPI CARDS
st.title("🇮🇳 India M&A Target Strategic Screener")
st.caption("Corporate Development & Private Equity Analytics Dashboard")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Universe Scope", len(filtered_df))
kpi2.metric("Median Revenue", f"₹{filtered_df['Revenue_Cr'].median():,.0f} Cr")
kpi3.metric("Weighted Margin", f"{filtered_df['EBITDA_Margin'].mean():.1f}%")
kpi4.metric("Tier-1 Pipeline", len(filtered_df[filtered_df['Strategic_Tag'] == '⭐ Tier-1 Target']))

st.write("")

# 6. WORKSPACE INTERFACE (TABS DESIGN)
tab_dashboard, tab_analytics, tab_methodology = st.tabs(["📋 Target Leaderboard", "📊 Market Analytics", "📚 Methodology Blueprint"])

with tab_dashboard:
    col_lead, col_detail = st.columns([2, 1])
    
    with col_lead:
        st.subheader("High-Score Corporate Targets")
        display_cols = ["Company", "Industry", "Revenue_Cr", "EBITDA_Margin", "Debt_Cr", "EV_EBITDA", "Score", "Strategic_Tag"]
        
        # Interactive Target Dataframe Selector
        selected_row = st.dataframe(
            filtered_df.head(top_n)[display_cols],
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row"  # Fixed selection parameter
        )
        
        # Export Actions Toolbar
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Screened Results Pipeline (.CSV)",
            data=csv_data,
            file_name="ma_target_screener_output.csv",
            mime="text/csv"
        )
        
    with col_detail:
        st.subheader("🎯 Target Profile Inspection")
        
        # Fixed selection state extraction matching Streamlit 1.35+ specifications
        selection_state = selected_row.get("selection", {})
        selected_rows_list = selection_state.get("rows", [])
        
        if len(selected_rows_list) > 0:
            target_index = selected_rows_list[0]
            # Safety check to avoid index mapping shifting on slices
            target_record = filtered_df.head(top_n).iloc[target_index]
            
            st.markdown(f"### **{target_record['Company']}**")
            st.markdown(f"**Sector Cluster:** `{target_record['Industry']}`")
            st.markdown(f"**Strategic Priority Classification:** {target_record['Strategic_Tag']}")
            st.divider()
            
            # Contextual profiling breakdown
            c1, c2 = st.columns(2)
            c1.metric("Revenue Volume", f"₹{target_record['Revenue_Cr']:,} Cr")
            c2.metric("Operating Margin", f"{target_record['EBITDA_Margin']}%")
            
            c3, c4 = st.columns(2)
            c3.metric("Total Debt Load", f"₹{target_record['Debt_Cr']:,} Cr")
            
            # Formatted handle for NaN multiples
            ev_ebitda_val = target_record['EV_EBITDA']
            ev_display = f"{ev_ebitda_val}x" if not pd.isna(ev_ebitda_val) else "N/A (Negative Yield)"
            c4.metric("EV / EBITDA", ev_display)
            
            # Progress bar health indicators
            st.write("**Proprietary Screening Health Score Match**")
            st.progress(int(target_record['Score'] / 100))
        else:
            st.info("💡 **Interactive Insights Activation:** Select/click any corporate row entity on the left table leaderboard to compile a comprehensive, dedicated target dossier card instantly.")

with tab_analytics:
    st.subheader("Data Distribution & Strategic Clustering Graphs")
    
    g1, g2 = st.columns(2)
    
    with g1:
        st.markdown("**Strategic Scatter Matrix (Efficiency vs Volume)**")
        # Creating a dynamic absolute bubble sizing column to avoid negative/zero radius errors
        scatter_df = filtered_df.copy()
        scatter_df["Bubble_Size"] = np.where(scatter_df["Debt_Cr"] > 0, scatter_df["Debt_Cr"], 1)
        
        fig_scatter = px.scatter(
            scatter_df,
            x="Revenue_Cr",
            y="EBITDA_Margin",
            size="Bubble_Size",
            color="Score",
            hover_name="Company",
            labels={"Revenue_Cr": "Revenue (INR Cr)", "EBITDA_Margin": "EBITDA Margin (%)", "Bubble_Size": "Debt Load (Cr)"},
            color_continuous_scale="darkmint"
        )
        fig_scatter.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=420)
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with g2:
        st.markdown("**Macro Sector Average Score Output Matrix**")
        sector_agg = filtered_df.groupby("Industry")["Score"].mean().reset_index().sort_values("Score", ascending=True)
        
        fig_sector = px.bar(
            sector_agg,
            x="Score",
            y="Industry",
            orientation="h",
            color="Score",
            color_continuous_scale="ice",
            labels={"Score": "Average Score Cluster", "Industry": ""}
        )
        fig_sector.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=420, coloraxis_showscale=False)
        st.plotly_chart(fig_sector, use_container_width=True)

with tab_methodology:
    st.markdown("### Proprietary Screening Engine Core Architecture")
    st.markdown("""
    This systematic pipeline is structured to mimic standard institutional private equity prioritization methodologies. 
    The final score normalization weights corporate scale vectors, margin efficiency profile matrixing, and leverage balance risks.
    """)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.info("### 📊 1. Scale Profile Matrix\n**Weight: 35%**\n\n* **Formula:** `Revenue / Max(Revenue)`\n* **Intent:** Ensures target entities meet minimum deployment ticket scale constraints.")
    with m2:
        st.info("### 📈 2. Operating Efficiency\n**Weight: 45%**\n\n* **Formula:** `EBITDA Margin / Max(Margin)`\n* **Intent:** Maximizes target operating viability score performance metrics.")
    with m3:
        st.info("### 🛡️ 3. Balance Sheet Risk\n**Weight: 20%**\n\n* **Formula:** `1 - (Debt / Max(Debt))`\n* **Intent:** Penalizes excessive leverage structures to mitigate immediate restructuring friction overhead.")
