
#%%
import geopandas as gpd
import osmnx as ox
import yaml
import matplotlib.pyplot as plt
import contextily as cx
from datetime import datetime
#%%
with open(r'../config.yml') as file:

    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    study_area = parsed_yaml_file['study_area']
    study_crs = parsed_yaml_file['study_crs']
    study_area_poly = parsed_yaml_file['study_area_poly']

    reference_comparison = parsed_yaml_file['reference_comparison']
    reference_format = parsed_yaml_file['reference_format']
    reference_fp = parsed_yaml_file['reference_fp']
    
    custom_filter = parsed_yaml_file['custom_filter']

print('Settings loaded!')
#%%
########## Study Area ##########

# Read polygon for study area
sa_poly = gpd.read_file(study_area_poly)

if sa_poly.crs == None:
    print('Please assign a crs to the study area polygon!')

if sa_poly.crs != study_crs:
    sa_poly = sa_poly.to_crs(study_crs)

assert sa_poly.crs == study_crs

area = sa_poly.area.values[0]
print(f'The size of the study area is {area / 1000000:.2f} square kilometers')

fig, ax = plt.subplots(1, figsize=(15,15))

sa_poly.plot(ax=ax, color='green', alpha=0.4)

ax.set_axis_off()

cx.add_basemap(
    ax, 
    crs=sa_poly.crs, 
    source=cx.providers.CartoDB.Voyager
)

#%%
########## PART 1: READ OSM DATA ##########

# TODO: Method for getting graph based on custom filter

graph_osm = ox.graph_from_polygon(sa_poly.to_crs('EPSG:4326').loc[0, 'geometry'], network_type='all', simplify=False, retain_all=True, truncate_by_edge=False, clean_periphery=True, custom_filter=custom_filter)

# Project graph to chosen crs
graph_osm = ox.project_graph(graph_osm, to_crs=study_crs)

# Get edges and nodes
nodes, edges = ox.graph_to_gdfs(graph_osm)

# Overview of data from OSM
osm_na_poly = nodes.unary_union.convex_hull # Use convex hull for area computation
osm_poly_gdf = gpd.GeoDataFrame()
osm_poly_gdf.at[0,'geometry'] = osm_na_poly
osm_poly_gdf = osm_poly_gdf.set_crs(study_crs)

graph_area = osm_poly_gdf.clip(sa_poly).area.values[0] # Clip in case convex hull goes beyond study area

print(f'The graph covers an area of {graph_area/ 1000000:.2f} square kilometers')

print(f'The length of the OSM network is {edges.unary_union.length/1000 :.2f} kilometers')


# Plot network
fig, ax = plt.subplots(1, figsize=(15,15))

edges.plot(ax=ax, color='black', linewidth=0.2)
nodes.plot(ax=ax, color='black', markersize=0.2)

sa_poly.plot(ax=ax, edgecolor='red', facecolor='None', linewidth=1)

cx.add_basemap(
    ax=ax, 
    crs=sa_poly.crs, 
    source=cx.providers.CartoDB.Voyager
)
ax.set_axis_off()
#%%
# TODO: Method for simplifying graph 
graph_osm_simple = None
#%%
# Save data

ox.save_graphml(graph_osm, f'../data/osm_{study_area}.graphml')

#ox.save_graphml(graph_osm_simple, f'../data/osm_{study_area}_simple.graphml')

# Save time for when OSM data was loaded
current_time = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
f = open('../osm_meta.txt', 'a')
f.write(f'OSM data for {study_area} downloaded at: {current_time} \n')
f.close()

#%%
########## PART 2: READ REFERENCE DATA ##########

if reference_comparison:

    # Read reference data
    ref_data = gpd.read_file(reference_fp)


    # Reproject

    # Clip to study area

    # Plot

    # Print some simple statements about how big the dataset is, how much area it covers, how many meters etc.

    # Convert to network format - using networkx/osmnx
    # TODO: Function for converting data to osmnx format

    # Simplify
    # TODO: Function for simplfying data

    # Save data

else:
    print('The analysis will not make use of a reference data set. Please update config settings if a extrinsic analysis of OSM data quality should be performed.')
#%%

def create_nx_data():
    
    # Function of converting geopandas dataframe to NX structure - or OSMNX??

    # Convert to network structure

    # Get nodes

    # Create 'fake' osmid for nodes - make sure that they are not identical to any existing IDs! Add a letter to distinguish them?

    # Create x y coordinate columns

    # Create multiindex in u v key format

    nx_graph = None

    return nx_graph
    ''''
    
     However, you can convert arbitrary node and edge GeoDataFrames as long as 
    1) gdf_nodes is uniquely indexed by osmid, 
    2) gdf_nodes contains x and y coordinate columns representing node geometries, 
    3) gdf_edges is uniquely multi-indexed by u, v, key (following normal MultiDiGraph structure). 
    This allows you to load any node/edge shapefiles or GeoPackage layers as GeoDataFrames then convert them to a MultiDiGraph for graph analysis. 
    Note that any geometry attribute on gdf_nodes is discarded since x and y provide the necessary node geometry information instead.
    
    '''