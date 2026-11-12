import os
import math
import re
import time
import pickle
import requests
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(
    page_title="Gurgaon Estates | Property Recommendations",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 1. EXACT 104 SECTORS FROM gurgaon_properties_outlier_treated (1).csv
#    (Strictly restricted — no extra sectors added)
# -----------------------------------------------------------------------------
ALLOWED_SECTORS = [
    'dwarka expressway', 'gwal pahari', 'manesar', 'sector 1', 'sector 10',
    'sector 102', 'sector 103', 'sector 104', 'sector 105', 'sector 106',
    'sector 107', 'sector 108', 'sector 109', 'sector 11', 'sector 110',
    'sector 111', 'sector 112', 'sector 113', 'sector 12', 'sector 13',
    'sector 14', 'sector 15', 'sector 17', 'sector 2', 'sector 21',
    'sector 22', 'sector 23', 'sector 24', 'sector 25', 'sector 26',
    'sector 27', 'sector 28', 'sector 3', 'sector 30', 'sector 31',
    'sector 33', 'sector 36', 'sector 37', 'sector 37d', 'sector 38',
    'sector 39', 'sector 4', 'sector 40', 'sector 41', 'sector 43',
    'sector 45', 'sector 46', 'sector 47', 'sector 48', 'sector 49',
    'sector 5', 'sector 50', 'sector 51', 'sector 52', 'sector 53',
    'sector 54', 'sector 55', 'sector 56', 'sector 57', 'sector 58',
    'sector 59', 'sector 6', 'sector 60', 'sector 61', 'sector 62',
    'sector 63', 'sector 63a', 'sector 65', 'sector 66', 'sector 67',
    'sector 67a', 'sector 68', 'sector 69', 'sector 7', 'sector 70',
    'sector 70a', 'sector 71', 'sector 72', 'sector 73', 'sector 74',
    'sector 76', 'sector 77', 'sector 78', 'sector 79', 'sector 8',
    'sector 80', 'sector 81', 'sector 82', 'sector 82a', 'sector 83',
    'sector 84', 'sector 85', 'sector 86', 'sector 88', 'sector 88a',
    'sector 89', 'sector 9', 'sector 90', 'sector 91', 'sector 92',
    'sector 93', 'sector 95', 'sector 99', 'sohna road'
]

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS (Light Canvas + Gurgaon Estates Theme)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

    .stApp { background-color: #F4F7F9 !important; color: #0F293A !important; }
    header[data-testid="stHeader"] { background-color: transparent !important; }

    /* Deep Navy Sidebar */
    section[data-testid="stSidebar"] { background-color: #0F293A !important; border-right: 1px solid #1B3B50; }
    section[data-testid="stSidebar"] * { color: #F8FAFC !important; }
    .sb-brand { padding: 0.4rem 0 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.12); margin-bottom: 1rem; }
    .sb-title { font-size: 1.2rem; font-weight: 800; color: #FFFFFF !important; }
    .sb-sub { font-size: 0.68rem; letter-spacing: 0.14em; color: #7FA1B5 !important; font-weight: 700; margin-top: 3px; }
    .sb-label { font-size: 0.68rem; letter-spacing: 0.12em; color: #7FA1B5 !important; font-weight: 700; margin: 1rem 0 0.5rem 0; }
    .sb-stat { background: #143246; border: 1px solid #20465E; border-radius: 10px; padding: 10px 14px; margin-bottom: 8px; }
    .sb-stat-val { font-size: 1.1rem; font-weight: 800; color: #5CE1B8 !important; }
    .sb-stat-lbl { font-size: 0.75rem; color: #9FB8C7 !important; }

    /* Gradient Hero Banner */
    .hero-box {
        background: linear-gradient(115deg, #0C2838 0%, #103F4E 55%, #166970 100%);
        border-radius: 18px; padding: 2rem 2.4rem; color: #FFFFFF;
        box-shadow: 0 12px 28px rgba(12, 40, 56, 0.12); margin-bottom: 1.5rem;
    }
    .hero-pill {
        display: inline-block; background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2);
        color: #CBD5E1; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em;
        padding: 4px 14px; border-radius: 999px; margin-bottom: 0.9rem;
    }
    .hero-h1 { font-size: 2rem; font-weight: 800; line-height: 1.2; margin: 0 0 0.7rem 0; color: #FFFFFF; }
    .hero-h1 span { color: #5CE1B8; }
    .hero-p { font-size: 0.94rem; color: #CBD5E1; max-width: 680px; line-height: 1.6; margin-bottom: 1.3rem; }
    .hero-stats { display: flex; flex-wrap: wrap; gap: 2.2rem; padding-top: 0.9rem; border-top: 1px solid rgba(255,255,255,0.14); }
    .hero-st-title { font-size: 1.05rem; font-weight: 800; color: #FFFFFF; }
    .hero-st-sub { font-size: 0.76rem; color: #94B8C4; }

    /* Elevated White Cards & Inputs */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important; border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important; padding: 1.25rem !important;
        box-shadow: 0 4px 16px rgba(15, 41, 58, 0.04) !important;
    }
    label[data-testid="stWidgetLabel"] p { color: #1E293B !important; font-weight: 600 !important; }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #F8FAFC !important; border-color: #CBD5E1 !important;
        border-radius: 10px !important; color: #0F293A !important;
    }
    div.stButton > button {
        width: 100%; background: linear-gradient(135deg, #0F293A 0%, #166970 100%) !important;
        color: #FFFFFF !important; border: none !important; border-radius: 10px !important;
        padding: 0.65rem 1.2rem !important; font-weight: 700 !important;
    }

    /* Legend & Result Cards */
    .map-legend {
        display: flex; gap: 16px; font-size: 0.78rem; color: #475569;
        background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;
        padding: 6px 12px; margin-bottom: 10px;
    }
    .dot-origin { color: #E11D48; font-weight: 800; }
    .dot-dest { color: #0F766E; font-weight: 800; }
    .res-card {
        background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 4px solid #166970;
        border-radius: 12px; padding: 11px 15px; margin-bottom: 9px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .res-title { font-weight: 700; font-size: 0.94rem; color: #0F293A; }
    .res-sub { font-size: 0.78rem; color: #64748B; margin-top: 2px; }
    .res-pill {
        background: #E6F7F4; color: #0F6E66; border: 1px solid #B2E5DC;
        font-weight: 700; font-size: 0.8rem; padding: 4px 11px; border-radius: 999px;
    }
    .rank-tag {
        background: #0F293A; color: #5CE1B8; font-weight: 800; font-size: 0.76rem;
        padding: 2px 8px; border-radius: 6px; margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 3. CACHED DATA, GEOCODING & ROAD ROUTING HELPERS
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    location_df = pickle.load(open('datasets/location_distance.pkl', 'rb'))
    cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
    cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
    cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1.0 * cosine_sim3

    # Optional CSV load to map societies to their exact sector if a sector isn't a column in location_df
    sector_to_societies = {}
    for csv_path in [
        'datasets/gurgaon_properties_outlier_treated.csv',
        'datasets/gurgaon_properties_outlier_treated (1).csv',
        'gurgaon_properties_outlier_treated.csv',
        'gurgaon_properties_outlier_treated (1).csv'
    ]:
        if os.path.exists(csv_path):
            df_props = pd.read_csv(csv_path)
            if 'sector' in df_props.columns and 'society' in df_props.columns:
                df_props = df_props[df_props['sector'].isin(ALLOWED_SECTORS)].dropna(subset=['society'])
                idx_lookup = {str(idx).strip().lower(): idx for idx in location_df.index}
                for sec, grp in df_props.groupby('sector'):
                    matched_apts = []
                    for soc in grp['society'].unique():
                        key = str(soc).strip().lower()
                        if key in idx_lookup:
                            matched_apts.append(idx_lookup[key])
                    sector_to_societies[sec] = sorted(set(matched_apts))
            break

    return location_df, cosine_sim_matrix, sector_to_societies


@st.cache_data(show_spinner=False)
def geocode_exact(place_name: str):
    """Fetch (lat, lon) strictly for the exact sector/property name passed—never substitutes another sector."""
    headers = {"User-Agent": "GurgaonEstatesPropTech/1.0"}
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": f"{place_name}, Gurgaon, Haryana, India", "format": "json", "limit": 1},
            headers=headers,
            timeout=4
        )
        data = resp.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
        time.sleep(0.3)
    except Exception:
        pass
    return None


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return round(2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 1)


@st.cache_data(show_spinner=False)
def get_route_and_distance(lat1, lon1, lat2, lon2):
    """Get driving path coordinates [[lon, lat], ...] and distance via OSRM, with straight-line fallback."""
    try:
        url = f"https://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
        resp = requests.get(url, params={"overview": "full", "geometries": "geojson"}, timeout=3)
        data = resp.json()
        if data.get("code") == "Ok" and data.get("routes"):
            route = data["routes"][0]
            coords = route["geometry"]["coordinates"]
            dist_km = round(route["distance"] / 1000.0, 1)
            return coords, dist_km
    except Exception:
        pass

    return [[lon1, lat1], [lon2, lat2]], haversine_km(lat1, lon1, lat2, lon2)


def render_route_map(origin_name, origin_coords, destinations):
    """Render light-themed PyDeck map with origin pin, property pins, road paths, and distance labels."""
    o_lat, o_lon = origin_coords
    points = [{
        "name": origin_name,
        "distance": "Selected Origin",
        "lat": o_lat,
        "lon": o_lon,
        "color": [225, 29, 72, 240],
        "radius": 220
    }]
    paths = []
    labels = []

    for item in destinations:
        d_lat, d_lon = item["coords"]
        route_coords, road_km = get_route_and_distance(o_lat, o_lon, d_lat, d_lon)
        display_km = item["dist_km"] if item["dist_km"] is not None else road_km

        points.append({
            "name": item["name"],
            "distance": f"{display_km} km away",
            "lat": d_lat,
            "lon": d_lon,
            "color": [15, 118, 110, 235],
            "radius": 170
        })

        paths.append({
            "name": f"{origin_name} → {item['name']}",
            "distance": f"{display_km} km",
            "path": route_coords
        })

        mid_pt = route_coords[len(route_coords) // 2]
        labels.append({
            "lon": mid_pt[0],
            "lat": mid_pt[1],
            "text": f"{display_km} km"
        })

    path_layer = pdk.Layer(
        "PathLayer",
        data=paths,
        get_path="path",
        get_color=[22, 105, 112, 200],
        width_scale=12,
        width_min_pixels=3,
        pickable=True
    )

    pin_layer = pdk.Layer(
        "ScatterplotLayer",
        data=points,
        get_position="[lon, lat]",
        get_color="color",
        get_radius="radius",
        radius_min_pixels=7,
        radius_max_pixels=16,
        stroked=True,
        get_line_color=[255, 255, 255, 255],
        line_width_min_pixels=2,
        pickable=True
    )

    text_layer = pdk.Layer(
        "TextLayer",
        data=labels,
        get_position="[lon, lat]",
        get_text="text",
        get_size=13,
        get_color=[15, 41, 58, 255],
        get_background_color=[255, 255, 255, 235],
        background=True,
        background_padding=[4, 2, 4, 2],
        pickable=False
    )

    view_state = pdk.ViewState(latitude=o_lat, longitude=o_lon, zoom=11.5, pitch=0)

    deck = pdk.Deck(
        layers=[path_layer, pin_layer, text_layer],
        initial_view_state=view_state,
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        tooltip={"html": "<b>{name}</b><br/>{distance}", "style": {"backgroundColor": "#0F293A", "color": "white"}}
    )

    st.markdown("""
        <div class="map-legend">
            <span><span class="dot-origin">●</span> Selected Origin</span>
            <span><span class="dot-dest">●</span> Matched Societies</span>
            <span>━ Road Path &amp; Distance (km)</span>
        </div>
    """, unsafe_allow_html=True)
    st.pydeck_chart(deck, use_container_width=True)


# -----------------------------------------------------------------------------
# 4. LOAD DATA & RECOMMENDER FUNCTION
# -----------------------------------------------------------------------------
location_df, cosine_sim_matrix, sector_to_societies = load_data()

# Normalized column lookup for matching your 104 sectors against location_distance.pkl
NORM_COL_MAP = {
    re.sub(r'[\s\-_]+', ' ', str(col)).strip().lower(): col
    for col in location_df.columns
}


def recommend_properties_with_scores(property_name, top_n=5):
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    top_properties = location_df.index[top_indices].tolist()

    return pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })


if "search_active" not in st.session_state:
    st.session_state.search_active = False
if "recommend_active" not in st.session_state:
    st.session_state.recommend_active = False


# -----------------------------------------------------------------------------
# 5. SIDEBAR & HERO BANNER
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"""
        <div class="sb-brand">
            <div class="sb-title">🏡 Gurgaon Estates</div>
            <div class="sb-sub">PROPTECH INTELLIGENCE</div>
        </div>
        <div class="sb-label">MARKET SNAPSHOT</div>
        <div class="sb-stat">
            <div class="sb-stat-val">{len(location_df):,}</div>
            <div class="sb-stat-lbl">Indexed Residential Societies</div>
        </div>
        <div class="sb-stat">
            <div class="sb-stat-val">{len(ALLOWED_SECTORS)}</div>
            <div class="sb-stat-lbl">Gurgaon Sectors Covered</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="hero-box">
    <div class="hero-pill">DISCOVER &bull; INVEST &bull; LIVE</div>
    <div class="hero-h1">Find a Place You'll<br><span>Love to Call Home.</span></div>
    <p class="hero-p">
        Explore Gurgaon real estate across your 104 curated sectors with interactive route mapping,
        radius filtering, and multi-factor ML property recommendations.
    </p>
    <div class="hero-stats">
        <div>
            <div class="hero-st-title">{len(location_df)}+ Properties</div>
            <div class="hero-st-sub">Verified Gurgaon Societies</div>
        </div>
        <div>
            <div class="hero-st-title">{len(ALLOWED_SECTORS)} Sectors</div>
            <div class="hero-st-sub">Curated Dataset Locations</div>
        </div>
        <div>
            <div class="hero-st-title">Live Route Map</div>
            <div class="hero-st-sub">Road Paths &amp; Distance Pins</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.subheader("Explore Gurgaon Real Estate")
st.caption("Select strictly from your 104 dataset sectors or generate AI-curated apartment matches.")

col1, col2 = st.columns(2, gap="large")

# -----------------------------------------------------------------------------
# 6. CARD 1: SECTOR & RADIUS SEARCH + INTERACTIVE PATH MAP
# -----------------------------------------------------------------------------
with col1:
    with st.container(border=True):
        st.markdown("#### 📍 Search by Sector & Radius")
        st.caption("Filter societies by distance from your selected sector and view road paths.")

        selected_sector = st.selectbox(
            "Select Sector",
            ALLOWED_SECTORS,
            key="loc_select"
        )
        radius = st.number_input(
            "Search Radius (in Kms)",
            min_value=0.5,
            max_value=50.0,
            value=5.0,
            step=0.5,
            key="radius_input"
        )

        if st.button("🔍 Search & Map Nearby Apartments", key="btn_search"):
            st.session_state.search_active = True

        if st.session_state.search_active:
            st.markdown("---")
            matched_col = NORM_COL_MAP.get(selected_sector)
            origin_coords = geocode_exact(selected_sector)

            # 1) Use precomputed distances if this sector is a column in location_distance.pkl
            if matched_col is not None:
                result_ser = location_df[location_df[matched_col] < radius * 1000][matched_col].sort_values()
                results_list = [(prop, round(dist_m / 1000, 1)) for prop, dist_m in result_ser.items()]
            else:
                # 2) Fallback: check societies mapped to this exact sector in your CSV
                results_list = []
                candidate_apts = sector_to_societies.get(selected_sector, [])
                if origin_coords and candidate_apts:
                    for prop in candidate_apts:
                        p_coords = geocode_exact(prop)
                        if p_coords:
                            _, d_km = get_route_and_distance(
                                origin_coords[0], origin_coords[1], p_coords[0], p_coords[1]
                            )
                            if d_km <= radius:
                                results_list.append((prop, d_km))
                    results_list.sort(key=lambda x: x[1])

            if not results_list:
                if origin_coords:
                    render_route_map(selected_sector, origin_coords, [])
                st.info(f"No properties found within **{radius} km** of **{selected_sector}**.")
            else:
                st.markdown(f"**{len(results_list)} properties** found within **{radius} km** of **{selected_sector}**:")

                if origin_coords:
                    with st.spinner("Plotting sector & road paths on map..."):
                        mapped_destinations = []
                        for prop_name, dist_km in results_list[:8]:
                            coords = geocode_exact(prop_name)
                            if coords:
                                mapped_destinations.append({
                                    "name": prop_name,
                                    "coords": coords,
                                    "dist_km": dist_km
                                })
                        if mapped_destinations:
                            render_route_map(selected_sector, origin_coords, mapped_destinations)

                for prop_name, dist_km in results_list:
                    st.markdown(f"""
                        <div class="res-card">
                            <div>
                                <div class="res-title">{prop_name}</div>
                                <div class="res-sub">Distance from {selected_sector}</div>
                            </div>
                            <span class="res-pill">{dist_km} kms</span>
                        </div>
                    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. CARD 2: SIMILAR APARTMENT RECOMMENDER + INTERACTIVE PATH MAP
# -----------------------------------------------------------------------------
with col2:
    with st.container(border=True):
        st.markdown("#### ✨ Similar Apartment Recommender")
        st.caption("Compare a reference society against its top ML matches and travel paths.")

        selected_appartment = st.selectbox(
            "Select Reference Apartment",
            sorted(location_df.index.to_list()),
            key="apt_select"
        )
        top_n = st.slider(
            "Number of Recommendations",
            min_value=3,
            max_value=8,
            value=5,
            key="top_n_slider"
        )

        if st.button("✨ Recommend & Map Similar Societies", key="btn_recommend"):
            st.session_state.recommend_active = True

        if st.session_state.recommend_active:
            recommendation_df = recommend_properties_with_scores(selected_appartment, top_n=top_n)
            st.markdown("---")
            st.markdown(f"**Top {top_n} matches** similar to **{selected_appartment}**:")

            road_distances = {}
            with st.spinner("Mapping reference property & recommended paths..."):
                ref_coords = geocode_exact(selected_appartment)
                if ref_coords:
                    rec_destinations = []
                    for _, row in recommendation_df.iterrows():
                        prop_name = row["PropertyName"]
                        coords = geocode_exact(prop_name)
                        if coords:
                            _, road_km = get_route_and_distance(
                                ref_coords[0], ref_coords[1], coords[0], coords[1]
                            )
                            road_distances[prop_name] = road_km
                            rec_destinations.append({
                                "name": prop_name,
                                "coords": coords,
                                "dist_km": road_km
                            })
                    if rec_destinations:
                        render_route_map(selected_appartment, ref_coords, rec_destinations)

            for idx, row in recommendation_df.iterrows():
                prop_name = row['PropertyName']
                match_pct = min(100, round((row['SimilarityScore'] / 2.3) * 100))
                dist_note = f" • {road_distances[prop_name]} km away" if prop_name in road_distances else ""
                st.markdown(f"""
                    <div class="res-card">
                        <div>
                            <div class="res-title">
                                <span class="rank-tag">#{idx + 1}</span>{prop_name}
                            </div>
                            <div class="res-sub">Similarity: {row['SimilarityScore']:.3f}{dist_note}</div>
                        </div>
                        <span class="res-pill">{match_pct}% Match</span>
                    </div>
                """, unsafe_allow_html=True)

            with st.expander("View Raw Similarity Data Table"):
                st.dataframe(
                    recommendation_df.style.format({"SimilarityScore": "{:.4f}"}),
                    use_container_width=True,
                    hide_index=True
                )