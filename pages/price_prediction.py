import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Gurgaon Estates | AI Price Prediction",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# PROPTECH INTELLIGENCE THEME CSS (MATCHES SUITE UI)
# =====================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    color-scheme: light !important;
}

/* Main App Canvas */
html, body, .stApp, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #f4f7f9 !important;
    color: #0f172a !important;
}

[data-testid="stHeader"] {
    background-color: rgba(244, 247, 249, 0.85) !important;
}

.block-container {
    max-width: 1380px;
    padding-top: 1.75rem;
    padding-bottom: 3rem;
}

/* =====================================================
   SIDEBAR TOGGLE ARROW (BLACK & HIGH-CONTRAST)
   ===================================================== */
[data-testid="stSidebarHeader"] button,
[data-testid="stSidebarCollapseButton"] button,
[data-testid="collapsedControl"] button,
[data-testid="stExpandSidebarButton"] button,
[data-testid="stSidebar"] button[kind="header"],
[data-testid="stHeader"] button[kind="header"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    color: #000000 !important;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.14) !important;
    opacity: 1 !important;
}

[data-testid="stSidebarHeader"] button:hover,
[data-testid="stSidebarCollapseButton"] button:hover,
[data-testid="collapsedControl"] button:hover,
[data-testid="stExpandSidebarButton"] button:hover,
[data-testid="stSidebar"] button[kind="header"]:hover,
[data-testid="stHeader"] button[kind="header"]:hover {
    background-color: #f1f5f9 !important;
    border-color: #94a3b8 !important;
}

[data-testid="stSidebarHeader"] button span,
[data-testid="stSidebarCollapseButton"] button span,
[data-testid="collapsedControl"] button span,
[data-testid="stExpandSidebarButton"] button span,
[data-testid="stSidebar"] button[kind="header"] span,
[data-testid="stHeader"] button[kind="header"] span,
[data-testid="stSidebarHeader"] [data-testid="stIconMaterial"],
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
[data-testid="collapsedControl"] [data-testid="stIconMaterial"],
[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"],
[data-testid="stHeader"] [data-testid="stIconMaterial"] {
    color: #000000 !important;
}

[data-testid="stSidebarHeader"] button svg,
[data-testid="stSidebarCollapseButton"] button svg,
[data-testid="collapsedControl"] button svg,
[data-testid="stExpandSidebarButton"] button svg,
[data-testid="stSidebar"] button[kind="header"] svg,
[data-testid="stHeader"] button[kind="header"] svg,
[data-testid="collapsedControl"] svg {
    fill: #000000 !important;
    color: #000000 !important;
}

[data-testid="stSidebarHeader"] button svg path,
[data-testid="stSidebarCollapseButton"] button svg path,
[data-testid="collapsedControl"] button svg path,
[data-testid="stExpandSidebarButton"] button svg path,
[data-testid="stSidebar"] button[kind="header"] svg path,
[data-testid="stHeader"] button[kind="header"] svg path,
[data-testid="collapsedControl"] svg path {
    fill: #000000 !important;
    stroke: #000000 !important;
}

/* =====================================================
   SIDEBAR STYLING (DEEP NAVY-TEAL, NEVER BLACK)
   ===================================================== */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #0b2233 0%, #0f2c3f 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

/* Fix All Text & Multipage Links Inside Sidebar (Excluding Toggle Button) */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] span,
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] div,
[data-testid="stSidebarNav"] span {
    color: #e2e8f0 !important;
}

[data-testid="stSidebarNav"] {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    margin-bottom: 1rem !important;
}

[data-testid="stSidebarNav"] a {
    border-radius: 10px !important;
    padding: 0.45rem 0.75rem !important;
    margin: 2px 0.5rem !important;
    transition: background 0.2s ease !important;
}

