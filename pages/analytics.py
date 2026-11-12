import textwrap
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Gurgaon Estates Pro | Market Intelligence",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# 2. CUSTOM CSS (COMMERCIAL UI + FULL CONTRAST LOCK)
# =====================================================
st.markdown(
    textwrap.dedent("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        color-scheme: light !important;
    }

    /* Layered Soft Slate-Ice Main Background (Makes White Cards Pop) */
    .stApp,
    [data-testid="stAppViewContainer"],
    section.main,
    [data-testid="stMain"] {
        background: linear-gradient(180deg, #ebf2f7 0%, #f5f8fb 40%, #edf3f8 100%) !important;
        font-family: 'DM Sans', sans-serif !important;
        color: #0c2335 !important;
    }

    /* Transparent Top Header Bar */
    [data-testid="stHeader"] {
        background-color: rgba(235, 242, 247, 0.85) !important;
        backdrop-filter: blur(8px);
    }

    .block-container {
        max-width: 1380px;
        padding-top: 1.6rem;
        padding-bottom: 3rem;
    }

    /* Force Crisp Dark Text on Main Page */
    section.main p,
    section.main label,
    section.main h1,
    section.main h2,
    section.main h3,
    section.main h4,
    [data-testid="stMain"] p,
    [data-testid="stMain"] label,
    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] h4,
    [data-testid="stWidgetLabel"] p {
        color: #0c2335 !important;
    }

    /* =================================================
       SIDEBAR STYLING (OCEAN-TEAL GRADIENT)
       ================================================= */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div:first-child {
        background-color: #0d2638 !important;
        background-image: linear-gradient(180deg, #0d2638 0%, #11354c 55%, #164960 100%) !important;
        border-right: 1px solid #1d4d68 !important;
    }

    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"],
    [data-testid="stSidebarHeader"],
    [data-testid="stSidebarNav"] {
        background-color: transparent !important;
        background-image: none !important;
    }

    [data-testid="stSidebarNav"] span {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebarNav"] a:hover {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: rgba(156, 229, 211, 0.16) !important;
        border-left: 3px solid #9ce5d3 !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] span {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #f1f5f9 !important;
    }

    [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #163d54 !important;
        border: 1px solid #2b5d7a !important;
        border-radius: 10px !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="select"] span,
    [data-testid="stSidebar"] div[data-baseweb="select"] input {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] span[data-baseweb="tag"] {
        background-color: #187573 !important;
        border: 1px solid #2aa19e !important;
        border-radius: 6px !important;
    }
    [data-testid="stSidebar"] span[data-baseweb="tag"] span {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: rgba(255, 255, 255, 0.10) !important;
        border: 1px solid rgba(156, 229, 211, 0.35) !important;
        color: #9ce5d3 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #187573 !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stButton > button p {
        color: inherit !important;
    }

    .sidebar-stat-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 14px 16px;
        margin-top: 10px;
    }
    .sidebar-stat-label {
        color: #9ce5d3 !important;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    .sidebar-stat-val {
        color: #ffffff !important;
        font-size: 20px;
        font-weight: 800;
        margin-top: 4px;
    }
    .sidebar-stat-sub {
        color: #cbd5e1 !important;
        font-size: 12px;
        margin-top: 2px;
    }

    /* Main Page Dropdowns & Expanders */
    section.main div[data-baseweb="select"] > div,
    [data-testid="stMain"] div[data-baseweb="select"] > div,
    [data-testid="stExpander"] details,
    [data-testid="stExpander"] summary {
        background-color: #ffffff !important;
        border: 1px solid #d5e0ea !important;
        border-radius: 10px !important;
        color: #0c2335 !important;
    }
    section.main div[data-baseweb="select"] span,
    section.main div[data-baseweb="select"] input,
    [data-testid="stMain"] div[data-baseweb="select"] span,
    [data-testid="stMain"] div[data-baseweb="select"] input {
        color: #0c2335 !important;
    }

    /* Dropdown Popup Menus */
    div[data-baseweb="popover"],
    ul[data-baseweb="menu"],
    ul[data-baseweb="menu"] li {
        background-color: #ffffff !important;
        color: #0c2335 !important;
    }
    ul[data-baseweb="menu"] li:hover {
        background-color: #eef4f8 !important;
    }

    /* =================================================
       HERO BANNER
       ================================================= */
    .main-header {
        background: linear-gradient(115deg, #0b2234 0%, #0f384c 52%, #187573 100%) !important;
        padding: 36px 42px;
        border-radius: 20px;
        margin-bottom: 24px;
        box-shadow: 0 14px 32px rgba(11, 34, 52, 0.14);
    }
    .header-pill {
        display: inline-block;
        background: rgba(255, 255, 255, 0.09);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: #9ce5d3 !important;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2.5px;
        padding: 6px 14px;
        border-radius: 999px;
        text-transform: uppercase;
    }
    .header-title {
        color: #ffffff !important;
        font-size: 35px;
        font-weight: 800;
        margin-top: 14px;
        line-height: 1.2;
    }
    .header-title-accent {
        color: #9ce5d3 !important;
        display: block;
    }
    .header-description {
        color: #cbd5e1 !important;
        font-size: 15px;
        margin-top: 10px;
        max-width: 680px;
        line-height: 1.6;
    }
    .header-divider {
        border: none;
        border-top: 1px solid rgba(255, 255, 255, 0.14);
        margin: 20px 0 16px 0;
    }
    .header-stats-row {
        display: flex;
        gap: 44px;
        flex-wrap: wrap;
    }
    .header-stat-num {
        color: #ffffff !important;
        font-size: 19px;
        font-weight: 800;
    }
    .header-stat-sub {
        color: #94a3b8 !important;
        font-size: 12px;
        margin-top: 2px;
    }

    /* Insight Cards */
    .insight-card {
        background: #ffffff;
        border: 1px solid #dde6ef;
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 3px 12px rgba(12, 35, 53, 0.04);
    }
    .insight-tag {
        color: #187573 !important;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .insight-main {
        color: #0c2335 !important;
        font-size: 18px;
        font-weight: 800;
        margin-top: 4px;
    }
    .insight-sub {
        color: #64748b !important;
        font-size: 13px;
        margin-top: 2px;
    }

    /* Section Headings */
    .section-heading {
        color: #0c2335 !important;
        font-size: 22px;
        font-weight: 800;
        margin-top: 28px;
        margin-bottom: 3px;
    }
    .section-description {
        color: #64748b !important;
        font-size: 14px;
        margin-bottom: 16px;
    }

    /* =================================================
       KPI CARDS & FIX FOR BLACK DELTA BADGE
       ================================================= */
    div[data-testid="stMetric"],
    div[data-testid="stPlotlyChart"] {
        background: #ffffff !important;
        border: 1px solid #dde6ef !important;
        border-radius: 16px !important;
        padding: 18px 20px !important;
        box-shadow: 0 4px 14px rgba(12, 35, 53, 0.04) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(12, 35, 53, 0.08) !important;
    }
    div[data-testid="stMetric"] {
        border-left: 4px solid #187573 !important;
    }
    div[data-testid="stMetricLabel"] p {
        color: #475569 !important;
        font-size: 13px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricValue"] div {
        color: #0c2335 !important;
        font-size: 28px !important;
        font-weight: 800 !important;
    }

    /* Override Streamlit's Black Pill on stMetricDelta */
    div[data-testid="stMetricDelta"] {
        background-color: #e6f6f4 !important;
        border: 1px solid #b5e4dc !important;
        border-radius: 999px !important;
        padding: 3px 11px !important;
        width: fit-content !important;
        margin-top: 6px !important;
    }
    div[data-testid="stMetricDelta"] > div,
    div[data-testid="stMetricDelta"] p,
    div[data-testid="stMetricDelta"] span {
        color: #0e5c59 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricDelta"] svg {
        display: none !important;
    }

    /* Sector Spotlight Card */
    .spotlight-card {
        background: #ffffff;
        border: 1px solid #dde6ef;
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 4px 14px rgba(12, 35, 53, 0.04);
    }
    .spotlight-badge {
        display: inline-block;
        background: #e6f6f4;
        color: #12615f !important;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 999px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .spotlight-title {
        color: #0c2335 !important;
        font-size: 22px;
        font-weight: 800;
        margin: 10px 0 12px 0;
    }
    .spotlight-item {
        display: flex;
        justify-content: space-between;
        padding: 9px 0;
        border-bottom: 1px solid #f1f5f9;
        font-size: 14px;
    }
    .spotlight-item:last-child {
        border-bottom: none;
    }
    .spotlight-label {
        color: #64748b !important;
    }
    .spotlight-value {
        color: #0c2335 !important;
        font-weight: 700;
    }

    /* Primary Download Button */
    .stDownloadButton > button {
        background: linear-gradient(120deg, #0f384c, #187573) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 700 !important;
        padding: 0.55rem 1.2rem !important;
    }
    .stDownloadButton > button p {
        color: #ffffff !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b !important;
        padding-top: 35px;
        font-size: 13px;
        border-top: 1px solid #d8e2ec;
        margin-top: 40px;
    }
    </style>
    """),
    unsafe_allow_html=True,
)


# =====================================================
# 3. PLOTLY LIGHT-THEME LOCK HELPER
# =====================================================
def style_chart(fig, height=450):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family="DM Sans, sans-serif", color="#0c2335", size=12),
        title_font=dict(size=16, color="#0c2335", family="DM Sans, sans-serif"),
        height=height,
        margin=dict(l=14, r=14, t=46, b=18),
    )
    fig.update_xaxes(
        tickfont=dict(color="#334155"),
        title_font=dict(color="#0c2335"),
        gridcolor="#f1f5f9",
    )
    fig.update_yaxes(
        tickfont=dict(color="#334155"),
        title_font=dict(color="#0c2335"),
        gridcolor="#f1f5f9",
    )
    return fig


# =====================================================
# 4. LOAD & CLEAN DATA
# =====================================================
@st.cache_data
def load_data():
    property_df = pd.read_csv("data/data_viz1.csv")
    furnishing_df = pd.read_csv("data/sector_furnishing_features.csv")

    numeric_cols = ["price", "price_per_sqft", "built_up_area", "bedRoom", "latitude", "longitude"]
    for col in numeric_cols:
        if col in property_df.columns:
            property_df[col] = pd.to_numeric(property_df[col], errors="coerce")

    if "sector" in property_df.columns:
        property_df["sector"] = property_df["sector"].astype(str).str.strip()
    if "property_type" in property_df.columns:
        property_df["property_type"] = property_df["property_type"].astype(str).str.strip().str.title()
    if "bedRoom" in property_df.columns:
        property_df["bhk_label"] = property_df["bedRoom"].dropna().astype(int).astype(str) + " BHK"

    if "sector" in furnishing_df.columns:
        furnishing_df["sector"] = furnishing_df["sector"].astype(str).str.strip()

    return property_df, furnishing_df


raw_df, furnishing_df = load_data()


# =====================================================
# 5. SIDEBAR FILTERS & RESET CONTROLS
# =====================================================
valid_prices = raw_df["price"].dropna()
min_p = round(float(valid_prices.min()), 1) if not valid_prices.empty else 0.0
max_p = round(float(valid_prices.max()), 1) if not valid_prices.empty else 50.0
if max_p <= min_p:
    max_p = min_p + 1.0

prop_types = sorted(raw_df["property_type"].dropna().unique().tolist()) if "property_type" in raw_df.columns else []
bhk_options = sorted(raw_df["bedRoom"].dropna().astype(int).unique().tolist()) if "bedRoom" in raw_df.columns else []
all_sectors = sorted(raw_df["sector"].dropna().unique().tolist()) if "sector" in raw_df.columns else []

with st.sidebar:
    st.markdown("### 🏠 Gurgaon Estates")
    st.markdown(
        "<span style='color:#9ce5d3; font-size:11px; font-weight:700; letter-spacing:2px;'>PROPTECH INTELLIGENCE</span>",
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown("#### 🔍 Market Filters")

    selected_types = st.multiselect(
        "Property Type",
        options=prop_types,
        default=prop_types,
        key="filter_prop_type",
    )

    price_range = st.slider(
        "Budget Range (₹ Cr)",
        min_value=min_p,
        max_value=max_p,
        value=(min_p, max_p),
        step=0.5,
        key="filter_price_range",
    )

    selected_bhk = st.multiselect(
        "Bedrooms (BHK)",
        options=bhk_options,
        default=bhk_options,
        format_func=lambda x: f"{x} BHK",
        key="filter_bhk",
    )

    selected_sectors = st.multiselect(
        "Target Sectors (Optional)",
        options=all_sectors,
        default=[],
        placeholder="All Gurgaon Sectors",
        key="filter_sectors",
    )

    if st.button("↺ Reset All Filters"):
        st.session_state["filter_prop_type"] = prop_types
        st.session_state["filter_price_range"] = (min_p, max_p)
        st.session_state["filter_bhk"] = bhk_options
        st.session_state["filter_sectors"] = []
        st.rerun()

# Apply Filters
new_df = raw_df.copy()
if selected_types and "property_type" in new_df.columns:
    new_df = new_df[new_df["property_type"].isin(selected_types)]
new_df = new_df[new_df["price"].between(price_range[0], price_range[1])]
if selected_bhk and "bedRoom" in new_df.columns:
    new_df = new_df[new_df["bedRoom"].isin(selected_bhk)]
if selected_sectors:
    new_df = new_df[new_df["sector"].isin(selected_sectors)]

with st.sidebar:
    pct_active = (len(new_df) / len(raw_df) * 100) if len(raw_df) else 0
    st.markdown(
        textwrap.dedent(f"""
        <div class="sidebar-stat-card">
            <div class="sidebar-stat-label">Active Scope</div>
            <div class="sidebar-stat-val">{len(new_df):,} Properties</div>
            <div class="sidebar-stat-sub">{pct_active:.0f}% of {len(raw_df):,} total listings</div>
        </div>
        """),
        unsafe_allow_html=True,
    )


# =====================================================
# 6. HERO BANNER
# =====================================================
st.markdown(
    textwrap.dedent(f"""
    <div class="main-header">
        <div class="header-pill">GURGAON REAL ESTATE INTELLIGENCE • 2026</div>
        <div class="header-title">
            Market Analytics &
            <span class="header-title-accent">Pricing Insights.</span>
        </div>
        <div class="header-description">
            Institutional-grade valuation benchmarks, geospatial sector heatmaps,
            and residential amenity intelligence across Gurgaon micro-markets.
        </div>
        <hr class="header-divider" />
        <div class="header-stats-row">
            <div>
                <div class="header-stat-num">{new_df['sector'].nunique()}+ Sectors</div>
                <div class="header-stat-sub">Gurgaon Micro-Markets Covered</div>
            </div>
            <div>
                <div class="header-stat-num">{len(new_df):,} Listings</div>
                <div class="header-stat-sub">Verified Market Inventory</div>
            </div>
            <div>
                <div class="header-stat-num">Live Spatial Map</div>
                <div class="header-stat-sub">Interactive Valuation Benchmarks</div>
            </div>
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)

if new_df.empty:
    st.warning("No properties match your sidebar filters. Click 'Reset All Filters' in the sidebar.")
    st.stop()


# =====================================================
# 7. MARKET OVERVIEW KPIs & AUTOMATED INSIGHTS
# =====================================================
st.markdown('<div class="section-heading">Market Overview</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">Real-time valuation metrics and automated micro-market highlights.</div>',
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Total Properties", f"{len(new_df):,}", delta="Active Selection", delta_color="off")

with m2:
    st.metric("Total Sectors", f"{new_df['sector'].nunique():,}", delta="Covered Locations", delta_color="off")

with m3:
    avg_price = new_df["price"].mean()
    med_price = new_df["price"].median()
    st.metric(
        "Average Property Price",
        f"₹{avg_price:,.2f} Cr" if pd.notna(avg_price) else "N/A",
        delta=f"Median: ₹{med_price:,.2f} Cr" if pd.notna(med_price) else None,
        delta_color="off",
    )

with m4:
    avg_rate = new_df["price_per_sqft"].mean()
    med_rate = new_df["price_per_sqft"].median()
    st.metric(
        "Average Price / Sqft",
        f"₹{avg_rate:,.0f}" if pd.notna(avg_rate) else "N/A",
        delta=f"Median: ₹{med_rate:,.0f}/sqft" if pd.notna(med_rate) else None,
        delta_color="off",
    )

# Automated Executive Insight Strip
sector_rates = new_df.groupby("sector")["price_per_sqft"].mean().dropna()
if not sector_rates.empty:
    top_sec = sector_rates.idxmax()
    top_sec_rate = sector_rates.max()
    val_sec = sector_rates.idxmin()
    val_sec_rate = sector_rates.min()
    dom_bhk = (
        new_df["bhk_label"].mode().iloc[0]
        if "bhk_label" in new_df.columns and not new_df["bhk_label"].dropna().empty
        else "N/A"
    )
    dom_share = (new_df["bhk_label"] == dom_bhk).mean() * 100 if dom_bhk != "N/A" else 0

    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-tag">🏆 Highest Rate Micro-Market</div>
                <div class="insight-main">{top_sec}</div>
                <div class="insight-sub">Average rate of ₹{top_sec_rate:,.0f} / sqft</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-tag">💎 Best Value Entry Market</div>
                <div class="insight-main">{val_sec}</div>
                <div class="insight-sub">Average rate of ₹{val_sec_rate:,.0f} / sqft</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-tag">🏠 Dominant Inventory Mix</div>
                <div class="insight-main">{dom_bhk} Units</div>
                <div class="insight-sub">Accounts for {dom_share:.1f}% of filtered listings</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =====================================================
# 8. SECTOR-WISE PROPERTY PRICE MAP + SPOTLIGHT
# =====================================================
st.markdown('<div class="section-heading">📍 Sector-wise Property Price Map</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">Bubble size reflects built-up area; color indicates rate per sqft. Click any sector dot to inspect its valuation profile.</div>',
    unsafe_allow_html=True,
)

required_columns = ["sector", "price", "price_per_sqft", "built_up_area", "latitude", "longitude"]
missing_columns = [col for col in required_columns if col not in new_df.columns]

if missing_columns:
    st.error(f"Missing columns in data_viz1.csv: {missing_columns}")
else:
    group_df = (
        new_df.groupby("sector", as_index=False)
        .agg(
            price=("price", "mean"),
            price_per_sqft=("price_per_sqft", "mean"),
            built_up_area=("built_up_area", "mean"),
            latitude=("latitude", "mean"),
            longitude=("longitude", "mean"),
            listings=("price", "count"),
        )
        .dropna(subset=["latitude", "longitude", "price_per_sqft"])
    )

    group_df = group_df[
        group_df["latitude"].between(28.30, 28.55)
        & group_df["longitude"].between(76.85, 77.20)
    ].reset_index(drop=True)

    if not group_df.empty:
        map_col, side_col = st.columns([2.2, 1])

        with map_col:
            fig_map = px.scatter_map(
                group_df,
                lat="latitude",
                lon="longitude",
                color="price_per_sqft",
                size="built_up_area",
                text="sector",
                hover_name="sector",
                hover_data={
                    "price": ":,.2f",
                    "price_per_sqft": ":,.0f",
                    "built_up_area": ":,.0f",
                    "listings": True,
                    "latitude": False,
                    "longitude": False,
                },
                labels={
                    "price": "Avg Price (₹ Cr)",
                    "price_per_sqft": "Price / Sqft (₹)",
                    "built_up_area": "Built-up Area (sqft)",
                    "listings": "Listings",
                },
                color_continuous_scale="Tealrose",
                zoom=10.2,
                center={"lat": 28.4595, "lon": 77.0266},
                map_style="carto-positron",
                size_max=19,
                height=520,
            )

            fig_map.update_traces(textposition="top right", marker=dict(opacity=0.88))
            fig_map.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor="#ffffff",
                font=dict(color="#0c2335"),
                coloraxis_colorbar=dict(
                    title=dict(text="Price / Sqft", font=dict(color="#0c2335")),
                    tickfont=dict(color="#0c2335"),
                    ticksuffix=" ₹",
                ),
            )

            event = st.plotly_chart(
                fig_map,
                use_container_width=True,
                key="gurgaon_sector_map",
                on_select="rerun",
                selection_mode="points",
            )

        with side_col:
            selected_sector_row = None
            if event and event.selection.points:
                selected_index = event.selection.points[0]["point_index"]
                if 0 <= selected_index < len(group_df):
                    selected_sector_row = group_df.iloc[selected_index]

            if selected_sector_row is None:
                selected_sector_row = group_df.sort_values("price_per_sqft", ascending=False).iloc[0]
                badge_label = "Top Premium Benchmark"
            else:
                badge_label = "Selected Sector Spotlight"

            st.markdown(
                textwrap.dedent(f"""
                <div class="spotlight-card">
                    <div class="spotlight-badge">{badge_label}</div>
                    <div class="spotlight-title">{selected_sector_row['sector']}</div>
                    <div class="spotlight-item">
                        <span class="spotlight-label">Avg. Property Price</span>
                        <span class="spotlight-value">₹{selected_sector_row['price']:,.2f} Cr</span>
                    </div>
                    <div class="spotlight-item">
                        <span class="spotlight-label">Avg. Price / Sqft</span>
                        <span class="spotlight-value">₹{selected_sector_row['price_per_sqft']:,.0f}</span>
                    </div>
                    <div class="spotlight-item">
                        <span class="spotlight-label">Avg. Built-up Area</span>
                        <span class="spotlight-value">{selected_sector_row['built_up_area']:,.0f} sqft</span>
                    </div>
                    <div class="spotlight-item">
                        <span class="spotlight-label">Available Listings</span>
                        <span class="spotlight-value">{int(selected_sector_row['listings'])} properties</span>
                    </div>
                </div>
                """),
                unsafe_allow_html=True,
            )

            st.write("")
            top5 = group_df.nlargest(5, "price_per_sqft").sort_values("price_per_sqft")
            fig_top5 = px.bar(
                top5,
                x="price_per_sqft",
                y="sector",
                orientation="h",
                title="Top 5 Sectors by Rate (₹/Sqft)",
                text_auto=",.0f",
                color_discrete_sequence=["#187573"],
            )
            style_chart(fig_top5, height=250)
            fig_top5.update_layout(xaxis_title="", yaxis_title="", margin=dict(l=8, r=16, t=38, b=8))
            st.plotly_chart(fig_top5, use_container_width=True)
    else:
        st.warning("No valid sector location data available.")


# =====================================================
# 9. FURNISHING FACILITIES WORD CLOUD + TOP AMENITIES
# =====================================================
st.markdown('<div class="section-heading">✨ Furnishing Facilities Analysis</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">Discover the most common furnishing and society facilities across Gurgaon sectors.</div>',
    unsafe_allow_html=True,
)

if "sector" not in furnishing_df.columns:
    st.error("The furnishing dataset must contain a sector column.")
else:
    sector_options = ["Overall"] + sorted(furnishing_df["sector"].dropna().unique().tolist())
    default_idx = (
        sector_options.index(selected_sectors[0])
        if len(selected_sectors) == 1 and selected_sectors[0] in sector_options
        else 0
    )

    selected_sector = st.selectbox(
        "Choose a sector",
        sector_options,
        index=default_idx,
        key="furnishing_sector",
    )

    if selected_sector == "Overall":
        sector_data = furnishing_df.copy()
    else:
        sector_data = furnishing_df[furnishing_df["sector"] == selected_sector].copy()

    features = sector_data.drop(columns=["sector", "society"], errors="ignore")
    features = features.apply(pd.to_numeric, errors="coerce").fillna(0)
    frequencies = {k: v for k, v in features.sum().to_dict().items() if v > 0}

    if frequencies:
        wc_col, bar_col = st.columns([1.6, 1])

        with wc_col:
            clean_frequencies = {
                str(k).replace("_", " ").title(): float(v)
                for k, v in frequencies.items()
            }
            wordcloud = WordCloud(
                width=1100,
                height=500,
                background_color="#0d2638",
                colormap="Set3",
                min_font_size=10,
                max_words=100,
            ).generate_from_frequencies(clean_frequencies)

            fig_wc, ax = plt.subplots(figsize=(12, 5.4))
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            fig_wc.patch.set_facecolor("#0d2638")
            plt.tight_layout(pad=0)
            st.pyplot(fig_wc, use_container_width=True)
            plt.close(fig_wc)

        with bar_col:
            top_amen = (
                pd.Series(clean_frequencies)
                .sort_values(ascending=False)
                .head(10)
                .sort_values(ascending=True)
                .reset_index()
            )
            top_amen.columns = ["Facility", "Count"]

            fig_amen = px.bar(
                top_amen,
                x="Count",
                y="Facility",
                orientation="h",
                title=f"Top 10 Facilities ({selected_sector})",
                text_auto=",.0f",
                color_discrete_sequence=["#0f384c"],
            )
            style_chart(fig_amen, height=405)
            fig_amen.update_layout(yaxis_title="", xaxis_title="Properties")
            st.plotly_chart(fig_amen, use_container_width=True)
    else:
        st.warning("No furnishing facilities available for this selection.")


# =====================================================
# 10. BUILT-UP AREA VS PRICE & BHK DISTRIBUTION
# =====================================================
st.markdown('<div class="section-heading">📈 Built-up Area vs Property Price & BHK Share</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">Understand how property size relates to price and explore bedroom configurations across sectors.</div>',
    unsafe_allow_html=True,
)

col_area, col_bhk = st.columns([1.4, 1])

with col_area:
    if "property_type" in new_df.columns:
        type_opts = ["All Types"] + sorted(new_df["property_type"].dropna().unique().tolist())
        chosen_type = st.selectbox("Select Property Type", type_opts, key="area_property_type")

        if chosen_type == "All Types":
            area_df = new_df.dropna(subset=["built_up_area", "price"]).copy()
        else:
            area_df = new_df[
                (new_df["property_type"] == chosen_type)
                & new_df["built_up_area"].notna()
                & new_df["price"].notna()
            ].copy()

        if not area_df.empty:
            fig_area = px.scatter(
                area_df,
                x="built_up_area",
                y="price",
                color="bedRoom" if "bedRoom" in area_df.columns else None,
                hover_data=["sector", "property_type"],
                title=f"{chosen_type} — Area vs Price",
                labels={
                    "built_up_area": "Built-up Area (sqft)",
                    "price": "Property Price (₹ Cr)",
                    "bedRoom": "BHK",
                },
                color_continuous_scale="Teal",
            )
            style_chart(fig_area, height=430)
            fig_area.update_coloraxes(colorbar_tickfont_color="#0c2335", colorbar_title_font_color="#0c2335")
            st.plotly_chart(fig_area, use_container_width=True)
        else:
            st.warning("No properties found for this property type.")

with col_bhk:
    bhk_sector_options = ["Overall"] + sorted(new_df["sector"].dropna().unique().tolist())
    selected_bhk_sector = st.selectbox("Select Sector for BHK Share", bhk_sector_options, key="bhk_sector")

    if selected_bhk_sector == "Overall":
        bhk_df = new_df.copy()
    else:
        bhk_df = new_df[new_df["sector"] == selected_bhk_sector].copy()

    if not bhk_df.empty and "bhk_label" in bhk_df.columns:
        bhk_counts = bhk_df["bhk_label"].dropna().value_counts().reset_index()
        bhk_counts.columns = ["BHK", "Count"]

        fig_bhk = px.pie(
            bhk_counts,
            names="BHK",
            values="Count",
            hole=0.48,
            title=f"BHK Distribution — {selected_bhk_sector}",
            color_discrete_sequence=["#0d2638", "#124559", "#187573", "#38a3a5", "#9ce5d3"],
        )
        fig_bhk.update_traces(textposition="inside", textinfo="percent+label", textfont=dict(color="#ffffff"))
        style_chart(fig_bhk, height=430)
        fig_bhk.update_layout(showlegend=False)
        st.plotly_chart(fig_bhk, use_container_width=True)


# =====================================================
# 11. BHK PRICE COMPARISON & HOUSE VS FLAT DISTRIBUTION
# =====================================================
st.markdown('<div class="section-heading">💰 BHK-wise Price & Property Type Comparison</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">Compare price ranges across 1–4 BHK units and compare house vs flat price distributions.</div>',
    unsafe_allow_html=True,
)

col_box, col_dist = st.columns(2)

with col_box:
    bhk_price_df = new_df[new_df["bedRoom"].between(1, 4)].sort_values("bedRoom").copy()
    if not bhk_price_df.empty:
        fig_box = px.box(
            bhk_price_df,
            x="bhk_label",
            y="price",
            color="bhk_label",
            title="Property Price Range by BHK (1–4 BHK)",
            labels={
                "bhk_label": "Number of Bedrooms",
                "price": "Property Price (₹ Cr)",
            },
            color_discrete_sequence=["#0d2638", "#124559", "#187573", "#38a3a5"],
        )
        style_chart(fig_box, height=440)
        fig_box.update_layout(showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

with col_dist:
    dist_df = new_df.dropna(subset=["price", "property_type"]).copy()
    if not dist_df.empty:
        fig_dist = px.histogram(
            dist_df,
            x="price",
            color="property_type",
            barmode="overlay",
            marginal="box",
            nbins=35,
            opacity=0.68,
            title="House vs Flat Price Distribution",
            labels={
                "price": "Property Price (₹ Cr)",
                "property_type": "Property Type",
            },
            color_discrete_map={"Flat": "#187573", "House": "#0d2638"},
        )
        style_chart(fig_dist, height=440)
        fig_dist.update_layout(
            yaxis_title="Number of Properties",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color="#0c2335"),
            ),
        )
        st.plotly_chart(fig_dist, use_container_width=True)


# =====================================================
# 12. DATA TABLE & CSV EXPORT
# =====================================================
with st.expander("📋 View & Download Filtered Property Data"):
    cols_to_show = [
        c for c in ["sector", "property_type", "bhk_label", "built_up_area", "price", "price_per_sqft"]
        if c in new_df.columns
    ]
    st.dataframe(new_df[cols_to_show].head(250), use_container_width=True)
    st.download_button(
        label="⬇️ Download Filtered Market Report (CSV)",
        data=new_df.to_csv(index=False).encode("utf-8"),
        file_name="gurgaon_market_analytics.csv",
        mime="text/csv",
    )


# =====================================================
# 13. FOOTER
# =====================================================
st.markdown(
    """
    <div class="footer">
        © 2026 Gurgaon Estates Pro | Commercial Real Estate Intelligence Platform
    </div>
    """,
    unsafe_allow_html=True,
)