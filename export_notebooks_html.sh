# Export all notebooks as HTML without code cells included

# Load data notebooks
jupyter nbconvert scripts/osm/1a_load_osm.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags remove_cell --no-input --to html

jupyter nbconvert scripts/reference/1b_load_reference.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags remove_cell --no-input --to html

# Intrinsic notebooks
jupyter nbconvert scripts/osm/2a_intrinsic_analysis_osm.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags no_export --no-input --to html

jupyter nbconvert scripts/reference/2b_intrinsic_analysis_reference.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags no_export --no-input --to html

# Extrinsic notebooks
jupyter nbconvert scripts/compare/3_extrinsic_analysis_metrics.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags no_export --no-input --to html

jupyter nbconvert scripts/compare/4_extrinsic_analysis_feature_matching.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags no_export --no-input --to html
