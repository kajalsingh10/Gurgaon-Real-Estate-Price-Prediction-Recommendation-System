import pandas as pd
import ast

# file_path = "data/gurgaon_properties.csv"

# # Read the original CSV
# df = pd.read_csv(file_path, skiprows=2, on_bad_lines="skip")

# # Clean column names
# df.columns = df.columns.str.strip()
# df = df.rename(columns={
#     df.columns[0]: "property_name"
# })

# # Furnishing features
# features = [
#     "Fridge", "Fan", "TV", "Sofa", "Light", "Microwave",
#     "Water Purifier", "Dining Table", "Modular Kitchen",
#     "Washing Machine", "Wardrobe", "Chimney", "AC",
#     "Curtains", "Geyser", "Bed", "Exhaust Fan", "Stove"
# ]

# # Extract sector
# df["sector"] = df["address"].str.extract(
#     r"(Sector\s+\d+[A-Za-z]?)",
#     flags=2
# )

# # Convert furnishing details to binary
# def extract_features(value):
#     try:
#         items = ast.literal_eval(value) if isinstance(value, str) else []
#     except (ValueError, SyntaxError):
#         items = []

#     items = [str(item).lower() for item in items]

#     result = {}

#     for feature in features:
#         result[feature] = int(
#             any(feature.lower() in item and not item.startswith("no ")
#                 for item in items)
#         )

#     return pd.Series(result)

# furnishing = df["furnishDetails"].apply(extract_features)

# # Combine sector and furnishing data
# result = pd.concat([df["sector"], furnishing], axis=1)
# result = result.dropna(subset=["sector"])

# # One row per sector
# result = result.groupby("sector")[features].max().reset_index()

# # Save output
# result.to_csv("data/sector_furnishing_features.csv", index=False)

# print(result.head())
# print("Final shape:", result.shape)
# print("Saved successfully!")
import pandas as pd
import numpy as np
df =pd.read_csv("data/data_viz1.csv")
def get_nearby_sectors(df, selected_sector, radius_km):

    # Get unique sectors with their coordinates
    sectors = df[['sector', 'latitude', 'longitude']].drop_duplicates(
        subset=['sector']
    ).dropna()

    # Find selected sector
    selected = sectors[
        sectors['sector'].str.lower() == selected_sector.lower()
    ]

    if selected.empty:
        return pd.DataFrame()

    lat1 = np.radians(selected.iloc[0]['latitude'])
    lon1 = np.radians(selected.iloc[0]['longitude'])

    lat2 = np.radians(sectors['latitude'])
    lon2 = np.radians(sectors['longitude'])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2)**2 +
        np.cos(lat1) * np.cos(lat2) *
        np.sin(dlon / 2)**2
    )

    distance = 6371 * 2 * np.arcsin(np.sqrt(a))

    sectors = sectors.copy()
    sectors['distance_km'] = distance

    # Return nearby sectors
    result = sectors[
        sectors['distance_km'] <= radius_km
    ]

    return result.sort_values('distance_km').reset_index(drop=True)

nearby = get_nearby_sectors(
    df,
    selected_sector="sector 36",
    radius_km=5
)

print(nearby)