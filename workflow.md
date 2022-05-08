# Questions to be answered in the analysis
## Completeness 
- **Density of nodes/edges/attributes (possibly grid-cell based?)**
- **If reference data set available: How 'much' of an area's cycling infrastructure is mapped?**
    - Total length/total length of different types of infrastructure
    - Development in contributions (spatial heterogeneity!)

## Quality
- **How well is it mapped?**
    - Customized simplification: tag diversity; parallel edges etc.
    - Differences in network structure
    - Differences in routing
    - Matching of data sets
    - Missing tags
    - Number of contributors
    - Contribution history

## Regional/local differences
- Point out areas that are possibly more "interesting": e.g. where number of edits is especially high/low, where number of contributors is high/low, where data sets differ strongly (include also: where infrastructure is more sparse?)

<br/>


# Workflow

## Input requirements
- config file filled out (grid cell size if not using default; ref data set true/false; place name etc.)
- study area (polygon)
- optional: custom filter --> with note on "missing tags" possibly changing
For the reference data set:
- is it centralline-based or feature-based?
- column that indicates oneway/twoway (in any case)
- column that indicates separated yes/no (optional)
- If reference data - must have nodes at intersections

## Load Data
For OSM and potentially also reference data set:

**Possible first step for decision on customized filtering**
- have a default custom filter; optional (adding complexity/for proficient OSM users):
- Load network data with "all tags" and let user decide which tag combinations to use
- All tags that user interprets as cycling infrastructure --> possibly visualize how the separate "layers" are distributed? *Possibly just do this in the intrinsic analysis?* 
- possible quantification: compare statistics on disconnected components for each layer

**Load network data**
- ~~Clip to study area~~
- ~~Reproject~~
- ~~Convert to graph structure~~
- ~~Simplify~~
- ~~Compute simple descriptions of dataset (length, area covered, density)~~
- ~~decide on grid cell size~~
- Save to files: 
    - custom filter dictionary,
    - ~metadata raw graph (downloaded when?)~ 
    - ~~raw graph,~~
    - ~~simplified graph,~~ 
    - simplification outcome dictionary, 
    - ~~grid~~

## Intrinsic Analysis
- ~~**Missing tags**~~~
    - *References: Girres and Touya, 2010*
- **Simplification outcomes**
- **Metrics based on network topology**
    - possibly starting from *Boeing 2017, Barron 2014 ("consistency")*
    - both for total network and for grid cells (some of the metrics/adjust definitions)
    - **WORK IN PROGRESS** on grid cell interpretation of network topology
- **Logical/conceptual consistency**
    - E.g. different ways of tagging the same infrastructure - is this a problem? (possibly: color map of what part of the network corresponds to which custom filter entry) - is it really interesting?
    - ~~Combination of incompatible tags or meaningless tag values~~
    - *References: Barron et al, 2013; Girres and Touya, 2010*
- **WORK IN PROGRESS: Number of contributors**
    - Total and per grid cell
    - *References: Gröchenig et al, 2014; Neis et al, 2012*
- **WORK IN PROGRESS: Historical development in contributions over time**
    - Total and per grid cell
    - For different types of infra (also include general road network?)
    - *References: Gröchenig et al, 2014; Neis et al, 2012; Keßler and de Groot 2013; Keßler et al. 2011* 

"Logical consistency: this is an aspect of the internal consistency of the dataset, in terms of topological correctness and the relationships that are encoded in the database. ." (Haklay, 2010)

"logical consistency: internal consistency of the data, and the data set's adherence to its own defined rules." (Goodchild and Clarke, 2002)

 "The first inconsistency is identified by analyzing roads which do not share a common Node with another one and and lie within a radius of one meter. The second inconsistency is identified by calculating duplicate road geometries. The third inconsistency is detected by analyzing roads which intersect but do not share a common Node. This can also be caused by missing tags characterizing bridges or tunnels. These topological errors are calculated, quantified and subsequently visualized" (Barron et al, 2013)

 "logical consistency can be defined as “degree of adherence to logical rules of data structure, attribution, and relationships”. Four main sub-elements considered for logical consistency in this standard are conceptual consistency, domain consistency, format consistency, and topological consistency." (Hashemi and Abbaspour, 2015)

## Extrinsic Analysis
*Requires a reference data set.*
**Metrics are:**
- **Simplification outcomes (stand-alone)**
- **Matching with Ane's algorithm**
- **Length of different types of cycling infrastructure** (if separated yes/no column is available)
    - Total and per grid cell
    - *References:  Ferster et al, 2019;  Forghani and Delavar, 2014; Haklay, 2010; Hochmair et al, 2015*
- **Matched/unmatched edges**
    - plot partial overlap/lack of overlap and numbers on difference
- **Differing classification in the two datasets (for features that have been matched)** 
    - Total and per grid cell
    - *References: Brovelli et al, 2016; Koukoletsos et al, 2012; Girres and Touya, 2010; Alireza Chehreghan and Rahim Ali Abbaspour, 2018*
- **Comparison of network structure**
    - Repeat topological network analysis
    - E.g. number of connected components, alpha, beta and gamma, dangling nodes etc.
    - network diameter
- **Routing feasibility/shortest path**
    - Differences in shortest paths between abritary points (points on the network? Between all nodes?)
    - possibly only on grid-cell basis
    - *References: Graser et al, 2014; Mondzech and Sester, 2011*

## Interpretation and Presentation of results
- Analysis of identified errors/inconsistencies - e.g. spatial clustering/autocorrelation - is there a tendency?
- Autogenerated summary and plots
- e.g. generate a PDF - each page contains a figure and an explanatory text. or keep it in notebook only

# TO-DO

## README
- Everything

## Config

## Intrinsinc Notebook
- Plots + save plots (**Friday**)
- Add references, edit explanations

## Extrinsic Notebook
- Finish comparison of network structure **(Ane: Sunday)**
- Polish texts, references and explanations 
- Plots + save plots (**Friday**)
- Summary of findings **Thursday**

**SUNDAY**
- Plot cells which are connected in one dataset but not in another (grid connectivity) (3 hours)
- clean up notebooks, add explanations (2 hours)
- if time: feature matching


## Paper
- Keywords to all sections: **(Ane: Sunday)**
- First draft **(A+A: Monday + Tuesday)**

## Before FOSS4G:
- Fix **all** plots (make nicer, some folium)
- Write tests for all functions
- Polish text and explanations to notebooks
- Documentation, environment
- Update README: description, how to cite, contacts
- Make reference list for notebook refs
- remove matching functions from graph_functions.py etc.


## NICE TO:
- Convert to simple graph in load data notebook?
- Small function for creating columns with index
- Small function for joining grids to data
- Feature matching?
- More advanced snapping - check if they share an edge or whether their one of their edges share a node with the other node.        Alternatively also check for edges within buffer distance, and whether there is a path to them within XX distance
- Functions for node over/undershoots
- For merge - check if col already exist - if it does - drop
