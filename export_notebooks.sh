# Export all notebooks as HTML without code cells included

# Load data notebooks
jupyter nbconvert scripts/osm/01a_load_osm.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags remove_cell --no-input --to html

jupyter nbconvert scripts/reference/01b_load_REF.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags remove_cell --no-input --to html

# Intrinsic notebooks
jupyter nbconvert scripts/osm/02a_intrinsic_analysis_OSM.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags no_export --no-input --to html

jupyter nbconvert scripts/reference/02b_intrinsic_analysis_REF.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags no_export --no-input --to html

# Extrinsic notebooks
jupyter nbconvert scripts/compare/03a_extrinsic_analysis_metrics.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags no_export --no-input --to html

jupyter nbconvert scripts/compare/03b_extrinsic_analysis_feature_matching.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags no_export --no-input --to html
