# Extended README

This file contains more detailed descriptions of the analysis in- and outputs.

## Input and output files

For simplicity, all input data and most settings used in the analysis, are loaded using the python files in the folder /scripts/settings. Below listed the exact input and output files used in each notebook.

### All notebooks

All notebooks make use of the setting specified in *config.yml*, which are loaded using *yaml_variables.py*.
Plotting settings are found in *plotdict.py*; settings for vector tiles used in leaflet plots in *tiledict.py*; styling settings for dataframe styling in *df_styler.py* and filepaths in *paths.py*.

### 01a_load_osm

**Input files:**

- `'../data/{study_area}/raw/mystudyarea_polygon'`

**Output files:**

- `'../data/osm/{study_area}/processed/grid_osm.gpkg'`
- `'../data/osm/{study_area}/processed/osm.graphml'`
- `'../data/osm/{study_area}/processed/osm_simple.graphml'`
- `'../data/osm/{study_area}/osm_meta_{study_area}.json'`

### 01b_load_reference

--Input files of this notebook:--

- `'../config.yml'`
- `'../data/reference/{study_area}/raw/study_area_polygon.gpkg'` (see README for instructions)
- `'../data/reference/{study_area}/raw/reference_data.gpkg'` (see README for instructions)

--Output files of this notebook:--

- `'../data/reference/{study_area}/processed/grid_reference.gpkg'`
- `'../data/reference/{study_area}/processed/reference.graphml'`
- `'../data/reference/{study_area}/processed/reference_simple.graphml'`

### 02a_intrinsic_analysis_osm

**Input files:**

- `../config.yml`
- `../data/ref_{study_area}.graphml`
- `../data/ref_{study_area}_simple.graphml`
- `../data/ref_nodes_{study_area}.pickle`
- `../data/ref_edges_{study_area}.pickle`
- `../data/ref_nodes_simplified_{study_area}.pickle`
- `../data/ref_edges_simplified_{study_area}.pickle`
- `../data/ref_nodes_joined_{study_area}.pickle`
- `../data/ref_edges_joined_{study_area}.pickle`
- `../data/ref_nodes_simplified_joined_{study_area}.pickle`
- `../data/ref_edges_simplified_joined_{study_area}.pickle`
- `../data/grid_{study_area}.gpkg`

**Output files:**

- `../results/ref_instrinsic_analysis_{study_area}.json`
- `../results/grid_results_intrinsic_{study_area}.pickle`
- `../results/plots/folium_multiple_edges_map_ref.html`
- `../results/plots/folium_danglingmap_ref.html`
- `../results/plots/folium_overundershoots_ref.html`
- `../results/plots/folium_component_gaps_ref.html`

### 02b_intrinsic_analysis_ref

**Input files:**

- `../config.yml`
- `../data/ref_{study_area}.graphml`
- `../data/ref_{study_area}_simple.graphml`
- `../data/ref_nodes_{study_area}.pickle`
- `../data/ref_edges_{study_area}.pickle`
- `../data/ref_nodes_simplified_{study_area}.pickle`
- `../data/ref_edges_simplified_{study_area}.pickle`
- `../data/ref_nodes_joined_{study_area}.pickle`
- `../data/ref_edges_joined_{study_area}.pickle`
- `../data/ref_nodes_simplified_joined_{study_area}.pickle`
- `../data/ref_edges_simplified_joined_{study_area}.pickle`
- `../data/grid_{study_area}.gpkg`

**Output files:**

- `../results/ref_instrinsic_analysis_{study_area}.json`
- `../results/grid_results_intrinsic_{study_area}.pickle`
- `../results/plots/folium_multiple_edges_map_ref.html`
- `../results/plots/folium_danglingmap_ref.html`
- `../results/plots/folium_overundershoots_ref.html`
- `../results/plots/folium_component_gaps_ref.html`

### 03b_extrinsic_analysis_feature_matching

**Input files_**

- `../config.yml`
- `../data/osm_{study_area}_simple.graphml`
- `../data/ref_{study_area}_simple.graphml`
- `../data/grid_{study_area}.gpkg`
- `../data/osm_nodes_simplified_{study_area}.pickle`
- `../data/osm_edges_simplified_{study_area}.pickle`
- `../data/osm_edges_joined_{study_area}.pickle`
- `../data/osm_edges_simplified_joined_{study_area}.pickle`
- `../data/ref_edges_simplified_{study_area}.pickle`
- `../data/ref_edges_simplified_joined_{study_area}.pickle`

**Output files:**

- `../results/segment_matches_{study_area}.pickle`
- `../results/feature_matches_{study_area}.json`
- `../results/grid_results_feature_matching_{study_area}.pickle`
- `../results/plots/folium_segment_matches.html`

## Plotting

....

##
