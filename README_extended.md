# Extended README

## Load OSM data

**Input files of this notebook:**

- `'../config.yml'`
- `'../data/{study_area}/raw/mystudyarea_polygon'` (see README for instructions)

**Output files of this notebook:**

- `'../data/osm/{study_area}/processed/grid_osm.gpkg'`
- `'../data/osm/{study_area}/processed/osm.graphml'`
- `'../data/osm/{study_area}/processed/osm_simple.graphml'`
- `'../data/osm/{study_area}/osm_meta_{study_area}.json'`

## Load reference data

**Input files of this notebook:**

- `'../config.yml'`
- `'../data/reference/{study_area}/raw/study_area_polygon.gpkg'` (see README for instructions)
- `'../data/reference/{study_area}/raw/reference_data.gpkg'` (see README for instructions)

**Output files of this notebook:**

- `'../data/reference/{study_area}/processed/grid_reference.gpkg'`
- `'../data/reference/{study_area}/processed/reference.graphml'`
- `'../data/reference/{study_area}/processed/reference_simple.graphml'`


## OSM intrinsic analysis - needs to be updated!

**Input files of this notebook:**
* `../config.yml`
* `../data/ref_{study_area}.graphml`
* `../data/ref_{study_area}_simple.graphml`
* `../data/ref_nodes_{study_area}.pickle`
* `../data/ref_edges_{study_area}.pickle`
* `../data/ref_nodes_simplified_{study_area}.pickle`
* `../data/ref_edges_simplified_{study_area}.pickle`
* `../data/ref_nodes_joined_{study_area}.pickle`
* `../data/ref_edges_joined_{study_area}.pickle`
* `../data/ref_nodes_simplified_joined_{study_area}.pickle`
* `../data/ref_edges_simplified_joined_{study_area}.pickle`
* `../data/grid_{study_area}.gpkg`

**Output files of this notebook:**
* `../results/ref_instrinsic_analysis_{study_area}.json`
* `../results/grid_results_intrinsic_{study_area}.pickle`
* `../results/plots/folium_multiple_edges_map_ref.html`
* `../results/plots/folium_danglingmap_ref.html`
* `../results/plots/folium_overundershoots_ref.html`
* `../results/plots/folium_component_gaps_ref.html`


## Reference intrinsic analysis - needs to be updated!

**Input files of this notebook:**
* `../config.yml`
* `../data/ref_{study_area}.graphml`
* `../data/ref_{study_area}_simple.graphml`
* `../data/ref_nodes_{study_area}.pickle`
* `../data/ref_edges_{study_area}.pickle`
* `../data/ref_nodes_simplified_{study_area}.pickle`
* `../data/ref_edges_simplified_{study_area}.pickle`
* `../data/ref_nodes_joined_{study_area}.pickle`
* `../data/ref_edges_joined_{study_area}.pickle`
* `../data/ref_nodes_simplified_joined_{study_area}.pickle`
* `../data/ref_edges_simplified_joined_{study_area}.pickle`
* `../data/grid_{study_area}.gpkg`

**Output files of this notebook:**
* `../results/ref_instrinsic_analysis_{study_area}.json`
* `../results/grid_results_intrinsic_{study_area}.pickle`
* `../results/plots/folium_multiple_edges_map_ref.html`
* `../results/plots/folium_danglingmap_ref.html`
* `../results/plots/folium_overundershoots_ref.html`
* `../results/plots/folium_component_gaps_ref.html`
