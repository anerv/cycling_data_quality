# Extended README

This file contains more detailed descriptions of the analysis in- and outputs.

## Input and output files

For simplicity, all input data and most settings used in the analysis, are loaded using the python files in the folder /scripts/settings. Below listed the exact input and output files used in each notebook.

### All notebooks

All notebooks make use of the setting specified in *config.yml*, which are loaded using *yaml_variables.py*.
Plotting settings are found in *plotdict.py*; settings for vector tiles used in leaflet plots in *tiledict.py*; styling settings for dataframe styling in *df_styler.py* and filepaths in *paths.py*.

### 01a_load_osm

#### Input files

- `'../data/{study_area}/raw/my_studyarea_polygon'`(see README for instructions)

#### Output files

- `'../data/osm/{study_area}/processed/grid_osm.gpkg'`
- `'../data/osm/{study_area}/processed/osm.graphml'`
- `'../data/osm/{study_area}/processed/osm_simple.graphml'`
- `'../data/osm/{study_area}/osm_meta_{study_area}.json'`
- `'../data/osm/{study_area}/processed/osm_edges.pickle'`
- `'../data/osm/{study_area}/processed/osm_nodes.pickle'`
- `'../data/osm/{study_area}/processed/osm_edges_simplified.pickle'`
- `'../data/osm/{study_area}/processed/osm_nodes_simplified.pickle'`
- `'../data/osm/{study_area}/processed/osm_edges_joined.pickle'`
- `'../data/osm/{study_area}/processed/osm_nodes_joined.pickle'`
- `'../data/osm/{study_area}/processed/osm_edges_simplified_joined.pickle'`
- `'../data/osm/{study_area}/processed/osm_nodes_simplified_joined.pickle'`

### 01b_load_reference

#### Input files

- `'../data/reference/{study_area}/raw/my_studyarea_polygon.gpkg'` (see README for instructions)
- `'../data/reference/{study_area}/raw/reference_data.gpkg'` (see README for instructions)

#### Output files

- `'../data/reference/{study_area}/processed/grid_reference.gpkg'`
- `'../data/reference/{study_area}/processed/reference.graphml'`
- `'../data/reference/{study_area}/processed/reference_simple.graphml'`
- `'../data/reference/{study_area}/processed/ref_edges.pickle'`
- `'../data/reference/{study_area}/processed/ref_nodes.pickle'`
- `'../data/reference/{study_area}/processed/ref_edges_simplified.pickle'`
- `'../data/reference/{study_area}/processed/ref_nodes_simplified.pickle'`
- `'../data/reference/{study_area}/processed/ref_edges_joined.pickle'`
- `'../data/reference/{study_area}/processed/ref_nodes_joined.pickle'`
- `'../data/reference/{study_area}/processed/ref_edges_simplified_joined.pickle'`
- `'../data/reference/{study_area}/processed/ref_nodes_simplified_joined.pickle'`

### 02a_intrinsic_analysis_osm

#### Input files

- `'../data/osm/{study_area}/processed/grid_osm.gpkg'`
- `'../data/osm/{study_area}/processed/osm.graphml'`
- `'../data/osm/{study_area}/processed/osm_simple.graphml'`
- `'../data/osm/{study_area}/processed/osm_edges.pickle'`
- `'../data/osm/{study_area}/processed/osm_nodes.pickle'`
- `'../data/osm/{study_area}/processed/osm_edges_simplified.pickle'`
- `'../data/osm/{study_area}/processed/osm_nodes_simplified.pickle'`
- `'../data/osm/{study_area}/processed/osm_edges_joined.pickle'`
- `'../data/osm/{study_area}/processed/osm_nodes_joined.pickle'`
- `'../data/osm/{study_area}/processed/osm_edges_simplified_joined.pickle'`
- `'../data/osm/{study_area}/processed/osm_nodes_simplified_joined.pickle'`

#### Output files

**Text files**

- `../results/ref_instrinsic_analysis_{study_area}.json`

**Spatial data**

- `../results/osm/{study_area}/grid_results_intrinsic.pickle`

**Plots**

- `../results/plots/folium_multiple_edges_map_ref.html`
- `../results/plots/folium_danglingmap_ref.html`
- `../results/plots/folium_overundershoots_ref.html`
- `../results/plots/folium_component_gaps_ref.html`

### 02b_intrinsic_analysis_ref

#### Input files

- `'../data/reference/{study_area}/processed/grid_reference.gpkg'`
- `'../data/reference/{study_area}/processed/reference.graphml'`
- `'../data/reference/{study_area}/processed/reference_simple.graphml'`
- `'../data/reference/{study_area}/processed/ref_edges.pickle'`
- `'../data/reference/{study_area}/processed/ref_nodes.pickle'`
- `'../data/reference/{study_area}/processed/ref_edges_simplified.pickle'`
- `'../data/reference/{study_area}/processed/ref_nodes_simplified.pickle'`
- `'../data/reference/{study_area}/processed/ref_edges_joined.pickle'`
- `'../data/reference/{study_area}/processed/ref_nodes_joined.pickle'`
- `'../data/reference/{study_area}/processed/ref_edges_simplified_joined.pickle'`
- `'../data/reference/{study_area}/processed/ref_nodes_simplified_joined.pickle'`

#### Output files

**Text files**
...

**Spatial data**

- `../results/ref/{study_area}/grid_results_intrinsic.pickle`

**Plots**

...

### 03a_extrinsic_analysis_metrics

#### Input files

### Output files

**Text files**
...

**Spatial data**

**Plots**

### 03b_extrinsic_analysis_feature_matching

#### Input files

- `'../data/osm/{study_area}/processed/grid_osm.gpkg'`
- `'../data/osm/{study_area}/processed/osm_edges_simplified.pickle'`
- `'../data/osm/{study_area}/processed/osm_nodes_simplified.pickle'`
- `'../data/osm/{study_area}/processed/osm_edges_simplified_joined.pickle'`
- `'../data/osm/{study_area}/processed/osm_nodes_simplified_joined.pickle'`

- `'../data/reference/{study_area}/processed/grid_reference.gpkg'`
- `'../data/reference/{study_area}/processed/ref_edges_simplified.pickle'`
- `'../data/reference/{study_area}/processed/ref_nodes_simplified.pickle'`
- `'../data/reference/{study_area}/processed/ref_edges_simplified_joined.pickle'`
- `'../data/reference/{study_area}/processed/ref_nodes_simplified_joined.pickle'`

#### Output files

**Text files**
...

**Spatial data**

- `'../results/compare/{study_area}/segment_matches_{buffer_dist}_{hausdorff_threshold}_{angular_threshold}.pickle'`

**Plots**

## Plotting

ADD DESCRIOTION OF PLOTTING SETTINGS HERE?

....