[data-testid="stSidebarNav"] a:hover {
    background-color: rgba(255, 255, 255, 0.08) !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background-color: rgba(255, 255, 255, 0.14) !important;
    font-weight: 700 !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] span {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* Sidebar Brand & Info Cards */
.sb-brand-wrap {
    padding: 0.25rem 0.25rem 1.1rem 0.25rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 1.2rem;
}
.sb-brand-title {
    color: #ffffff !important;
    font-size: 20px;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: -0.3px;
}
.sb-brand-sub {
    color: #7dd3fc !important;
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    margin-top: 4px;
}
.sb-section-label {
    color: #94a3b8 !important;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 1rem 0 0.6rem 0;
}
.sb-card {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 12px 14px;
    margin-bottom: 10px;
}
.sb-card-label {
    color: #94a3b8 !important;
    font-size: 11px;
    font-weight: 600;
}
.sb-card-val {
    color: #ffffff !important;
    font-size: 16px;
    font-weight: 800;
    margin-top: 2px;
}
.sb-card-hint {
    color: #6ee7b7 !important;
    font-size: 11px;
    font-weight: 600;
    margin-top: 2px;
}

/* =====================================================
   MAIN CONTENT TYPOGRAPHY & INPUT WIDGETS
   ===================================================== */
[data-testid="stAppViewContainer"] .main p,
[data-testid="stAppViewContainer"] .main span,
[data-testid="stAppViewContainer"] .main label,
[data-testid="stAppViewContainer"] .main h1,
[data-testid="stAppViewContainer"] .main h2,
[data-testid="stAppViewContainer"] .main h3,
[data-testid="stAppViewContainer"] .main h4,
[data-testid="stWidgetLabel"] p {
    color: #0f172a;
}

/* Selectbox & Dropdown Menus */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] input,
div[data-baseweb="select"] svg {
    color: #0f172a !important;
    fill: #0f172a !important;
}
ul[data-baseweb="menu"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
}
ul[data-baseweb="menu"] li {
    color: #0f172a !important;
    background-color: #ffffff !important;
}
ul[data-baseweb="menu"] li:hover {
    background-color: #f1f5f9 !important;
}

/* Number Input & Stepper Buttons */
div[data-baseweb="input"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
}
div[data-baseweb="input"] input {
    background-color: #ffffff !important;
    color: #0f172a !important;
    font-weight: 600 !important;
}
[data-testid="stNumberInputStepDown"],
[data-testid="stNumberInputStepUp"] {
    background-color: #f8fafc !important;
    color: #0f172a !important;
    border-left: 1px solid #e2e8f0 !important;
}
[data-testid="stNumberInputStepDown"] svg,
[data-testid="stNumberInputStepUp"] svg {
    fill: #0f172a !important;
}

/* =====================================================
   HERO BANNER (EXACT SUITE GRADIENT & TYPOGRAPHY)
   ===================================================== */
.hero-banner {
    background: linear-gradient(95deg, #0b2233 0%, #103b49 52%, #15625c 100%);
    padding: 38px 44px;
    border-radius: 22px;
    margin-bottom: 28px;
    box-shadow: 0 14px 32px -8px rgba(11, 34, 51, 0.22);
}
.hero-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.16);
    color: #a7f3d0 !important;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.2px;
    padding: 6px 14px;
    border-radius: 999px;
    text-transform: uppercase;
}
.hero-title-white {
    color: #ffffff !important;
    font-size: 38px;
    font-weight: 800;
    margin-top: 16px;
    line-height: 1.15;
    letter-spacing: -0.6px;
}
.hero-title-mint {
    color: #6ee7b7 !important;
    font-size: 38px;
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.6px;
}
.hero-subtitle {
    color: #cbd5e1 !important;
    font-size: 15px;
    line-height: 1.6;
    margin-top: 14px;
    max-width: 680px;
}
.hero-stats-row {
    display: flex;
    flex-wrap: wrap;
    gap: 44px;
    margin-top: 28px;
}
.hero-stat-num {
    color: #ffffff !important;
    font-size: 19px;
    font-weight: 800;
}
.hero-stat-desc {
    color: #94a3b8 !important;
    font-size: 12.5px;
    margin-top: 2px;
}

/* Section Heading Style */
.section-heading {
    color: #0f172a !important;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.3px;
    margin-bottom: 2px;
}
.section-sub {
    color: #64748b !important;
    font-size: 14px;
    margin-bottom: 16px;
}

