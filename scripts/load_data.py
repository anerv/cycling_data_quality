
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

graph_osm = ox.graph_from_polygon(sa_poly.to_crs('EPSG:4326').loc[0, 'geometry'], network_type='bike', simplify=False, retain_all=True, truncate_by_edge=False, clean_periphery=True)

# Project graph to chosen crs
graph_osm = ox.project_graph(graph_osm, to_crs=study_crs)

# Get osm_edges and osm_nodes
osm_nodes, osm_edges = ox.graph_to_gdfs(graph_osm)

# Overview of data from OSM
osm_na_poly = osm_nodes.unary_union.convex_hull # Use convex hull for area computation
osm_poly_gdf = gpd.GeoDataFrame()
osm_poly_gdf.at[0,'geometry'] = osm_na_poly
osm_poly_gdf = osm_poly_gdf.set_crs(study_crs)

graph_area = osm_poly_gdf.clip(sa_poly).area.values[0] # Clip in case convex hull goes beyond study area

print(f'The graph covers an area of {graph_area/ 1000000:.2f} square kilometers')

print(f'The length of the OSM network is {osm_edges.unary_union.length/1000 :.2f} kilometers')


# Plot network
fig, ax = plt.subplots(1, figsize=(15,15))

osm_edges.plot(ax=ax, color='black', linewidth=0.2)
osm_nodes.plot(ax=ax, color='black', markersize=0.2)

sa_poly.plot(ax=ax, edgecolor='red', facecolor='None', linewidth=1)

cx.add_basemap(
    ax=ax, 
    crs=sa_poly.crs, 
    source=cx.providers.CartoDB.Voyager
)
ax.set_axis_off()

# TODO: Method for simplifying graph 
graph_osm_simple = None
#%%
# Save data

ox.save_graphml(graph_osm, f'../data/osm_{study_area}.graphml')

#ox.save_graphml(graph_osm_simple, f'../data/osm_{study_area}_simple.graphml')

print('OSM networks saved!')

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
    if ref_data.crs == None:
        print('Please assign a crs to the study area polygon!')

    if ref_data.crs != study_crs:
        ref_data = ref_data.to_crs(study_crs)

    assert ref_data.crs == study_crs


    # Clip reference data to study area poly

    # Convert to network format
    graph_ref = None


    area = 100000000
    print(f'The reference data covers an {area / 1000000:.2f} square kilometers')

    # Plot network
    fig, ax = plt.subplots(1, figsize=(15,15))

    ref_nodes, ref_edges = None

    ref_edges.plot(ax=ax, color='purple', linewidth=0.2)
    ref_nodes.plot(ax=ax, color='purple', markersize=0.2)

    sa_poly.plot(ax=ax, edgecolor='red', facecolor='None', linewidth=1)

    ax.set_axis_off()

    cx.add_basemap(
        ax, 
        crs=sa_poly.crs, 
        source=cx.providers.CartoDB.Voyager
)
    # Simplify
    # TODO: Function for simplfying data
    graph_ref_simple = None

    # Print some simple statements about how big the dataset is, how much area it covers, how many meters etc.
    
    # Save data

    ox.save_graphml(graph_ref, f'../data/ref_{study_area}.graphml')

    #ox.save_graphml(graph_ref_simple, f'../data/ref_{study_area}_simple.graphml')

    print('Reference networks saved!')
    
else:
    print('The analysis will not make use of a reference data set. Please update config settings if a extrinsic analysis of OSM data quality should be performed.')
#%%

def create_nx_data():

    # Function of converting geopandas dataframe to NX structure - or OSMNX??

    # Convert to network structure

    # Get osm_nodes

    # Create 'fake' osmid for osm_nodes - make sure that they are not identical to any existing IDs! Add a letter to distinguish them?

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