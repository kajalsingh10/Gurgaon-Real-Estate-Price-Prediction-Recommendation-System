import streamlit as st

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Gurgaon Estates | Real Estate Intelligence",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Global App Styling */
.stApp {
    background-color: #f4f7fa;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Transparent top header so sidebar toggle remains accessible */
header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.block-container {
    max-width: 1240px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* ==================================================
   SIDEBAR STYLING
   ================================================== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2942 0%, #133b52 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

[data-testid="stSidebar"] * {
    color: #f1f5f9;
}

.sidebar-brand {
    padding: 0.5rem 0 1.25rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    margin-bottom: 1.25rem;
}

.sidebar-brand-title {
    font-size: 22px;
    font-weight: 800;
    color: #ffffff !important;
    letter-spacing: -0.5px;
}

.sidebar-brand-sub {
    font-size: 12px;
    color: #94d2bd !important;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 2px;
}

.sidebar-section-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #94a3b8 !important;
    margin: 1rem 0 0.5rem 0;
}

/* Sidebar Navigation Buttons */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255, 255, 255, 0.06);
    color: #e2e8f0 !important;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 0.6rem 0.9rem;
    font-weight: 600;
    font-size: 14px;
    text-align: left;
    justify-content: flex-start;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #176b72;
    border-color: #2a9d8f;
    color: #ffffff !important;
    transform: translateX(3px);
}

.sidebar-stat-card {
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 14px;
    margin-top: 1rem;
}

.sidebar-stat-title {
    font-size: 12px;
    font-weight: 700;
    color: #a9e5d8 !important;
    margin-bottom: 6px;
}

.sidebar-stat-text {
    font-size: 12.5px;
    line-height: 1.5;
    color: #cbd5e1 !important;
}

/* ==================================================
   HERO SECTION
   ================================================== */
