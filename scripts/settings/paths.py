exec(open("../settings/yaml_variables.py").read())
import pickle

# OSM filepaths
osm_processed_fp = f"../../data/OSM/{study_area}/processed/"

osm_graph_fp = osm_processed_fp + "OSM_graph.graphml"
osm_graph_simplified_fp = osm_processed_fp + "OSM_simplified_graph.graphml"

osm_edges_fp = osm_processed_fp + "OSM_edges.pickle"
osm_nodes_fp = osm_processed_fp + "OSM_nodes.pickle"
osm_edges_simplified_fp = osm_processed_fp + "OSM_edges_simplified.pickle"
osm_nodes_simplified_fp = osm_processed_fp + "OSM_nodes_simplified.pickle"

osm_edges_joined_fp = osm_processed_fp + "OSM_edges_joined.pickle"
osm_nodes_joined_fp = osm_processed_fp + "OSM_nodes_joined.pickle"
osm_edges_simplified_joined_fp = osm_processed_fp + "OSM_edges_simplified_joined.pickle"
osm_nodes_simplified_joined_fp = osm_processed_fp + "OSM_nodes_simplified_joined.pickle"

osm_grid_fp = osm_processed_fp + "grid.gpkg"

osm_meta_fp = osm_processed_fp + "OSM_meta.json"

osm_resplot_fp = f"../../results/OSM/{study_area}/"
osm_res_fp = f"../../results/OSM/{study_area}/"


# Reference filepaths
ref_processed_fp = f"../../data/REFERENCE/{study_area}/processed/"

ref_graph_fp = ref_processed_fp + "REF_graph.graphml"
ref_graph_simplified_fp = ref_processed_fp + "REF_simplified_graph.graphml"

ref_edges_fp = ref_processed_fp + "REF_edges.pickle"
ref_nodes_fp = ref_processed_fp + "REF_nodes.pickle"
ref_edges_simplified_fp = ref_processed_fp + "REF_edges_simplified.pickle"
ref_nodes_simplified_fp = ref_processed_fp + "REF_nodes_simplified.pickle"

ref_edges_joined_fp = ref_processed_fp + "REF_edges_joined.pickle"
ref_nodes_joined_fp = ref_processed_fp + "REF_nodes_joined.pickle"
ref_edges_simplified_joined_fp = ref_processed_fp + "REF_edges_simplified_joined.pickle"
ref_nodes_simplified_joined_fp = ref_processed_fp + "REF_nodes_simplified_joined.pickle"

ref_grid_fp = ref_processed_fp + "grid.gpkg"

ref_resplot_fp = f"../../results/REFERENCE/{study_area}/"
ref_res_fp = f"../../results/REFERENCE/{study_area}/"
