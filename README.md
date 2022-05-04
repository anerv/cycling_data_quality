# Cycling Data Quality

This repository contains a reproducible workflow for assessing the quality of open source data on cycling infrastructure networks.

Focus on OSM as starting point - but can just as well be repurposed for analysing data from other sources
Lot of research on OSM/VGI data quality - but only little focusing specifically on cycling - and we know that cycling data often lower quality than other sources (REF), that errors are not random, quality varies a lot + cycling features have their own challenges due to how they are mapped in OSM.

There are many aspects of data quality - and which are relevant depends on your use cases for data.
This analysis is specifically made for people working with network based research, where topology and the structure of the network have a big influence on results/outcomes.

The purpose is not to give any final assesment the data quality, but to highlight aspects that might be relevant for assessing whether the data for a given area is fit-for-use/purpose.
Up to the user - who whe assume often will have some familiarity with the study area - to decide whether the state identified issues are a problem.
Similarly, some aspects, such as unconnected components, might be a problem with data quality - or a problem with the build infrastructure - these things require local knowledge to assess.

The repository contains 3 elements:

- Data processing - convert to network and simplified structure.
- Intrinsic analysis - only uses OSM data
- Extrinsic analysis - 

## How to use the workflow

### Input requirements

- nodes at intersections
- only cycling infra
- col describing physical separation or not?

### Reference Geometries

Centerline or true geoms

Specify whether the cycling infrastructure in the reference data have been mapped as centerlines or true geometries.
Describes whether cycling infrastructure is digitised as one line per road segment (regardless of whether there are cycling infrastructure along both sides)
or if there are two distinct geometries mapped in situations with a bike path/track on both sides of a street.
Can be a value describing the whole dataset or the name of the column describing the situation for each row.
Valid values are: 'centerline' or 'true_geometries'.

### Config:

### Intrinsic Analysis

### Extrinsic Analysis

### Summary

### Limitations

Caution - MAUP
Interpretation

## Demonstration
To see how the workflow might be used...

## Data & Licenses

The repository includes test data from the following sources:

**OpenStreetMap**

© OpenStreetMap contributors

License: [Open Data Commons Open Database License](https://opendatacommons.org/licenses/odbl/)

**NVDB, Sweden**

© NVDB (Nationell Vägdatabas)

License: [Creative Commons](https://creativecommons.org/publicdomain/zero/1.0/legalcode.sv)

**GeoDanmark**

© SDFE ( Styrelsen for Dataforsyning og Effektivisering og Danske kommuner)

License: [GeoDanmark](https://www.geodanmark.dk/wp-content/uploads/2020/03/Vilk%C3%A5r-for-brug-af-frie-geografiske-data.pdf)

**Vejle Municipality**

© Vejle Kommune

License: [Open Data DK](https://www.opendata.dk/open-data-dk/open-data-dk-licens)

**City of Copenhagen**

© Københavns Kommune

License: [Open Data DK](https://www.opendata.dk/open-data-dk/open-data-dk-licens)