.hero-box {
    background: radial-gradient(circle at top right, #1f8a8c 0%, #102a43 65%);
    padding: 52px 48px;
    border-radius: 24px;
    margin-bottom: 42px;
    box-shadow: 0 20px 40px -15px rgba(16, 42, 67, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.hero-badge {
    display: inline-block;
    background: rgba(169, 229, 216, 0.15);
    border: 1px solid rgba(169, 229, 216, 0.35);
    color: #a9e5d8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2.5px;
    padding: 6px 14px;
    border-radius: 999px;
}

.hero-heading {
    color: #ffffff;
    font-size: 44px;
    font-weight: 800;
    line-height: 1.18;
    margin: 20px 0 16px 0;
    letter-spacing: -0.8px;
}

.hero-heading span {
    color: #a9e5d8;
}

.hero-description {
    color: #dbeafe;
    font-size: 17px;
    line-height: 1.65;
    max-width: 680px;
    margin-bottom: 28px;
}

.hero-metrics {
    display: flex;
    flex-wrap: wrap;
    gap: 28px;
    padding-top: 22px;
    border-top: 1px solid rgba(255, 255, 255, 0.14);
}

.metric-item {
    display: flex;
    flex-direction: column;
}

.metric-value {
    color: #ffffff;
    font-size: 22px;
    font-weight: 800;
}

.metric-label {
    color: #94d2bd;
    font-size: 12.5px;
    font-weight: 500;
}

/* ==================================================
   SECTION HEADINGS
   ================================================== */
.section-heading {
    color: #102a43;
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.4px;
    margin-bottom: 6px;
}

.section-description {
    color: #64748b;
    font-size: 15px;
    margin-bottom: 24px;
}

/* ==================================================
   CARDS & BUTTONS
   ================================================== */
.feature-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 26px;
    min-height: 215px;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 16px 30px -10px rgba(16, 42, 67, 0.12);
    border-color: #176b72;
}

.icon-wrap {
    width: 52px;
    height: 52px;
    border-radius: 14px;
    background: #eaf4f2;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    margin-bottom: 16px;
}

.feature-title {
    color: #102a43;
    font-size: 19px;
    font-weight: 700;
    margin-bottom: 8px;
}

.feature-description {
    color: #64748b;
    font-size: 14px;
    line-height: 1.6;
}

/* Main Content Buttons */
.main .stButton > button {
    width: 100%;
    background: #176b72;
    color: #ffffff;
    border: none;
    border-radius: 12px;
    padding: 0.7rem 1rem;
    font-weight: 700;
    font-size: 14px;
    box-shadow: 0 4px 10px rgba(23, 107, 114, 0.2);
    transition: all 0.2s ease;
}

.main .stButton > button:hover {
    background: #102a43;
    color: #ffffff;
    transform: translateY(-2px);
    box-shadow: 0 6px 14px rgba(16, 42, 67, 0.25);
}

/* ==================================================
   CTA & FOOTER
   ================================================== */
.cta-box {
    background: linear-gradient(120deg, #eaf4f2 0%, #e0f2fe 100%);
    border: 1px solid #cce3de;
    border-left: 5px solid #176b72;
    border-radius: 16px;
    padding: 26px 30px;
    margin-top: 40px;
    color: #102a43;
}

.cta-title {
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 6px;
}

.cta-text {
    font-size: 14.5px;
    color: #334e68;
    line-height: 1.6;
}

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
    padding-top: 42px;
    border-top: 1px solid #e2e8f0;
    margin-top: 42px;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# SIDEBAR NAVIGATION & MARKET PULSE
# ==================================================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">🏡 Gurgaon Estates</div>
        <div class="sidebar-brand-sub">PropTech Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">Navigation</div>', unsafe_allow_html=True)

    if st.button("🏠  Home Overview", use_container_width=True, key="nav_home"):
        st.rerun()

    if st.button("📊  Market Analytics", use_container_width=True, key="nav_analytics"):
        st.switch_page("pages/Analytics.py")

    if st.button("💰  Price Prediction", use_container_width=True, key="nav_prediction"):
        st.switch_page(st.switch_page("pages/price_prediction.py"))

    if st.button("🔎  Property Recommendations", use_container_width=True, key="nav_recommendation"):
        st.switch_page("pages/Recommendation.py")

    st.markdown('<div class="sidebar-section-label">Market Snapshot</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-stat-card">
        <div class="sidebar-stat-title">🔥 High-Growth Corridors</div>
        <div class="sidebar-stat-text">
            • Golf Course Extension Rd<br>
            • Dwarka Expressway<br>
            • Southern Peripheral Rd (SPR)<br>
            • New Gurgaon (Sectors 82–95)
        </div>
    </div>
    """, unsafe_allow_html=True)
    


# ==================================================
# HERO SECTION
# ==================================================

st.markdown("""
<div class="hero-box">
    <div class="hero-badge">DISCOVER • INVEST • LIVE</div>
    <div class="hero-heading">
        Find a Place You'll<br><span>Love to Call Home.</span>
    </div>
    <div class="hero-description">
        Explore Gurgaon real estate with intelligent analytics. Compare sector-wise
        price trends, forecast fair property valuations, and uncover homes tailored
        to your lifestyle.
    </div>
    <div class="hero-metrics">
        <div class="metric-item">
            <span class="metric-value">85+</span>
            <span class="metric-label">Gurgaon Sectors Covered</span>
        </div>
        <div class="metric-item">
            <span class="metric-value">ML-Powered</span>
            <span class="metric-label">Instant Price Valuation</span>
        </div>
        <div class="metric-item">
            <span class="metric-value">Smart Match</span>
            <span class="metric-label">Personalized Recommendations</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==================================================
# CORE MODULES (NAVIGATION CARDS)
# ==================================================

st.markdown('<div class="section-heading">Explore Gurgaon Real Estate</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">Everything you need to make smarter property decisions, all in one place.</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-wrap">📊</div>
        <div class="feature-title">Market Analytics</div>
        <div class="feature-description">
            Explore Gurgaon property trends, price-per-sq.ft distributions,
            top-performing sectors, and deep market insights.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Explore Analytics →", key="analytics"):
        st.switch_page("pages/Analytics.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-wrap">💰</div>
        <div class="feature-title">Price Prediction</div>
        <div class="feature-description">
            Estimate accurate property prices using machine learning based
            on sector, area, configuration, and amenities.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Predict Price →", key="prediction"):
        st.switch_page("pages/Price_Prediction.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-wrap">🏡</div>
        <div class="feature-title">Property Recommendations</div>
        <div class="feature-description">
            Discover similar societies and residential options matched to
            your preferred locality, budget, and lifestyle.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Discover Properties →", key="recommendation"):
        st.switch_page("pages/Recommendation.py")


# ==================================================
# WHY CHOOSE OUR PLATFORM
# ==================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-heading">Make Smarter Property Decisions</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-description">Built to remove guesswork from buying and investing in NCR.</div>',
    unsafe_allow_html=True
)

a, b, c = st.columns(3, gap="large")

with a:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-wrap">📍</div>
        <div class="feature-title">Location Insights</div>
        <div class="feature-description">
            Evaluate metro connectivity, expressway access, and nearby social
            infrastructure across Gurgaon sectors.
        </div>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-wrap">📈</div>
        <div class="feature-title">Data-Driven Analysis</div>
        <div class="feature-description">
            Back every investment with historical pricing patterns and
            sector-level supply-demand benchmarks.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown("""
    <div class="feature-card">
        <div class="icon-wrap">🎯</div>
        <div class="feature-title">Personalized Discovery</div>
        <div class="feature-description">
            Cut through thousands of listings with similarity-based
            recommendations tailored to your exact criteria.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# CALL TO ACTION & FOOTER
# ==================================================

st.markdown("""
<div class="cta-box">
    <div class="cta-title">🏡 Your Next Home Starts Here</div>
    <div class="cta-text">
        Use the sidebar or the module cards above to analyze Gurgaon market trends,
        benchmark property prices, and shortlist high-potential homes.
    </div>
</div>

<div class="footer">
    © 2026 Gurgaon Estates | Real Estate Intelligence Platform
</div>
""", unsafe_allow_html=True)
st.markdown("""
<style>
button[data-testid="stSidebarCollapsedControl"] {
    color: black !important;
    background-color: white !important;
}
</style>
""", unsafe_allow_html=True)