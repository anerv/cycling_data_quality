# Libraries used in the workflow

osmnx
networkx
geopandas
pandas
momepy
haversine
matplotlib
contextily
folium
pyyaml
jupyterlab
ipykernel

conda config --prepend channels conda-forge
conda create -n cdq_new --strict-channel-priority osmnx geopandas pandas networkx folium pyyaml matplotlib contextily jupyterlab haversine momepy ipykernel

conda env export | cut -f -2 -d "=" | grep -v "prefix" > environment.yml
