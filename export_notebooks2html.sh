# Export all notebooks as HTML without code cells included

# OSM notebooks
jupyter nbconvert scripts/osm/1a_load_osm.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags noex --no-input --to html
mv scripts/osm/1a_load_osm.html exports/html/1a.html

jupyter nbconvert scripts/osm/1b_intrinsic_analysis_osm.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags noex --no-input --to html
mv scripts/osm/1b_intrinsic_analysis_osm.html exports/html/1b.html

# REFERENCE notebooks
jupyter nbconvert scripts/reference/2a_load_reference.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags noex --no-input --to html
mv scripts/reference/2a_load_reference.html exports/html/2a.html

jupyter nbconvert scripts/reference/2b_intrinsic_analysis_reference.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags noex --no-input --to html
mv scripts/reference/2b_intrinsic_analysis_reference.html exports/html/2b.html

# COMPARE notebooks
jupyter nbconvert scripts/compare/3_extrinsic_analysis_metrics.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags noex --no-input --to html
mv scripts/compare/3_extrinsic_analysis_metrics.html exports/html/3.html

jupyter nbconvert scripts/compare/4_extrinsic_analysis_feature_matching.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags noex --no-input --to html
mv scripts/compare/4_extrinsic_analysis_feature_matching.html exports/html/4.html
