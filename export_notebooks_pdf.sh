# Export all notebooks as HTML without code cells included

# Load data notebooks
jupyter nbconvert scripts/osm/1a_load_osm.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags remove_cell --no-input --to pdf

jupyter nbconvert scripts/reference/1b_load_reference.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags remove_cell --no-input --to pdf

# Intrinsic notebooks
jupyter nbconvert scripts/osm/2a_intrinsic_analysis_osm.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags no_export --no-input --to pdf

jupyter nbconvert scripts/reference/2b_intrinsic_analysis_reference.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags no_export --no-input --to pdf

# Extrinsic notebooks
jupyter nbconvert scripts/compare/3_extrinsic_analysis_metrics.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags no_export --no-input --to pdf

jupyter nbconvert scripts/compare/4_extrinsic_analysis_feature_matching.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags no_export --no-input --to pdf

gs -q -dNOPAUSE -dBATCH -dPDFSETTINGS=/prepress -sDEVICE=pdfwrite -sOutputFile=report.pdf scripts/osm/1a_load_osm.pdf scripts/osm/2a_intrinsic_analysis_osm.pdf scripts/reference/1b_load_reference.pdf scripts/reference/2b_intrinsic_analysis_reference.pdf scripts/compare/3_extrinsic_analysis_metrics.pdf scripts/compare/4_extrinsic_analysis_feature_matching.pdf