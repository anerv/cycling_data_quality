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
