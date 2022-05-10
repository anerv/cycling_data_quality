# Reproducible Quality Assessment of OSM Data for Cycling Research


This repository contains a reproducible workflow for assessing the quality of OSM data on cycling infrastructure.

A fair amount of research projects on OSM and other forms of volunteered geographic information (VGI) have already been conducted - but few focus explicitly on cycling infrastructure, although we know that paths and tracks for cyclists and pedestrians often are among the latter features to be mapped, and once they do, are more likely to have errors (**REF**). Moreover, the location of errors and dips in data quality in crowdsourced data are often not random (**REF**), which necessitates a critical stance towards the data we use for our research, despite the overall high quality of OSM.

The goal behind this workflow is to give researchers and others working with OSM data for research centred on cycling networks an a method for getting a quick overview of the OSM data quality in a given area.

'Data quality' covers a wide range of aspects. The conceptualisation of data quality used here is what is refered to as 'fitness-for-use' (**REF**) - this means that data quality is interpreted as whether or not the data fulfils the user needs, rather than any unversal definition of quality. We do research based on networks, which means that we are particularly interested in the cores structure of the cycling infrastructure in OSM, data topology, and the data coverage.

The purpose is not to give any final assessment of the data quality, but to highlight aspects that might be relevant for assessing whether the data for a given area is fit for use. While the workflow does make use of a reference data set for comparison, if one is available, the ambition is not to give any final assessment of the quality of OSM compared to the reference data. OSM data on cycling infrastructure is often at a comparable or higher quality than government data sets, and the interpretation of differences between the two thus requires some local knowledge.

The repository contains 4 elements:

1. Data processing: This notebook downloads data from OSM and processes it to the format needed for the analysis. If any reference data is provided, it will also be converted to a simplified network format here.

2. Intrinsic analyis: This notebook attempts to understand the quality of the OSM data in the study area from the perspective of cycling research. We look at aspects such as missing tags, unconnected components, and network gaps (future editions will also look use history of OSM edits and contributor meta data).

3. Extrinsic analysis: The third notebook evolves around a comparison of the OSM data with a reference data set. The analysis looks at for example differences in network density and structure, differing connectivity across the study area, and feature matching.

4. Summary of results: This notebook summarises the findings from notebook 2 & 3 to a final report, that can be used for assessing the data quality of the OSM and, if available, the reference data.

## How to use the workflow

The intrinsic and extrinsic notebooks can be run independently, but you must run 'load_data.ipynb' first.
The 

### Input requirements

- Polygon
- Reference data
- Update config

#### Reference data

- nodes at intersections
- only cycling infra
- col describing physical separation or not/protected unprotected
- col describing 

#### config.yml

### Reference Geometries

Centerline or true geoms

Specify whether the cycling infrastructure in the reference data have been mapped as centerlines or true geometries.
Describes whether cycling infrastructure is digitised as one line per road segment (regardless of whether there are cycling infrastructure along both sides)
or if there are two distinct geometries mapped in situations with a bike path/track on both sides of a street.
Can be a value describing the whole dataset or the name of the column describing the situation for each row.
Valid values are: 'centerline' or 'true_geometries'.


### Intrinsic Analysis

### Extrinsic Analysis

### Summary

### Limitations

Caution - MAUP
Interpretation

## Demonstration

To see how the workflow might be used...

## Get in touch!

Do you have any suggestions for additional metrics or ways to improve the workflow?
Reach us at anev@itu.dk (Ane Rahbek Vierø) or anevy@itu.dk (Anastasia Vybornova).

## Data & Licenses

The repository includes test data from the following sources:

**OpenStreetMap**

© OpenStreetMap contributors

License: [Open Data Commons Open Database License](https://opendatacommons.org/licenses/odbl/)


**GeoDanmark**

© SDFE ( Styrelsen for Dataforsyning og Effektivisering og Danske kommuner)

License: [GeoDanmark](https://www.geodanmark.dk/wp-content/uploads/2020/03/Vilk%C3%A5r-for-brug-af-frie-geografiske-data.pdf)


**City of Copenhagen**

© Københavns Kommune

License: [Open Data DK](https://www.opendata.dk/open-data-dk/open-data-dk-licens)

The code in this repository is made avialble under XXX license.
Please cite XXX when using.