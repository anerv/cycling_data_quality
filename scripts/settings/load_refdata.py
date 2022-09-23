# This data is prepared in the 01b_load_reference notebook

import osmnx as ox
import geopandas as gpd
import pickle

exec(open('yaml_variables.py').read())

# Load simplified and non-simplified graphs
reference_graph = ox.load_graphml(
    f'../data/reference/{study_area}/processed/reference.graphml', 
    edge_dtypes={'cycling_bidirectional': ox.io._convert_bool_string})

reference_simplified_graph = ox.load_graphml(
    f'../data/reference/{study_area}/processed/reference_simple.graphml', 
    edge_dtypes={'cycling_bidirectional': ox.io._convert_bool_string, 
    'infrastructure_length':float})

print('Graphs loaded!')

# Load grid
grid = gpd.read_file(f'../data/reference/{study_area}/processed/grid.gpkg')
grid_ids = grid.grid_id.to_list()

# Load saved edged and nodes
with open(f'../data/reference/{study_area}/processed/reference_nodes.pickle', 'rb') as fp:
    nodes = pickle.load(fp)

with open(f'../data/reference/{study_area}/processed/reference_edges.pickle', 'rb') as fp:
    edges = pickle.load(fp)

with open(f'../data/reference/{study_area}/processed/reference_nodes_simplified.pickle', 'rb') as fp:
    nodes_simplified = pickle.load(fp)

with open(f'../data/reference/{study_area}/processed/reference_edges_simplified.pickle', 'rb') as fp:
    edges_simplified = pickle.load(fp)

# Joined data
with open(f'../data/reference/{study_area}/processed/reference_nodes_joined.pickle', 'rb') as fp:
    nodes_joined = pickle.load(fp)

with open(f'../data/reference/{study_area}/processed/reference_edges_joined.pickle', 'rb') as fp:
    edges_joined = pickle.load(fp)

with open(f'../data/reference/{study_area}/processed/reference_nodes_simplified_joined.pickle', 'rb') as fp:
    nodes_simp_joined = pickle.load(fp)

with open(f'../data/reference/{study_area}/processed/reference_edges_simplified_joined.pickle', 'rb') as fp:
    edges_simp_joined = pickle.load(fp)

print('reference data loaded!')