/* Form Group Headers */
.form-group-title {
    color: #0f766e !important;
    font-size: 12px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-top: 12px;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid #e2e8f0;
}

/* Primary CTA Button */
.stButton > button {
    background: linear-gradient(95deg, #0f766e 0%, #15625c 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.78rem 1.5rem !important;
    font-size: 15.5px !important;
    font-weight: 800 !important;
    box-shadow: 0 6px 18px rgba(15, 118, 110, 0.25) !important;
    transition: all 0.2s ease !important;
}
.stButton > button p {
    color: #ffffff !important;
    font-weight: 800 !important;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 24px rgba(15, 118, 110, 0.35) !important;
}

/* Download Button */
.stDownloadButton > button {
    background-color: #0b2233 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.2rem !important;
    font-weight: 700 !important;
}
.stDownloadButton > button p {
    color: #ffffff !important;
}

/* =====================================================
   VALUATION HERO CARD & KPI CARDS
   ===================================================== */
.valuation-card {
    background: linear-gradient(125deg, #0b2233 0%, #103b49 55%, #15625c 100%);
    border-radius: 20px;
    padding: 28px 30px;
    box-shadow: 0 12px 28px rgba(11, 34, 51, 0.16);
    margin-bottom: 18px;
}
.val-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.1);
    color: #a7f3d0 !important;
    border: 1px solid rgba(255, 255, 255, 0.18);
    font-size: 11px;
    font-weight: 700;
    padding: 5px 12px;
    border-radius: 999px;
    letter-spacing: 1.4px;
    text-transform: uppercase;
}
.val-sub-label {
    color: #cbd5e1 !important;
    font-size: 13.5px;
    font-weight: 500;
    margin-top: 14px;
}
.val-range {
    color: #ffffff !important;
    font-size: 35px;
    font-weight: 800;
    line-height: 1.15;
    margin-top: 4px;
    letter-spacing: -0.5px;
}
.val-range span {
    color: #6ee7b7 !important;
}
.val-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 20px;
    padding-top: 18px;
    border-top: 1px solid rgba(255, 255, 255, 0.14);
}
.val-mini-label {
    color: #94a3b8 !important;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    font-weight: 600;
}
.val-mini-num {
    color: #ffffff !important;
    font-size: 17px;
    font-weight: 800;
    margin-top: 3px;
}

/* Custom KPI Cards */
.kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 5px solid #0d9488;
    border-radius: 16px;
    padding: 16px 18px;
    box-shadow: 0 3px 10px rgba(15, 23, 42, 0.03);
    margin-bottom: 16px;
}
.kpi-title {
    color: #64748b !important;
    font-size: 12.5px;
    font-weight: 600;
}
.kpi-value {
    color: #0f172a !important;
    font-size: 23px;
    font-weight: 800;
    margin-top: 4px;
    margin-bottom: 8px;
    letter-spacing: -0.4px;
}
.kpi-pill {
    display: inline-block;
    background-color: #e6f4f1;
    color: #0f766e !important;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 999px;
}

/* White Form Container */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #ffffff !important;
    border-radius: 20px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04) !important;
}

div[data-testid="stPlotlyChart"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 18px !important;
    padding: 12px !important;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.03) !important;
}

.footer {
    text-align: center;
    color: #64748b !important;
    padding-top: 28px;
    font-size: 13px;
    border-top: 1px solid #e2e8f0;
    margin-top: 36px;
}
</style>
""",
    unsafe_allow_html=True,
)


# =====================================================
# LOAD MODEL & DATASET (CACHED)
# =====================================================
@st.cache_data
def load_dataset():
    with open("datasets/df.pkl", "rb") as file:
        return pickle.load(file)


@st.cache_resource
def load_pipeline():
    with open("datasets/pipeline.pkl", "rb") as file:
        return pickle.load(file)


try:
    df = load_dataset()
    pipeline = load_pipeline()
except FileNotFoundError as e:
    st.error(f"Required model/dataset file missing: {e}")
    st.stop()


# =====================================================
# SIDEBAR BRANDING & MARKET SNAPSHOT
# =====================================================
total_listings = len(df)
total_sectors = df["sector"].nunique() if "sector" in df.columns else 0
median_market_price = float(pd.to_numeric(df["price"], errors="coerce").median()) if "price" in df.columns else 0.0

with st.sidebar:
    st.markdown(
        """
