import yaml
from src import evaluation_functions as ef

with open(r'../../config.yml') as file:

    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    # Settings for study area
    study_area = parsed_yaml_file['study_area']
    study_crs = parsed_yaml_file['study_crs']

    # Settings for OSM data
    use_custom_filter = parsed_yaml_file['use_custom_filter']
    custom_filter = parsed_yaml_file['custom_filter']
    cycling_infrastructure_queries = parsed_yaml_file['cycling_infrastructure_queries']
    osm_cycling_infrastructure_type = parsed_yaml_file['osm_cycling_infrastructure_type']
    osm_way_tags = parsed_yaml_file['osm_way_tags']

    # Settings for reference data
    reference_comparison = parsed_yaml_file['reference_comparison']
    reference_geometries = parsed_yaml_file['reference_geometries']
    cycling_bidirectional = parsed_yaml_file['bidirectional']
    ref_cycling_infrastructure_type = parsed_yaml_file['ref_cycling_infrastructure_type']
    reference_id_col = parsed_yaml_file['reference_id_col']

    grid_cell_size = parsed_yaml_file['grid_cell_size']

    missing_tag_dict = parsed_yaml_file['missing_tag_analysis']
    incompatible_tags_dict = parsed_yaml_file['incompatible_tags_analysis']

study_area_poly_fp = f'../../data/study_area_polygon/{study_area}/study_area_polygon.gpkg'
reference_fp = f'../../data/reference/{study_area}/raw/reference_data.gpkg'

ef.check_settings_validity(
    study_area, 
    study_area_poly_fp, 
    study_crs, 
    use_custom_filter, 
    custom_filter, 
    reference_comparison,
    reference_fp, 
    reference_geometries, 
    cycling_bidirectional, 
    grid_cell_size
    )
