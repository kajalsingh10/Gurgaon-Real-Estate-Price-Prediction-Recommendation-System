import os
import re
import math
import html
import time
import hashlib
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
    initial_sidebar_state="expanded",
)

# Rough bounding box for Gurgaon / Manesar, used to reject wrong geocoding hits.
GURGAON_BOUNDS = {"lat": (28.20, 28.60), "lon": (76.75, 77.30)}


def html_block(markup: str) -> str:
    """Strip indentation and blank lines so Streamlit's Markdown parser never
    mistakes indented HTML for a code block."""
    return "".join(line.strip() for line in markup.strip().splitlines() if line.strip())


def natural_key(text: str):
    """Sort 'sector 2' before 'sector 10'."""
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", str(text))]


def show_df(df, **kwargs):
    """st.dataframe wrapper compatible with old and new Streamlit versions."""
    try:
        st.dataframe(df, width="stretch", hide_index=True, **kwargs)
    except TypeError:
        st.dataframe(df, use_container_width=True, hide_index=True, **kwargs)


# -----------------------------------------------------------------------------
# 1. CSS
# -----------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background-color: #F4F7F9 !important; color: #0F293A !important; }
header[data-testid="stHeader"] { background-color: transparent !important; }
section[data-testid="stSidebar"] { background-color: #0F293A !important; border-right: 1px solid #1B3B50; }
section[data-testid="stSidebar"] * { color: #F8FAFC !important; }
[data-testid="stSidebarCollapseButton"] button,
section[data-testid="stSidebar"] button[kind="header"],
section[data-testid="stSidebar"] button[kind="headerNoPadding"],
section[data-testid="stSidebar"] [data-testid="stBaseButton-headerNoPadding"],
section[data-testid="stSidebar"] [data-testid="baseButton-headerNoPadding"] {
    background-color: #FFFFFF !important; color: #000000 !important;
    border-radius: 8px !important; opacity: 1 !important;
}
[data-testid="stSidebarCollapseButton"] button *,
section[data-testid="stSidebar"] button[kind="header"] *,
section[data-testid="stSidebar"] button[kind="headerNoPadding"] *,
section[data-testid="stSidebar"] [data-testid="stBaseButton-headerNoPadding"] *,
section[data-testid="stSidebar"] [data-testid="baseButton-headerNoPadding"] * {
    color: #000000 !important; fill: #000000 !important;
}
[data-testid="stExpandSidebarButton"] button,
[data-testid="collapsedControl"] button,
header[data-testid="stHeader"] button[kind="headerNoPadding"],
header[data-testid="stHeader"] [data-testid="stBaseButton-headerNoPadding"] {
    background-color: #FFFFFF !important; color: #000000 !important;
    border: 1px solid #CBD5E1 !important; border-radius: 8px !important; opacity: 1 !important;
}
[data-testid="stExpandSidebarButton"] button *,
[data-testid="collapsedControl"] button *,
header[data-testid="stHeader"] button[kind="headerNoPadding"] *,
header[data-testid="stHeader"] [data-testid="stBaseButton-headerNoPadding"] * {
    color: #000000 !important; fill: #000000 !important;
}
.sb-brand { padding: 0.4rem 0 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.12); margin-bottom: 1rem; }
.sb-title { font-size: 1.2rem; font-weight: 800; color: #FFFFFF !important; }
.sb-sub { font-size: 0.68rem; letter-spacing: 0.14em; color: #7FA1B5 !important; font-weight: 700; margin-top: 3px; }
.sb-label { font-size: 0.68rem; letter-spacing: 0.12em; color: #7FA1B5 !important; font-weight: 700; margin: 1rem 0 0.5rem 0; }
.sb-stat { background: #143246; border: 1px solid #20465E; border-radius: 10px; padding: 10px 14px; margin-bottom: 8px; }
.sb-stat-val { font-size: 1.1rem; font-weight: 800; color: #5CE1B8 !important; }
.sb-stat-lbl { font-size: 0.75rem; color: #9FB8C7 !important; }
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
"""
st.markdown(html_block(CSS), unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. DATA LOADING
# -----------------------------------------------------------------------------
def normalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    frame.columns = (
        frame.columns.astype(str).str.strip().str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True).str.strip("_")
    )
    aliases = {
        "sector_name": "sector", "society_name": "society",
        "lat": "latitude", "latitute": "latitude",
        "lon": "longitude", "lng": "longitude", "long": "longitude",
        "bedroom": "bedroom", "bed_room": "bedroom",
    }
    return frame.rename(columns={c: aliases[c] for c in frame.columns if c in aliases})


# Approximate centres for named areas that are not numbered sectors.
FALLBACK_AREA_COORDS = {
    "sohna road": (28.4050, 77.0400),
    "sohna road road": (28.4050, 77.0400),
    "dwarka expressway": (28.4300, 76.9900),
    "manesar": (28.3500, 76.9370),
    "gwal pahari": (28.4400, 77.1400),
}


def fill_missing_coordinates(coord_df, sectors):
    """Approximate coordinates for sectors missing from the coordinate file:
    - named areas -> hard-coded centre
    - 'sector 10a', 'sector 3 phase 2', ... -> parent 'sector N' coordinates
    - 'new', 'new sector 2' -> centre of sectors 82-95 (New Gurgaon)
    Returns (rows_to_add, still_missing)."""
    known = {r.sector: (r.latitude, r.longitude) for r in coord_df.itertuples()}
    rows, still_missing = [], []
    for sec in sectors:
        if sec in known:
            continue
        pos = FALLBACK_AREA_COORDS.get(sec)
        if pos is None:
            m = re.match(r"^sector (\d+)", sec)
            if m and f"sector {m.group(1)}" in known:
                pos = known[f"sector {m.group(1)}"]
            elif sec.startswith("new"):
                pts = [known[f"sector {n}"] for n in range(82, 96) if f"sector {n}" in known]
                if pts:
                    pos = (float(np.mean([p[0] for p in pts])), float(np.mean([p[1] for p in pts])))
        if pos is None:
            still_missing.append(sec)
        else:
            rows.append({"sector": sec, "latitude": pos[0], "longitude": pos[1]})
    return rows, still_missing


@st.cache_data(show_spinner="Loading data...")
def load_data():
    """Returns (location_df, cosine_sim_matrix, property_df, messages).
    No st.* UI calls here (they misbehave inside cached functions)."""
    messages = []  # list of (level, text)

    with open("datasets/location_distance.pkl", "rb") as f:
        location_df = pickle.load(f)
    with open("datasets/cosine_sim1.pkl", "rb") as f:
        cosine_sim1 = pickle.load(f)
    with open("datasets/cosine_sim2.pkl", "rb") as f:
        cosine_sim2 = pickle.load(f)
    with open("datasets/cosine_sim3.pkl", "rb") as f:
        cosine_sim3 = pickle.load(f)

    cosine_sim_matrix = 0.5 * np.asarray(cosine_sim1) + 0.8 * np.asarray(cosine_sim2) + 1.0 * np.asarray(cosine_sim3)

    # ---- property CSV ----
    property_candidates = [
        "datasets/gurgaon_properties_outlier_treated.csv",
        "datasets/gurgaon_properties_outlier_treated (1).csv",
        "gurgaon_properties_outlier_treated.csv",
        "gurgaon_properties_outlier_treated (1).csv",
    ]
    for folder in ("datasets", "data", "."):
        if os.path.isdir(folder):
            for filename in sorted(os.listdir(folder)):
                if filename.lower().endswith(".csv") and filename.lower() != "data_viz1.csv":
                    candidate = os.path.join(folder, filename)
                    if candidate not in property_candidates:
                        property_candidates.append(candidate)

    property_df = None
    checked = []
    for csv_path in property_candidates:
        if not os.path.isfile(csv_path):
            continue
        checked.append(csv_path)
        try:
            cand = normalize_columns(pd.read_csv(csv_path))
        except Exception:
            continue
        if "sector" not in cand.columns:
            continue
        if "society" not in cand.columns:
            name_col = next((c for c in ["property_name", "propertyname", "name"] if c in cand.columns), None)
            cand["society"] = cand[name_col] if name_col else ""
        cand["sector"] = cand["sector"].astype(str).str.strip().str.lower()
        cand["society"] = cand["society"].fillna("").astype(str).str.strip()
        cand = cand[cand["sector"].ne("") & cand["sector"].ne("nan")].copy()
        if not cand.empty:
            property_df = cand
            break

    if property_df is None:
        messages.append((
            "error",
            "Could not load the property CSV. Put it in the `datasets` folder and make sure it has a "
            f"`sector` column. Files checked: {', '.join(checked) if checked else 'none found'}."
        ))
        return location_df, cosine_sim_matrix, None, messages

    # ---- coordinates ----
    coordinate_df = None
    for coord_path in ("data/data_viz1.csv", "datasets/data_viz1.csv", "data_viz1.csv"):
        if not os.path.isfile(coord_path):
            continue
        try:
            coords = normalize_columns(pd.read_csv(coord_path))
            if not {"sector", "latitude", "longitude"}.issubset(coords.columns):
                continue
            coords["sector"] = coords["sector"].astype(str).str.strip().str.lower()
            coords["latitude"] = pd.to_numeric(coords["latitude"], errors="coerce")
            coords["longitude"] = pd.to_numeric(coords["longitude"], errors="coerce")
            coords = coords.dropna(subset=["latitude", "longitude"])
            coords = coords[
                coords["latitude"].between(-90, 90)
                & coords["longitude"].between(-180, 180)
                & coords["sector"].ne("") & coords["sector"].ne("nan")
            ]
            if not coords.empty:
                coordinate_df = (
                    coords.groupby("sector", as_index=False)
                    .agg(latitude=("latitude", "median"), longitude=("longitude", "median"))
                )
                break
        except Exception as exc:
            messages.append(("warning", f"Could not read {coord_path}: {exc}"))

    if coordinate_df is not None:
        extra_rows, still_missing = fill_missing_coordinates(coordinate_df, property_df["sector"].unique())
        if extra_rows:
            coordinate_df = pd.concat([coordinate_df, pd.DataFrame(extra_rows)], ignore_index=True)
        property_df = property_df.drop(columns=["latitude", "longitude"], errors="ignore")
        property_df = property_df.merge(coordinate_df, on="sector", how="left")
        if still_missing:
            messages.append((
                "warning",
                f"No coordinates could be found for: {', '.join(sorted(still_missing, key=natural_key))}. "
                "They are excluded from radius search."
            ))
    else:
        if not {"latitude", "longitude"}.issubset(property_df.columns):
            property_df["latitude"] = np.nan
            property_df["longitude"] = np.nan
        messages.append((
            "warning",
            "data/data_viz1.csv was not found (or lacks sector, latitude, longitude). "
            "The sector dropdown works, but radius search needs coordinates."
        ))

    return location_df, cosine_sim_matrix, property_df, messages


# -----------------------------------------------------------------------------
# 3. GEO HELPERS
# -----------------------------------------------------------------------------
def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    a = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    a = min(1.0, max(0.0, a))
    return round(6371.0 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 1)


@st.cache_data(show_spinner=False, ttl=60 * 60 * 24)
def geocode_exact(place_name: str, sector_hint: str = ""):
    """Geocode a society name via Nominatim. Returns (lat, lon) inside Gurgaon bounds, else None."""
    headers = {"User-Agent": "GurgaonEstatesPropTech/1.0 (streamlit app)"}
    queries = []
    if sector_hint:
        queries.append(f"{place_name}, {sector_hint.title()}, Gurgaon, Haryana, India")
    queries.append(f"{place_name}, Gurgaon, Haryana, India")
    queries.append(f"{place_name}, Gurugram, Haryana, India")
    for q in queries:
        try:
            resp = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": q, "format": "json", "limit": 1},
                headers=headers, timeout=5,
            )
            if resp.status_code == 200:
                data = resp.json()
                if data:
                    lat, lon = float(data[0]["lat"]), float(data[0]["lon"])
                    if (GURGAON_BOUNDS["lat"][0] <= lat <= GURGAON_BOUNDS["lat"][1]
                            and GURGAON_BOUNDS["lon"][0] <= lon <= GURGAON_BOUNDS["lon"][1]):
                        return lat, lon
        except Exception:
            pass
        time.sleep(1.0)  # respect Nominatim's 1 request/second policy
    return None


def build_society_index(df):
    """society (lowercase) -> (sector, lat, lon) using the sector's coordinates."""
    index = {}
    if df is None or not {"society", "sector", "latitude", "longitude"}.issubset(df.columns):
        return index
    valid = df.dropna(subset=["latitude", "longitude"])
    for r in valid[["society", "sector", "latitude", "longitude"]].itertuples(index=False):
        key = str(r.society).strip().lower()
        if key and key not in index:
            index[key] = (r.sector, float(r.latitude), float(r.longitude))
    return index


def locate_society(name, society_index):
    """Returns (coords, is_approx, sector). Tries exact geocoding, then falls back to the
    society's sector centre (with a small stable offset so pins don't overlap)."""
    info = society_index.get(str(name).strip().lower())
    sector = info[0] if info else ""
    exact = geocode_exact(str(name), sector)
    if exact:
        return exact, False, sector
    if info:
        h = hashlib.md5(str(name).encode("utf-8")).digest()
        d_lat = (h[0] / 255 - 0.5) * 0.008   # about +/- 450 m
        d_lon = (h[1] / 255 - 0.5) * 0.008
        return (info[1] + d_lat, info[2] + d_lon), True, sector
    return None, False, sector


def get_nearby_sectors(df, selected_sector, radius_km):
    empty = pd.DataFrame(columns=["sector", "latitude", "longitude", "distance_km"])
    required = {"sector", "latitude", "longitude"}
    if df is None or not required.issubset(df.columns):
        return empty

    valid = df[["sector", "latitude", "longitude"]].copy()
    valid["latitude"] = pd.to_numeric(valid["latitude"], errors="coerce")
    valid["longitude"] = pd.to_numeric(valid["longitude"], errors="coerce")
    valid = valid.dropna(subset=["latitude", "longitude"])
    if valid.empty:
        return empty

    sectors = (
        valid.groupby("sector", as_index=False)
        .agg(latitude=("latitude", "median"), longitude=("longitude", "median"))
    )
    origin = sectors[sectors["sector"] == str(selected_sector).strip().lower()]
    if origin.empty:
        return empty

    lat1 = np.radians(float(origin.iloc[0]["latitude"]))
    lon1 = np.radians(float(origin.iloc[0]["longitude"]))
    lat2 = np.radians(sectors["latitude"].to_numpy(dtype=float))
    lon2 = np.radians(sectors["longitude"].to_numpy(dtype=float))
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    sectors["distance_km"] = (2 * 6371.0 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))).round(2)

    return (
        sectors[sectors["distance_km"] <= float(radius_km)]
        .sort_values("distance_km").reset_index(drop=True)
    )


@st.cache_data(show_spinner=False, ttl=60 * 60 * 6)
def get_route_and_distance(lat1, lon1, lat2, lon2):
    """Driving path [[lon, lat], ...] and km via OSRM; straight-line fallback."""
    try:
        url = f"https://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
        resp = requests.get(url, params={"overview": "full", "geometries": "geojson"}, timeout=4)
        data = resp.json()
        if data.get("code") == "Ok" and data.get("routes"):
            route = data["routes"][0]
            return route["geometry"]["coordinates"], round(route["distance"] / 1000.0, 1)
    except Exception:
        pass
    return [[lon1, lat1], [lon2, lat2]], haversine_km(lat1, lon1, lat2, lon2)


def render_route_map(origin_name, origin_coords, destinations):
    o_lat, o_lon = origin_coords
    points = [{
        "name": origin_name, "distance": "Selected Origin",
        "lat": o_lat, "lon": o_lon, "color": [225, 29, 72, 240], "radius": 220,
    }]
    paths, labels = [], []

    for item in destinations:
        d_lat, d_lon = item["coords"]
        route_coords, road_km = get_route_and_distance(o_lat, o_lon, d_lat, d_lon)
        display_km = item["dist_km"] if item.get("dist_km") is not None else road_km
        points.append({
            "name": item["name"], "distance": f"{display_km} km away",
            "lat": d_lat, "lon": d_lon, "color": [15, 118, 110, 235], "radius": 170,
        })
        paths.append({
            "name": f"{origin_name} → {item['name']}",
            "distance": f"{display_km} km", "path": route_coords,
        })
        if route_coords:
            mid = route_coords[len(route_coords) // 2]
            labels.append({"lon": mid[0], "lat": mid[1], "text": f"{display_km} km"})

    path_layer = pdk.Layer(
        "PathLayer", data=paths, get_path="path", get_color=[22, 105, 112, 200],
        width_scale=12, width_min_pixels=3, pickable=True,
    )
    pin_layer = pdk.Layer(
        "ScatterplotLayer", data=points, get_position="[lon, lat]", get_color="color",
        get_radius="radius", radius_min_pixels=7, radius_max_pixels=16, stroked=True,
        get_line_color=[255, 255, 255, 255], line_width_min_pixels=2, pickable=True,
    )
    text_layer = pdk.Layer(
        "TextLayer", data=labels, get_position="[lon, lat]", get_text="text", get_size=13,
        get_color=[15, 41, 58, 255], get_background_color=[255, 255, 255, 235],
        background=True, background_padding=[4, 2, 4, 2], pickable=False,
    )
    deck = pdk.Deck(
        layers=[path_layer, pin_layer, text_layer],
        initial_view_state=pdk.ViewState(latitude=o_lat, longitude=o_lon, zoom=11.5, pitch=0),
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        tooltip={"html": "<b>{name}</b><br/>{distance}",
                 "style": {"backgroundColor": "#0F293A", "color": "white"}},
    )

    st.markdown(html_block("""
        <div class="map-legend">
            <span><span class="dot-origin">●</span> Selected Origin</span>
            <span><span class="dot-dest">●</span> Nearby Locations</span>
            <span>━ Road Path &amp; Distance (km)</span>
        </div>
    """), unsafe_allow_html=True)
    try:
        st.pydeck_chart(deck, width="stretch")
    except TypeError:
        st.pydeck_chart(deck, use_container_width=True)


# -----------------------------------------------------------------------------
# 4. LOAD + RECOMMENDER
# -----------------------------------------------------------------------------
try:
    location_df, cosine_sim_matrix, property_df, load_messages = load_data()
except FileNotFoundError as exc:
    st.error(f"Required file missing: {exc}. Check the `datasets/` folder (location_distance.pkl, cosine_sim1/2/3.pkl).")
    st.stop()
except Exception as exc:
    st.error(f"Failed to load data: {exc}")
    st.stop()

for level, text in load_messages:
    getattr(st, level)(text)

if property_df is not None and "sector" in property_df.columns:
    ALLOWED_SECTORS = sorted(property_df["sector"].dropna().astype(str).str.strip().unique().tolist(), key=natural_key)
else:
    ALLOWED_SECTORS = []

N_SOCIETIES = len(location_df)


def recommend_properties_with_scores(property_name, top_n=5):
    try:
        pos = location_df.index.get_loc(property_name)
    except KeyError:
        return pd.DataFrame(columns=["PropertyName", "SimilarityScore"])
    if isinstance(pos, slice):          # duplicate index labels
        pos = pos.start
    elif not isinstance(pos, (int, np.integer)):
        pos = int(np.argmax(pos))

    scores = np.asarray(cosine_sim_matrix[pos], dtype=float)
    order = [i for i in np.argsort(-scores) if i != pos]
    names, out = set(), []
    for i in order:
        name = location_df.index[i]
        if name == property_name or name in names:
            continue
        names.add(name)
        out.append((name, float(scores[i])))
        if len(out) == top_n:
            break
    return pd.DataFrame(out, columns=["PropertyName", "SimilarityScore"])


for key in ("search_active", "recommend_active"):
    if key not in st.session_state:
        st.session_state[key] = False


# -----------------------------------------------------------------------------
# 5. SIDEBAR & HERO
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(html_block(f"""
        <div class="sb-brand">
            <div class="sb-title">🏡 Gurgaon Estates</div>
            <div class="sb-sub">PROPTECH INTELLIGENCE</div>
        </div>
        <div class="sb-label">MARKET SNAPSHOT</div>
        <div class="sb-stat">
            <div class="sb-stat-val">{N_SOCIETIES:,}</div>
            <div class="sb-stat-lbl">Indexed Residential Societies</div>
        </div>
        <div class="sb-stat">
            <div class="sb-stat-val">{len(ALLOWED_SECTORS)}</div>
            <div class="sb-stat-lbl">Gurgaon Sectors Covered</div>
        </div>
    """), unsafe_allow_html=True)

st.markdown(html_block(f"""
    <div class="hero-box">
        <div class="hero-pill">DISCOVER &bull; INVEST &bull; LIVE</div>
        <div class="hero-h1">Find a Place You'll<br><span>Love to Call Home.</span></div>
        <p class="hero-p">
            Explore Gurgaon real estate across your dataset sectors with interactive route mapping,
            radius filtering, and multi-factor ML property recommendations.
        </p>
        <div class="hero-stats">
            <div>
                <div class="hero-st-title">{N_SOCIETIES}+ Properties</div>
                <div class="hero-st-sub">Verified Gurgaon Societies</div>
            </div>
            <div>
                <div class="hero-st-title">{len(ALLOWED_SECTORS)} Sectors</div>
                <div class="hero-st-sub">Dataset Locations</div>
            </div>
            <div>
                <div class="hero-st-title">Live Route Map</div>
                <div class="hero-st-sub">Road Paths &amp; Distance Pins</div>
            </div>
        </div>
    </div>
"""), unsafe_allow_html=True)

st.subheader("Explore Gurgaon Real Estate")
st.caption("Select a sector from your property dataset or generate AI-curated apartment matches.")

col1, col2 = st.columns(2, gap="large")

# -----------------------------------------------------------------------------
# 6. CARD 1: SECTOR & RADIUS SEARCH
# -----------------------------------------------------------------------------
with col1:
    with st.container(border=True):
        st.markdown("#### 📍 Search by Sector & Radius")
        st.caption("Filter societies by distance from your selected sector and view road paths.")

        if not ALLOWED_SECTORS:
            st.error("No sectors available. Check your property CSV and its `sector` column.")
        else:
            selected_sector = st.selectbox(
                "Select Sector", ALLOWED_SECTORS, key="loc_select",
                format_func=lambda s: s.title(),
            )
            radius = st.number_input(
                "Search Radius (in Kms)", min_value=0.5, max_value=50.0,
                value=5.0, step=0.5, key="radius_input",
            )

            if st.button("🔍 Search & Map Nearby Apartments", key="btn_search"):
                st.session_state.search_active = True

            if st.session_state.search_active:
                st.markdown("---")
                nearby_sectors = get_nearby_sectors(property_df, selected_sector, radius)

                if nearby_sectors.empty:
                    has_coords = (
                        {"latitude", "longitude"}.issubset(property_df.columns)
                        and property_df[["latitude", "longitude"]].notna().all(axis=1).any()
                    )
                    if not has_coords:
                        st.error("Latitude/longitude are missing, so distances can't be calculated. "
                                 "Add data/data_viz1.csv with sector, latitude, longitude.")
                    else:
                        st.warning(f"No valid coordinates found for {selected_sector.title()}. "
                                   "Check this sector's latitude/longitude.")
                else:
                    sel_key = selected_sector.strip().lower()
                    nearby_names = nearby_sectors["sector"].tolist()
                    nearby_properties = property_df[property_df["sector"].isin(nearby_names)].copy()
                    lookup = dict(zip(nearby_sectors["sector"], nearby_sectors["distance_km"]))
                    nearby_properties["distance_km"] = nearby_properties["sector"].map(lookup)
                    nearby_properties = nearby_properties.sort_values(["distance_km", "sector"])

                    st.success(
                        f"Found {len(nearby_sectors)} sector(s) and {len(nearby_properties)} "
                        f"propert{'y' if len(nearby_properties) == 1 else 'ies'} within "
                        f"{radius:.1f} km of {selected_sector.title()}."
                    )

                    origin_row = nearby_sectors[nearby_sectors["sector"] == sel_key].iloc[0]
                    origin_coords = (float(origin_row["latitude"]), float(origin_row["longitude"]))

                    destinations = [
                        {"name": r["sector"].title(),
                         "coords": (float(r["latitude"]), float(r["longitude"])),
                         "dist_km": None}
                        for _, r in nearby_sectors.iterrows() if r["sector"] != sel_key
                    ]

                    if destinations:
                        if len(destinations) > 8:
                            st.caption("Map shows the 8 closest sectors; the table lists all of them.")
                        with st.spinner("Plotting nearby sectors on the map..."):
                            render_route_map(selected_sector.title(), origin_coords, destinations[:8])
                    else:
                        st.info("Only the selected sector is within this radius. Increase the radius to see more.")

                    st.markdown("### Nearby Sectors")
                    st.caption("distance_km is straight-line distance; map labels show road distance.")
                    show_df(nearby_sectors[["sector", "latitude", "longitude", "distance_km"]])

                    st.markdown("### Properties in Nearby Sectors")
                    preferred = ["sector", "society", "price", "bedroom", "bathroom", "built_up_area", "distance_km"]
                    display_cols = [c for c in preferred if c in nearby_properties.columns]
                    show_df(nearby_properties[display_cols])


# -----------------------------------------------------------------------------
# 7. CARD 2: SIMILAR APARTMENT RECOMMENDER
# -----------------------------------------------------------------------------
with col2:
    with st.container(border=True):
        st.markdown("#### ✨ Similar Apartment Recommender")
        st.caption("Compare a reference society against its top ML matches and travel paths.")

        selected_apartment = st.selectbox(
            "Select Reference Apartment", sorted(location_df.index.to_list()), key="apt_select",
        )
        top_n = st.slider("Number of Recommendations", min_value=3, max_value=8, value=5, key="top_n_slider")

        if st.button("✨ Recommend & Map Similar Societies", key="btn_recommend"):
            st.session_state.recommend_active = True

        if st.session_state.recommend_active:
            recommendation_df = recommend_properties_with_scores(selected_apartment, top_n=top_n)
            st.markdown("---")

            if recommendation_df.empty:
                st.warning("No recommendations found for this apartment.")
            else:
                st.markdown(f"**Top {len(recommendation_df)} matches** similar to **{selected_apartment}**:")

                road_distances = {}
                approx_names = set()
                society_index = build_society_index(property_df)
                with st.spinner("Mapping reference property & recommended paths..."):
                    ref_coords, ref_approx, _ = locate_society(selected_apartment, society_index)
                    if ref_coords:
                        rec_destinations = []
                        for _, row in recommendation_df.iterrows():
                            name = row["PropertyName"]
                            coords, approx, _ = locate_society(name, society_index)
                            if coords:
                                _, road_km = get_route_and_distance(ref_coords[0], ref_coords[1], coords[0], coords[1])
                                road_distances[name] = road_km
                                if approx:
                                    approx_names.add(name)
                                rec_destinations.append({"name": name, "coords": coords, "dist_km": road_km})
                        if rec_destinations:
                            render_route_map(selected_apartment, ref_coords, rec_destinations)
                            if ref_approx or approx_names:
                                st.caption("Some pins are placed at their sector's centre because the exact "
                                           "society location couldn't be found, so those distances are approximate (~).")
                        else:
                            st.info("Couldn't locate the recommended societies on the map.")
                    else:
                        st.info("Couldn't locate the reference society on the map; showing results without it.")

                for rank, (_, row) in enumerate(recommendation_df.iterrows(), start=1):
                    name = row["PropertyName"]
                    score = float(row["SimilarityScore"])
                    match_pct = max(0, min(100, round((score / 2.3) * 100)))
                    dist_note = (f" • {'~' if (name in approx_names or ref_approx) else ''}{road_distances[name]} km away"
                                 if name in road_distances else "")
                    st.markdown(html_block(f"""
                        <div class="res-card">
                            <div>
                                <div class="res-title"><span class="rank-tag">#{rank}</span>{html.escape(str(name))}</div>
                                <div class="res-sub">Similarity: {score:.3f}{dist_note}</div>
                            </div>
                            <span class="res-pill">{match_pct}% Match</span>
                        </div>
                    """), unsafe_allow_html=True)

                with st.expander("View Raw Similarity Data Table"):
                    show_df(recommendation_df.style.format({"SimilarityScore": "{:.4f}"}))