<div class="sb-brand-wrap">
    <div class="sb-brand-title">🏠 Gurgaon Estates</div>
    <div class="sb-brand-sub">PropTech Intelligence</div>
</div>
<div class="sb-section-label">Valuation Engine</div>
<div class="sb-card">
    <div class="sb-card-label">Training Corpus</div>
    <div class="sb-card-val">{:,} Properties</div>
    <div class="sb-card-hint">● Active ML Pipeline</div>
</div>
<div class="sb-card">
    <div class="sb-card-label">Micro-Market Coverage</div>
    <div class="sb-card-val">{}+ Sectors</div>
    <div class="sb-card-hint">Citywide Median: ₹{:.2f} Cr</div>
</div>
""".format(total_listings, total_sectors, median_market_price),
        unsafe_allow_html=True,
    )


# =====================================================
# HERO BANNER (MATCHES SUITE DESIGN)
# =====================================================
st.markdown(
    f"""
<div class="hero-banner">
    <div class="hero-badge">Gurgaon Real Estate Intelligence • 2026</div>
    <div class="hero-title-white">AI Property Valuation &amp;</div>
    <div class="hero-title-mint">Fair Market Estimator.</div>
    <div class="hero-subtitle">
        Configure residential specifications below to generate an institutional-grade ML valuation range, implied per-sqft rate, and live micro-market benchmark across Gurgaon sectors.
    </div>
    <div class="hero-stats-row">
        <div>
            <div class="hero-stat-num">{total_sectors}+ Sectors</div>
            <div class="hero-stat-desc">Gurgaon Micro-Markets Covered</div>
        </div>
        <div>
            <div class="hero-stat-num">{total_listings:,} Listings</div>
            <div class="hero-stat-desc">Verified Training Inventory</div>
        </div>
        <div>
            <div class="hero-stat-num">ML-Powered</div>
            <div class="hero-stat-desc">Instant Fair Price Valuation</div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# =====================================================
# MAIN WORKSPACE: LEFT (INPUTS) | RIGHT (VALUATION)
# =====================================================
left_col, right_col = st.columns([1.18, 1], gap="large")

