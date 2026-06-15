import streamlit as st

st.set_page_config(
    page_title="MergerFlow Research Center",
    page_icon="📚",
    layout="wide"
)

st.title("📚 MergerFlow Research Center")
st.caption("Enterprise M&A Education, Deal Analysis & Transaction Intelligence")

st.markdown("---")

# M&A Lifecycle
st.header("🏛 The M&A Lifecycle")

lifecycle_steps = [
    "1. Corporate Strategy Formulation",
    "2. Target Identification & Screening",
    "3. Initial Outreach & Confidential Discussions",
    "4. Non-Disclosure Agreement (NDA)",
    "5. Due Diligence",
    "6. Valuation & Financial Analysis",
    "7. Deal Structuring",
    "8. Negotiation",
    "9. Definitive Agreements",
    "10. Regulatory Review & Approval",
    "11. Transaction Close",
    "12. Post-Merger Integration"
]

for step in lifecycle_steps:
    st.markdown(f"✅ {step}")

st.markdown("---")

# Due Diligence
st.header("🔍 Due Diligence Framework")

with st.expander("Financial Due Diligence"):
    st.markdown("""
    - Revenue quality assessment
    - EBITDA normalization
    - Cash flow analysis
    - Working capital review
    - Debt obligations
    - Historical performance trends
    """)

with st.expander("Legal Due Diligence"):
    st.markdown("""
    - Litigation review
    - Contract analysis
    - Intellectual property ownership
    - Regulatory compliance
    - Employment agreements
    """)

with st.expander("Commercial Due Diligence"):
    st.markdown("""
    - Market size and growth
    - Competitive positioning
    - Customer concentration
    - Pricing power
    - Industry outlook
    """)

with st.expander("Operational Due Diligence"):
    st.markdown("""
    - Supply chain resilience
    - Technology infrastructure
    - Human capital assessment
    - Operational efficiency
    - Integration readiness
    """)

st.markdown("---")

# Valuation
st.header("💰 Valuation Academy")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    ### Discounted Cash Flow (DCF)

    Values a company based on projected future cash flows discounted back to present value.

    Most useful when:
    - Cash flows are predictable
    - Long-term forecasts are reliable
    """)

    st.info("""
    ### Comparable Company Analysis

    Values a company using trading multiples of similar public companies.

    Common multiples:
    - EV / EBITDA
    - EV / Revenue
    - P / E
    """)

with col2:
    st.info("""
    ### Precedent Transactions

    Uses historical acquisition multiples paid in similar deals.

    Captures:
    - Control premium
    - Strategic value
    - Market conditions
    """)

    st.info("""
    ### Leveraged Buyout (LBO)

    Determines value based on returns achievable using debt financing.

    Key Drivers:
    - Entry Multiple
    - Exit Multiple
    - Debt Structure
    - EBITDA Growth
    """)

st.markdown("---")

# Deal Case Studies
st.header("📖 Landmark M&A Case Studies")

with st.expander("Microsoft × LinkedIn (2016)"):
    st.markdown("""
    **Deal Value:** $26.2 Billion

    **Strategic Rationale**
    - Strengthen enterprise ecosystem
    - Integrate professional network with Office products

    **Outcome**
    - Significant growth in LinkedIn revenue
    - Improved enterprise data ecosystem
    """)

with st.expander("Facebook × Instagram (2012)"):
    st.markdown("""
    **Deal Value:** ~$1 Billion

    **Strategic Rationale**
    - Mobile-first social platform acquisition
    - Eliminate emerging competitive threat

    **Outcome**
    - Became one of the most successful acquisitions in technology history
    """)

with st.expander("Disney × 21st Century Fox (2019)"):
    st.markdown("""
    **Deal Value:** ~$71 Billion

    **Strategic Rationale**
    - Content expansion
    - Strengthen streaming capabilities

    **Outcome**
    - Major scale increase for Disney+
    - Consolidation of media assets
    """)

with st.expander("Google × YouTube (2006)"):
    st.markdown("""
    **Deal Value:** $1.65 Billion

    **Strategic Rationale**
    - Dominance in online video
    - Expansion of advertising inventory

    **Outcome**
    - YouTube became the world's largest video platform
    """)

st.markdown("---")

st.header("🎯 How MergerFlow Screens Targets")

st.markdown("""
MergerFlow's proprietary screening engine ranks acquisition candidates using a weighted scoring methodology based on:

- Revenue Scale (35%)
- EBITDA Margin Efficiency (45%)
- Balance Sheet Risk (20%)

The objective is to identify financially attractive targets exhibiting strong operating performance while minimizing leverage-related risks.

This framework is inspired by institutional private equity and corporate development screening methodologies.
""")

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#94a3b8; font-size:0.8rem;">
        Engineered by Anchita Duggal · MergerFlow Global
    </div>
    """,
    unsafe_allow_html=True
)
