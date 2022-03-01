
#%%
import geopandas as gpd
import osmnx as ox
import yaml
import pickle
import matplotlib.pyplot as plt
#%%
with open(r'../config.yml') as file:

    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    study_area = parsed_yaml_file['study_area']
    reference_format = parsed_yaml_file['reference_format']
    reference_fp = parsed_yaml_file['reference_fp']
    reference_crs = parsed_yaml_file['reference_crs']
    study_crs = parsed_yaml_file['study_crs']
    study_area_poly = parsed_yaml_file['study_area_poly']
    
print('Settings loaded!')
#%%
# Read reference data
ref_data = gpd.read_file(reference_fp)

sa_poly = gpd.read_file(study_area_poly)

# Reproject

# Clip to study area

# Plot

# Print some simple statements about how big the dataset is, how much area it covers, how many meters etc.

# Convert to network format - using ????

#%%

# Read OSM

# Ensure that OSM data cover the exact same area as the reference data
# Compute bounding box from polygon definiong the study area - get data - then clip data to study area

bb = sa_poly.to_crs('EPSG:4326').bounds

north = bb.maxy.loc[0]
south = bb.miny.loc[0]
east = bb.maxx.loc[0]
west = bb.minx.loc[0]

# Using OSMnx - # Maybe use Michael's method wrapped in a function - makes it easy to choose which types to incliude - e.g. simply say bikelanes yes, bikepaths yes, bicycle streets no etc.
G = ox.graph_from_bbox(north, south, east, west, network_type=type, simplify=False, retain_all=True, truncate_by_edge=False, clean_periphery=True, custom_filter=None)

# Reproject

# Plot

# Print some simple statements about how big the dataset is, how much area it covers, how many meters etc.

#%%

# Save data

fig, ax = plt.subplots(1)

sa_poly.envelope.plot(ax=ax)
sa_poly.plot(ax=ax, color='yellow')
# %%