with left_col:
    with st.container(border=True):
        st.markdown('<div class="section-heading">Configure Property Specifications</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-sub">Select exact residential attributes to compute a tailored fair market valuation.</div>',
            unsafe_allow_html=True,
        )

        # --- Group 1: Location & Core Dimensions ---
        st.markdown('<div class="form-group-title">1. Location &amp; Core Dimensions</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)

        with c1:
            property_type_display = st.selectbox(
                "Property Category",
                options=["Flat", "House"],
                index=0,
            )
            property_type = property_type_display.lower()

        with c2:
            sector_options = sorted(df["sector"].dropna().unique().tolist())
            sector = st.selectbox("Gurgaon Sector", options=sector_options)

        c3, c4 = st.columns(2)
        with c3:
            default_area = float(df["built_up_area"].median()) if "built_up_area" in df.columns else 1500.0
            built_up_area = float(
                st.number_input(
                    "Built-Up Area (sq.ft.)",
                    min_value=100.0,
                    max_value=50000.0,
                    value=round(default_area, 0),
                    step=50.0,
                )
            )

        with c4:
            age_options = sorted(df["agePossession"].dropna().unique().tolist())
            property_age = st.selectbox("Property Age / Possession", options=age_options)

        # --- Group 2: Layout & Room Configuration ---
        st.markdown('<div class="form-group-title">2. Layout &amp; Room Configuration</div>', unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)

        with r1:
            bedroom_options = sorted(df["bedRoom"].dropna().unique().tolist())
            default_bed_idx = (
                bedroom_options.index(3.0)
                if 3.0 in bedroom_options
                else (bedroom_options.index(3) if 3 in bedroom_options else 0)
            )
            bedrooms = float(
                st.selectbox(
                    "Bedrooms (BHK)",
                    options=bedroom_options,
                    index=default_bed_idx,
                    format_func=lambda x: f"{int(x)} BHK",
                )
            )

        with r2:
            bathroom_options = sorted(df["bathroom"].dropna().unique().tolist())
            default_bath_idx = (
                bathroom_options.index(3.0)
                if 3.0 in bathroom_options
                else (bathroom_options.index(3) if 3 in bathroom_options else 0)
            )
            bathroom = float(
                st.selectbox(
                    "Bathrooms",
                    options=bathroom_options,
                    index=default_bath_idx,
                    format_func=lambda x: f"{int(x)} Bath",
                )
            )

        with r3:
            balcony_options = sorted(df["balcony"].dropna().unique().tolist(), key=str)
            balcony = st.selectbox("Balconies", options=balcony_options)

        # --- Group 3: Interiors, Floor & Utility Rooms ---
        st.markdown('<div class="form-group-title">3. Interiors, Floor &amp; Utility Rooms</div>', unsafe_allow_html=True)
        f1, f2, f3 = st.columns(3)

        with f1:
            furnishing_options = sorted(df["furnishing_type"].dropna().unique().tolist())
            furnishing_type = st.selectbox("Furnishing Status", options=furnishing_options)

        with f2:
            luxury_options = sorted(df["luxury_category"].dropna().unique().tolist())
            luxury_category = st.selectbox("Luxury Tier", options=luxury_options)

        with f3:
            floor_options = sorted(df["floor_category"].dropna().unique().tolist())
            floor_category = st.selectbox("Floor Elevation", options=floor_options)

        u1, u2 = st.columns(2)
        with u1:
            servant_room = float(
                st.selectbox(
                    "Servant Room",
                    options=[0.0, 1.0],
                    format_func=lambda x: "Included (Yes)" if x == 1.0 else "Not Included (No)",
                )
            )

        with u2:
            store_room = float(
                st.selectbox(
                    "Store Room",
                    options=[0.0, 1.0],
                    format_func=lambda x: "Included (Yes)" if x == 1.0 else "Not Included (No)",
                )
            )

        st.write("")
        predict_clicked = st.button("✨ Generate Fair Market Valuation", use_container_width=True)


# =====================================================
# PREDICTION & BENCHMARKING ENGINE
# =====================================================
columns = [
    "property_type",
    "sector",
    "bedRoom",
    "bathroom",
    "balcony",
    "agePossession",
    "built_up_area",
    "servant room",
    "store room",
    "furnishing_type",
    "luxury_category",
    "floor_category",
]

input_data = [[
    property_type,
    sector,
    bedrooms,
    bathroom,
    balcony,
    property_age,
    built_up_area,
    servant_room,
    store_room,
    furnishing_type,
    luxury_category,
    floor_category,
]]

one_df = pd.DataFrame(input_data, columns=columns)

if predict_clicked or "last_valuation" not in st.session_state:
    base_price = float(np.expm1(pipeline.predict(one_df))[0])
    low = max(0.05, base_price - 0.22)
    high = base_price + 0.22
    rate_per_sqft = (base_price * 1e7) / built_up_area if built_up_area > 0 else 0.0

    st.session_state["last_valuation"] = {
        "property_type_display": property_type_display,
        "sector": sector,
        "bedrooms": int(bedrooms),
        "bathroom": int(bathroom),
        "balcony": balcony,
        "built_up_area": built_up_area,
        "property_age": property_age,
        "furnishing_type": furnishing_type,
        "luxury_category": luxury_category,
        "floor_category": floor_category,
        "servant_room": "Yes" if servant_room == 1.0 else "No",
        "store_room": "Yes" if store_room == 1.0 else "No",
        "base_price": base_price,
        "low": low,
        "high": high,
        "rate_per_sqft": rate_per_sqft,
    }
    if predict_clicked:
        st.toast("Fair market valuation updated!", icon="✅")

val = st.session_state["last_valuation"]


# =====================================================
# RIGHT COLUMN: VALUATION CERTIFICATE & SECTOR BENCHMARK
# =====================================================
with right_col:
    # 1. Primary Valuation Hero Card
    st.markdown(
        f"""
<div class="valuation-card">
    <div class="val-badge">AI Valuation Estimate • {val['property_type_display']}</div>
    <div class="val-sub-label">Estimated Fair Market Price Range in <strong style="color:#ffffff;">{val['sector']}</strong></div>
    <div class="val-range">₹{val['low']:,.2f} Cr – <span>₹{val['high']:,.2f} Cr</span></div>
    <div class="val-grid">
        <div>
            <div class="val-mini-label">Point Estimate</div>
            <div class="val-mini-num">₹{val['base_price']:,.2f} Cr</div>
        </div>
        <div>
            <div class="val-mini-label">Implied Rate</div>
            <div class="val-mini-num">₹{val['rate_per_sqft']:,.0f}/sqft</div>
        </div>
        <div>
            <div class="val-mini-label">Configuration</div>
            <div class="val-mini-num">{val['bedrooms']} BHK • {val['built_up_area']:,.0f} sqft</div>
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # 2. Sector Market Comparison Cards
    sector_df = df[df["sector"] == val["sector"]].copy()

    if not sector_df.empty and "price" in sector_df.columns:
        sec_prices = pd.to_numeric(sector_df["price"], errors="coerce").dropna()

        if not sec_prices.empty:
            sec_median = float(sec_prices.median())
            sec_avg = float(sec_prices.mean())
            sec_min = float(sec_prices.min())
            sec_max = float(sec_prices.max())

            if "price_per_sqft" in sector_df.columns:
                sec_rate_med = pd.to_numeric(sector_df["price_per_sqft"], errors="coerce").median()
                sec_rate_avg = pd.to_numeric(sector_df["price_per_sqft"], errors="coerce").mean()
                rate_val_str = f"₹{sec_rate_med:,.0f}" if pd.notna(sec_rate_med) else "N/A"
                rate_pill_str = f"Mean: ₹{sec_rate_avg:,.0f}/sqft" if pd.notna(sec_rate_avg) else "Sector Benchmark"
            else:
                rate_val_str = f"₹{sec_min:,.1f}–{sec_max:,.1f} Cr"
                rate_pill_str = "Min–Max Range"

            k1, k2, k3 = st.columns(3)
            with k1:
                st.markdown(
                    f"""
<div class="kpi-card">
    <div class="kpi-title">Sector Median Price</div>
    <div class="kpi-value">₹{sec_median:,.2f} Cr</div>
    <div class="kpi-pill">Mean: ₹{sec_avg:,.2f} Cr</div>
</div>
""",
                    unsafe_allow_html=True,
                )
            with k2:
                st.markdown(
                    f"""
<div class="kpi-card">
    <div class="kpi-title">Sector Rate / Sqft</div>
    <div class="kpi-value">{rate_val_str}</div>
    <div class="kpi-pill">{rate_pill_str}</div>
</div>
""",
                    unsafe_allow_html=True,
                )
            with k3:
                st.markdown(
                    f"""
<div class="kpi-card">
    <div class="kpi-title">Sector Comps</div>
    <div class="kpi-value">{len(sec_prices):,}</div>
    <div class="kpi-pill">Verified Listings</div>
</div>
""",
                    unsafe_allow_html=True,
                )

            # Visual Position Chart within Sector
            fig_gauge = go.Figure()

            fig_gauge.add_trace(
                go.Box(
                    x=sec_prices,
                    name=val["sector"],
                    orientation="h",
                    marker_color="#94a3b8",
                    fillcolor="rgba(148, 163, 184, 0.25)",
                    line=dict(color="#475569", width=1.5),
                    boxpoints=False,
                    hoverinfo="x",
                )
            )

            fig_gauge.add_trace(
                go.Scatter(
                    x=[val["base_price"]],
                    y=[val["sector"]],
                    mode="markers+text",
                    name="Your Estimate",
                    text=[f"₹{val['base_price']:,.2f} Cr"],
                    textposition="top center",
                    textfont=dict(color="#0f766e", size=13, family="Plus Jakarta Sans, sans-serif"),
                    marker=dict(color="#0d9488", size=15, symbol="diamond", line=dict(color="#ffffff", width=2)),
                )
            )

            fig_gauge.update_layout(
                title=dict(
                    text=f"Valuation Position vs. {val['sector']} Market",
                    font=dict(size=15, color="#0f172a", family="Plus Jakarta Sans, sans-serif"),
                ),
                template="plotly_white",
                paper_bgcolor="#ffffff",
                plot_bgcolor="#ffffff",
                height=235,
                showlegend=False,
                margin=dict(l=14, r=14, t=44, b=24),
                xaxis=dict(
                    title=dict(text="Property Price (₹ Cr)", font=dict(color="#334155")),
                    tickfont=dict(color="#334155"),
                    gridcolor="#f1f5f9",
                ),
                yaxis=dict(showticklabels=False),
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

    # 3. Exportable Valuation Summary Report
    report_df = pd.DataFrame(
        [
            {
                "Property Category": val["property_type_display"],
                "Sector": val["sector"],
                "Configuration": f"{val['bedrooms']} BHK, {val['bathroom']} Bath, {val['balcony']} Balcony",
                "Built-Up Area (sqft)": val["built_up_area"],
                "Age / Possession": val["property_age"],
                "Furnishing": val["furnishing_type"],
                "Luxury Tier": val["luxury_category"],
                "Floor Elevation": val["floor_category"],
                "Servant Room": val["servant_room"],
                "Store Room": val["store_room"],
                "Estimated Low (Cr)": round(val["low"], 2),
                "Point Estimate (Cr)": round(val["base_price"], 2),
                "Estimated High (Cr)": round(val["high"], 2),
                "Implied Rate (INR/sqft)": round(val["rate_per_sqft"], 0),
            }
        ]
    )

    st.download_button(
        label="📄 Download Official Valuation Summary (CSV)",
        data=report_df.to_csv(index=False).encode("utf-8"),
        file_name=f"valuation_{val['sector'].replace(' ', '_')}_{val['bedrooms']}BHK.csv",
        mime="text/csv",
        use_container_width=True,
    )


# =====================================================
# FOOTER
# =====================================================
st.markdown(
    """
<div class="footer">
    © 2026 Gurgaon Estates • PropTech Intelligence &amp; AI Valuation Suite
</div>
""",
    unsafe_allow_html=True,
)

# =====================================================
# ENSURE SIDEBAR STARTS OPEN ON INITIAL PAGE LOAD
# (User can still hide/collapse it anytime via the arrow)
# =====================================================
components.html(
    """
    <script>
    (function() {
        const parentDoc = window.parent.document;
        const currentPath = window.parent.location.pathname;
        if (window.parent.__lastOpenedSidebarPath !== currentPath) {
            window.parent.__lastOpenedSidebarPath = currentPath;
            let attempts = 0;
            const ensureOpen = setInterval(() => {
                attempts++;
                const expandBtn =
                    parentDoc.querySelector('[data-testid="stExpandSidebarButton"] button') ||
                    parentDoc.querySelector('[data-testid="collapsedControl"] button') ||
                    parentDoc.querySelector('[data-testid="collapsedControl"]');
                const sidebar = parentDoc.querySelector('[data-testid="stSidebar"]');
                const isCollapsed = sidebar && sidebar.getAttribute('aria-expanded') === 'false';

                if (expandBtn && (isCollapsed || expandBtn.offsetParent !== null)) {
                    expandBtn.click();
                    clearInterval(ensureOpen);
                } else if ((sidebar && sidebar.getAttribute('aria-expanded') === 'true') || attempts > 15) {
                    clearInterval(ensureOpen);
                }
            }, 120);
        }
    })();
    </script>
    """,
    height=0,
    width=0,
)