# This data is prepared in the 01a_load_osm notebook

import osmnx as ox
import geopandas as gpd
import pickle

exec(open("../settings/yaml_variables.py").read())
exec(open("../settings/paths.py").read())

# Load simplified and non-simplified graphs
osm_graph = ox.load_graphml(
    osm_graph_fp, edge_dtypes={"cycling_bidirectional": ox.io._convert_bool_string}
)

osm_graph_simplified = ox.load_graphml(
    osm_graph_simplified_fp,
    edge_dtypes={
        "cycling_bidirectional": ox.io._convert_bool_string,
        "infrastructure_length": float,
    },
)

print("OSM graphs loaded successfully!")

# Load grid
osm_grid = gpd.read_file(osm_grid_fp)
grid_ids = osm_grid.grid_id.to_list()

# Load saved edged and nodes
with open(osm_nodes_fp, "rb") as fp:
    osm_nodes = pickle.load(fp)

with open(osm_edges_fp, "rb") as fp:
    osm_edges = pickle.load(fp)

with open(osm_nodes_simplified_fp, "rb") as fp:
    osm_nodes_simplified = pickle.load(fp)

with open(osm_edges_simplified_fp, "rb") as fp:
    osm_edges_simplified = pickle.load(fp)

# Joined data
with open(osm_nodes_joined_fp, "rb") as fp:
    osm_nodes_joined = pickle.load(fp)

with open(osm_edges_joined_fp, "rb") as fp:
    osm_edges_joined = pickle.load(fp)

with open(osm_nodes_simplified_joined_fp, "rb") as fp:
    osm_nodes_simp_joined = pickle.load(fp)

with open(osm_edges_simplified_joined_fp, "rb") as fp:
    osm_edges_simp_joined = pickle.load(fp)

print("OSM data loaded successfully!")
