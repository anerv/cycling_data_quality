# Reproducible Quality Assessment of OpenStreetMap Data for Bicycle Research

This repository contains a reproducible workflow for assessing the quality of OSM data on bicycle infrastructure. The aim is to provide researchers and others who work with OSM data for research centered on bicycle networks an informed overview of the OSM data quality in a given area.

A fair amount of research projects on OpenStreetMap (OSM) and other forms of volunteered geographic information (VGI) have already been conducted, but few focus explicitly on bicycle infrastructure. Doing so is important because paths and tracks for cyclists and pedestrians are often mapped last and are more likely to have errors ([Barron et al., 2014](https://onlinelibrary.wiley.com/doi/10.1111/tgis.12073), [Neis et al. 2012](https://www.mdpi.com/1999-5903/4/1/1)). Moreover, the spatial distribution of errors and dips in data quality in crowdsourced data are often not random ([Forghani and Delavar, 2014](https://www.mdpi.com/2220-9964/3/2/750)), which necessitates a critical stance towards the data we use for our research, despite the overall high quality of OSM.

'Data quality' covers a wide range of aspects. The conceptualisation of data quality used here is what is refered to as 'fitness-for-purpose' ([Barron et al., 2014](https://onlinelibrary.wiley.com/doi/10.1111/tgis.12073)) - this means that data quality is interpreted as whether or not the data fulfils the user needs, rather than any unversal definition of quality. To particularly support network-based research, this workflow provides insights into the topological structure of the bicycle network apart from data coverage.

The purpose is not to give any final assessment of the data quality, but to highlight aspects that might be relevant for assessing whether the data for a given area is fit for use. While the workflow does make use of a reference dataset for comparison, if one is available, the ambition is not to give any final assessment of the quality of OSM compared to the reference data. OSM data on bicycle infrastructure is often at a comparable or higher quality than government datasets, and the interpretation of differences between the two thus requires some local knowledge.

## Workflow structure

The workflow is divided into 3 elements: **OSM**, aimed at analyzing OpenStreetMap data, **reference**, designed for evaluating non-osm bicycle network data, and **comparison**, for comparing OSM and reference data.

The OSM and reference elements can be run independently, but for comparing the data, the notebooks for processing both OSM and reference data must be run first.

### Notebooks

All analysis notebooks are located in the scripts folder.

#### OSM

- **[01a_load_osm](scripts/osm/01a_load_osm.ipynb):** This notebook downloads data from OSM, processes it to the format needed in the analysis.

- **[02a_intrinsic_analysis_osm](scripts/osm/02a_intrinsic_analysis_OSM.ipynb):** The intrinsic analyses evaluates the quality of the OSM in the study area from the perspective of bicycle research. This evaluation includes, for example, missing tags, disconnected components, and network gaps. *Intrinsic* means that the dataset is analyzed for itself without being compared to other data.

#### Reference

- **[01b_load_reference](scripts/reference/01b_load_reference.ipynb):** This notebook processes the provided reference data to the format needed in the analysis.

- **[02b_intrinsic_analysis_reference](scripts/reference/02b_intrinsic_analysis_ref.ipynb):** The intrinsic analyses evaluates the quality of the OSM in the study area from the perspective of bicycle research. This evaluation includes, for example, disconnected components and network gaps. *Intrinsic* means that the dataset is analyzed for itself without being compared to other data.

#### Compare

- **[03a_extrinsic_analysis_metrics](scripts/compare/03a_extrinsic_analysis_metrics.ipynb):** The extrinsic analysis compares the results computed in the intrinsic analysis of the OSM and reference data. The analysis considers for example differences in network density and structure, and differing connectivity across the study area.
- **[03b_extrinsic_analysis_feature_matching](scripts/compare/03b_extrinsic_analysis_feature_matching.ipynb):** The fourth notebook contains functionality for matching corresponding features in the reference and OSM data. This step is more computationally expensive, but gives an excellent overview of different geometries and/or errors of missing or excess data.

---

## How to use the workflow

After setting up the environment and folder structure and filling out the configurations, the notebooks for OSM data (<span style="color:blue;">blue</span>) and the notebooks for the reference data (<span style="color:orange;">orange</span>) can be run independently[^1], but both must be run before the extrinsic analysis can be performed.

Once the desired parts of the analysis has been completed, the notebooks including the resulting plots can be exported to HTML.

<div style='text-align: center;'>

<img src='images/workflow_illustration_2.png' width=700/>

</div>

For an example of how the workflow can be used, see the notebooks in the 'examples' folder.

### Setting up the Python environment and folder structure

To ensure that all packages needed for the analysis are installed, we recommend creating and activating a new conda environment using the `environment.yml`:

```
conda env create --file=environment.yml
conda activate cdq
```

If this fails, the environment can be created by running:

```
conda config --prepend channels conda-forge
conda create -n cdq_new --strict-channel-priority osmnx geopandas pandas networkx folium pyyaml matplotlib contextily jupyterlab haversine momepy nbconvert ipykernel
```

*This method does however not control the library versions and should only be used as the last option.*

The repository has been set up using the structure described in the [Good Research Developer](https://goodresearch.dev/setup.html). Once the repository have been downloaded, navigate to the main folder in a terminal window and run the command

```
pip install -e .
```

Lastly, add the environment kernel to Jupyter via:

```
python -m ipykernel install --user --name=cdq
```

Running Jupyter notbook,

```
jupyter lab
```

and select the `cdq` kernel on top right.

To create the folder structure required by the workflow, navigate to the main folder in a terminal window and run the Python file `setup_folders.py`

```
python setup_folders.py
```

This should return:

```
Successfully created folder data/osm/'my_studyarea'/
Successfully created folder data/reference/'my_studyarea'/
Successfully created folder data/compare/'my_studyarea'/
...
```

### Troubleshooting

Problems accessing functions located in the src folder: Check that `pip install -e .` was run successfully.

### Input requirements

To run the analysis, the user must:

- Provide a **polygon** defining the study area (see config.yml for accepted formats)
- Update the **config.yml** with settings for how to run the analysis (see below for details)
- If the extrinsic analysis is to be performed, a **reference dataset** must be provided

### Reference data

The reference dataset must be in a format readable by GeoPandas (e.g. GeoPackage, GeoJSON, Shapefile etc.)

For the code to run without errors, the data must:

- only contain **bicycle infrastructure** (i.e. not also the regular street network)
- have all geometries as **LineStrings** (not MultiLineStrings)
- have start/end nodes at **intersections**
- be in a **CRS** recognised by GeoPandas
- contain a column describing whether each feature[^2] is a physically **protected**/separated infrastructure or if it is **unprotected**
- contain a column describing whether each feture is **bidirectional** or not (see below for details)
- contain a column describing how features have been digitized (**'geometry type'**) (see below for details)
- contain a column with a unique **ID** for each feature

For an example of how a municipal dataset with bicycle infrastructure can be converted to the above format, see the notebooks [reference_data_preparation_01](examples/reference_data_preparation_01.ipynb) and [reference_data_preparation_02](examples/reference_data_preparation_02.ipynb).

### Configuration file

The configuration file `config.yml` contains a range of settings needed for adapting the analysis to different areas and types of reference data.
Below is an explanation of the settings that are not completely intuitive.

#### **Custom filter**

In the config.yml we provide one way of getting the designated bicycle infrastructure from OSM data. What is considered bicycle infrastructure - and how it is tagged in OSM - is however highly contextual. If you want to use your own filter for retrieving bicycle infrastructure, set `use_custom_filter` to *True* and provide the custom filter under the `custom_filter` variable. For an example of how it should be formatted, see the provided filter `bicycle_infrastructure_queries`.

*Please note that  all ':' in OSM column names are replaced with '_' in the preprocessing of the data to enable using pandas.query without errors.*

#### **Infrastructure type**

Similarly, the config.yml contains a dictionary with queries used to classify all edges as either protected, unprotected or mixed (if there is protected in one side and unprotected in the other side). Update if needed, but note that it should correspond to the queries used to define the bicycle infrastructuer - i.e. all edges should be classified as either protected, unprotected or mixed.

#### **Missing tag analysis**

In the intrinsic analysis, one element is to analyse how many edges have values for attributes commonly considered important for evaluating bikefriendliness. If you want to change which tags are analysed, modify the dictionary `missing_tags_analysis`. Please not that the relevant tags might depend on the geometry type (i.e. center line or true geometry, see below).

#### **Incompatible tags analysis**

OSM has guidelines, but no restrictions on how tags can be combined. This sometimes results in contradictory information, for example when a path is both tagged as *'highway=cycleway'* and *'bicycle=dismount'*. We have included a dictionary with a few examples of tag combinations that we consider incomptabile, but more entries can be added.

The dictionary is a nested dictionary, where the first key is a subdictionary with the name of the column - e.g. *'bicycle_infrastructure'*. The dictionary value for *'bicycle_infrastructure'* is the actual value for the column bicycle_infrastructure (e.g. *'yes'*), that is considered incompatible with a list of column-value combinations, available as a list of values for the sub-dictionary under *'yes'* as a key.

#### **Reference Geometries**

In the config.yml, the setting `reference_geometries` refers to how the bicycle infrastructure have been digitized. In this context we operate with two different scenarios: either the bicycle infrastructure has been mapped as an attribute to the center line of the road (this is often done when the bicycle infrastructure is running along or are part of a street with car traffic) *or* it has been digitized as it's own geometry.
In the first scenario you will only have one line, even in situations with a cycle track on each side of the street, while two cycletracks on each side will result in two lines in the second scenario.

If a dataset only includes one type of mapping bicycle infrastructure, you can simply set `reference_geometries` to either *'centerline'* or *'true_geometries'*.

If the data, like OSM, includes a variation of both, the data must contain a column named *'reference_geometris'* with values being either *'centerline'* or *'true_geometries'*, specifying the digitization method for each feature.

The illustration below shows a situation where the same bicycle infrastructure have been mapped in two different ways. The blue line is a center line mapping, while the red lines are from a dataset that digitizes all bicycle infrastructure as individual geometries.

<div style='text-align: center;'><img src='images/geometry_types_illustration.png' width=500/></div>

#### **Bidirectional**

Due to the different ways of mapping geometries described above, datasets of the same area will have vastly different lengths if you do not consider that the blue line on the illustration above is bidirectional, while the red lines are not. To enable more accuracte comparisons of length differences, the data must either contain a column *'bidirectional'* with values either True or False, indicating whether each features allows for bicycle in both directions or not.
If all features in the reference dataset have the same value, you can simply set `bidirectional` as either *True* or *False* in the config.yml.

<div style='text-align: center;'><img src='images/bidirectional_illustration.png' width=500/></div>

#### **Bicycle infrastructure type**

The 'bicycle infrastructure' type simply refers to whether infrastructure is protected (i.e. physically separated from car traffic) or unprotected (e.g. a bike path only marked with paint).

The setting requires a dictionary, `ref_bicycle_infrastructure_type` with two entries: `protected` and `unprotected`. For each entry a list of queries should be provided that returns respectively the protected or unprotected infrastructure.

For example, the query `"vejklasse == 'Cykelsti langs vej'"` returns all the protected bicycle infrastructure in the test data from GeoDanmark available in the repository.

<div style='text-align: center;'>

<img src='images/track_illustration.jpeg' width=250/>

*Protected cycle track. Attribution: [wiki.openstreetmap](https://wiki.openstreetmap.org/wiki/File:Sciezki_wroclaw_wyspianskiego_1.jpg)*

</div>

<div style='text-align: center;'>

<img src='images/cycle_lane_illustration.jpeg' width=380/>

*Unprotected cycle lane. Attribution: [wiki.openstreetmap](https://wiki.openstreetmap.org/wiki/File:Fietsstrook_Herenweg_Oudorp.jpg)*

</div>

### Exporting results

All notebooks will produce a number of figures and results, saved in the `results` folder.

To export the notebooks including the explanations and plots but without the code, navigate to the main folder in a terminal window and run:

```
sh export_notebooks.sh
```

This will generate all notebooks as HTML files.

*Please note: If you are doing the analysis for multiple study areas or with several parameter settings and wish to generate HTML reports for each instance, the notebooks must be exported each time.*

---

## Limitations

Although we in the design of the workflow attempt to cover the main aspects of data quality relevant to bicycle networks, there are some limitations to the current state of the method. In terms of data modelling, for the sake of simplicity, we make use of an undirected network. This means that it does not contain information about allowed travel directions, assumes movements in each direction on all links and therefore always represent streets and paths with one edge (instead of one for each direction of travel). The current state of the workflow does not make use of routing on the network, but for future iterations travelling directions, as well as including the underlying street network, might be necessary for accurate path computations.

Another limitation touches upon the core purpose of the workflow, and the type of result it can produce: since we do not operate with one dataset as ground truth against which another can be evaluated, we cannot conclude where the error lies when differences are identified. For a successful application of the workflow, we thus both expect the user to have some familiarity with OSM data structures and tagging conventions, but also enough knowledge of the study area to evaluate the results independently.

Furthermore we do not directly evaluate the positional accuracy of neither the OSM or the reference data - although a certain level of internal positional accuracy can be deduced from the feature matching. While some level of positional accuracy certainly is of importance, the internal structure and topology is of greater significance for the research questions we are working with.

A final word of caution concerns the use of grid cells for computing local values for quality metrics. While this has the benefit of highlighting spatial variation in potential errors and density of mapped features, it also introduces the problem of the 'modifiable areal unit problem' (MAUP) - meaning that imposing artifical spatial boundaries on our data can distort the results and highlight or disguise patterns based on how we delimit the study area.

---

## Demonstration

To see how the workflow might be used, see the notebooks in the 'Examples' folder.

---

## Get in touch

Do you have any suggestions for additional metrics or ways to improve the workflow?
Reach us at anev@itu.dk (Ane Rahbek Vierø) or anevy@itu.dk (Anastasia Vybornova).

---

## Data & Licenses

The repository includes test data from the following sources:

### OpenStreetMap

© OpenStreetMap contributors

License: [Open Data Commons Open Database License](https://opendatacommons.org/licenses/odbl/)

### GeoDanmark

© SDFE (Styrelsen for Dataforsyning og Effektivisering og Danske kommuner)

License: [GeoDanmark](https://www.geodanmark.dk/wp-content/uploads/2022/08/Vilkaar-for-brug-af-frie-geografiske-data_GeoDanmark-grunddata-august-2022.pdf)

### City of Copenhagen

© Københavns Kommune

License: [Open Data DK](https://www.opendata.dk/open-data-dk/open-data-dk-licens)

**Our code is free to use and repurpose under the [CC BY-SA 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/)**

[^1]: I.e., the notebooks for loading respectively OSM and reference data must be run *before* the corresponding intrinsic analysis notebook is run, but running the OSM notebooks can be done without running the reference notebooks and vice versa.

[^2]: We use the word 'feature' to refer to a network edge. Each row in the network edge geodataframes thus represents one feature.
