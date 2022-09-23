# Run this file while in the main folder
import os
import yaml

with open(r'config.yml') as file:

    parsed_yaml_file = yaml.load(file, Loader=yaml.FullLoader)

    study_area = parsed_yaml_file['study_area']


# Create folder structure for data
compare_data_path = 'data/compare/'
osm_data_path = 'data/osm/'
ref_data_path = 'data/reference/'

compare_results_path = 'results/compare/'
osm_results_path = 'results/osm/'
ref_results_path = 'results/reference/'

paths = [osm_data_path, ref_data_path, compare_data_path, osm_results_path, ref_results_path, compare_results_path]

for path in paths:
    sa_folder = path + study_area + '/'

    if not os.path.exists(sa_folder):
        os.mkdir(sa_folder)
        print('Successfully created folder ' + sa_folder)

# Create folders for raw data
for path in paths[0:2]:
    raw_path = path + study_area + '/raw/'

    if not os.path.exists(raw_path):
        os.makedirs(raw_path)
        print('Successfully created folder ' + raw_path)

# Create folders for processed data
for path in paths[0:3]:
    process_path = path + study_area + '/processed/'

    if not os.path.exists(process_path):
        os.makedirs(process_path)
        print('Successfully created folder ' + process_path)