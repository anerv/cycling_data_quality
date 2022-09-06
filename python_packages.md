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
conda create -n cdq_new --strict-channel-priority osmnx=1.2.2 geopandas=0.11.1 pandas=1.4.3 networkx=2.8.6 folium=0.12.1.post1 pyyaml=6.0 matplotlib=3.5.3 contextily=1.2.0 jupyterlab=3.4.5 haversine=2.6.0 momepy=0.5.3 ipykernel=6.15.2

conda env export | cut -f -2 -d "=" | grep -v "prefix" > environment.yml
