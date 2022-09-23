# This data is prepared in the 01b_load_ref notebook

import osmnx as ox
import geopandas as gpd
import pickle

exec(open('../settings/yaml_variables.py').read())
exec(open('../settings/paths.py').read())

# Load simplified and non-simplified graphs
ref_graph = ox.load_graphml(
    ref_graph_fp, 
    edge_dtypes={'cycling_bidirectional': ox.io._convert_bool_string})

ref_graph_simplified = ox.load_graphml(
    ref_graph_simplified_fp, 
    edge_dtypes={'cycling_bidirectional': ox.io._convert_bool_string, 
    'infrastructure_length':float})

print('Reference graphs loaded successfully!')

# Load grid
grid = gpd.read_file(ref_grid_fp)
grid_ids = grid.grid_id.to_list()

# Load saved edged and nodes
with open(ref_nodes_fp, 'rb') as fp:
    ref_nodes = pickle.load(fp)

with open(ref_edges_fp, 'rb') as fp:
    ref_edges = pickle.load(fp)

with open(ref_nodes_simplified_fp, 'rb') as fp:
    ref_nodes_simplified = pickle.load(fp)

with open(ref_edges_simplified_fp, 'rb') as fp:
    ref_edges_simplified = pickle.load(fp)

# Joined data
with open(ref_nodes_joined_fp, 'rb') as fp:
    ref_nodes_joined = pickle.load(fp)

with open(ref_edges_joined_fp, 'rb') as fp:
    ref_edges_joined = pickle.load(fp)

with open(ref_nodes_simplified_joined_fp, 'rb') as fp:
    ref_nodes_simp_joined = pickle.load(fp)

with open(ref_edges_simplified_joined_fp, 'rb') as fp:
    ref_edges_simp_joined = pickle.load(fp)

print('Reference data loaded successfully!')