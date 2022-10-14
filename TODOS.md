# TO-DO

## GENERAL

- ~~merge Ana's newest branch~~
- ~~Rethink logical structure of notebooks~~
- ~~script that ensures that folders exist (**ANE**)~~
- ~~Create data folder structure (study area parameter) (like 'https://drivendata.github.io/cookiecutter-data-science/#directory-structure') (**ANE**)~~
- ~~title in all notebooks (**ANE**)~~
- ~~script/function that loads settings in all notebooks (**ANE**)~~
- ~~script/function that loads data in all notebooks (**ANE**)~~
- ~~Merge adjacent markdown cells (**ANE**)~~
- ~~unconnected->disconnected (**ANE**)~~
- ~~cycling --> bicycle (**ANE**)~~
- ~~Highlight user configs with colored box (**ANE**)~~
- ~~Move user configs to separate cell - force users to define them (**ANE**)~~
- ~~Polish print-statements - make sure that all print statements are meaningful (e.g. generate network - good or bad?) (**ANE**)~~

- come up with name :) (and change title in all notebooks)
- DRY-WET/refactoring/maintainability
- start thinking from end product: summary pdf, what should it contain, how should it be written, how to have plots, tables, text?

- Find more lightweight format than graphml for storing graphs?

- Export all plots and results as images and csvs (consider that results should be possible to use for fixing OSM) (**ANA**)
- exported data/plots need metadata for parameter info (csv) (**ANA**)
- Cut average node degree? (in all notebooks) (**ANA**)

- switch to american english (**ANE**)
- switch to passive voice (**ANE**)

- generate report (html to pdf) with markdown and results (almost done - we need to add 'remove_cell' tag to cells that should not be included e.g. markdown above a code cell with no output) (**ANE**)
- ADD import warnings, warnings.filterwarnings('ignore') to all notebooks? (**ANE**)

## MICHAEL

- colors
- change all imported src functions to something more comprehensible (**ASK MICHAEL**)
- DRY folium plots?

## ANASTASSIA

### Plots

- all plots: work on title; export (with adjusted aspect ratio); add metadata in plotname; add print statement if nothing is plotted; plot filepaths - if used more than once, move them to paths.py??
- barplots: don't overlap, no xticks
- folium plots: add marker layer; add stamen lite as default background map; add legend?!; default parameters in all functions
- more rainbowy colormap, or use "parabolic" easing (to highlight low/high probs better). rethink colormap for diff plot: red=OSM is better
- components - plot components of size less than XX in the same color? (speedup)

- plot prob length of network components (complementary probability function) (Zipf) (**ANA**)

### Other

- export data into csvs / txt files
- remove "average node degree"

## Functions

- ~~change find_adjacent_component func (**ANE**)~~
- speed up matching?

## README

- add Michael's changes
- illustration of workflow
- update GeoDanmark attribution?
- rewrite --> don't use we
- update readme numbering of notebooks
- update summary descriptions
- Update README/config with format of polygon for study area
- recommend max study area size - refer to pyrosm for bigger areas
- Make advanced README with input/output files
- add instructions about reference data and folder structure (filepaths no longer provided in config!!)
- add instructions for how to export notebooks without code

## Config

## Load data

- ~~split (**ANE**)~~

## Intrinsinc OSM

- comments on how differences are computed
- check pct calculations

- ~~network density can be confusing (2 meanings - make clear) (**ANE**)~~
- ~~In the entire dataset, 22673 edges or 45.18 % have information about: surface. Could you also say the length (and its ratio?). more interesting for planners/policy (**ANE**)~~
- ~~Add better explanation of component gaps + change plotting (**ANE**)~~
- ~~summary dataframe (**ANE**)~~

- plot prob length of network components (complementary probability function) (Zipf) (**ANA**)
- different tagging plots: needs legend with colors (**ANA**)

- plotting of component gaps (**ANA**)

- add local node degree (later)
- add %cells reached? (**ANA**)

- update calculation of missing intersections (**ANE**)

## Intrinsic Reference

- comments on how differences are computed
- check pct calculations

- copy markdown from osm intrinsic (**ANE**)
- plot prob length of network components (complementary probability function) (Zipf) (**ANA**)
- plotting of component gaps (**ANA**)
- add local node degree (later)
- add %cells reached? (**ANA**)

- update calculation of missing intersections (**ANE**)

## Extrinsic Notebooks

- SHOULD BE REDONE IN A NEW NOTEBOOK
- include summary dataframe at end

- import results from intrinsic notebooks - check that results exist!
- comments on how differences are computed
- check pct calculations

- plot prob length of network components (complementary probability function) (**ANA**)

- node deg simplification diffs needed? is single not enough? (add pct plot)
- make plots from intrinsic notebooks smaller and emphasize the difference plots
- wrong direction? make more clear it is diff. Edge density differences ' + study_area + " [m/km2], relative to OSM data
- don't have headlines deeper than ####?
- don't repeat documentation
- is dangling node diff interesting?
- over/undershoots diff interesting? also hard to see
- components: use same cmap for ranking
- difference calculated only where both data available? Make it clear when this is the case, and when it isn't
- %cells reached supercool, but why not already in 02ab. nan color? more rainbowy colormap, or use "parabolic" easing (to highlight low/high probs better). rethink colormap for diff plot: red=OSM is better

## Feature Matching Notebook

- comments on how differences are computed
- NA plotting
- check pct calculations
- legend/explanation of folium map
- don't use red/green

- summary dataframe (**ANE**)

## Summary of findings

- does it make sense to do summary for just one dataset?
- change colors
- comments on how differences are computed
- NA plotting
- check pct calculations
- pct diff calculations in summary notebooks - -100%
- gives these things a human name, with a dict: edge_density_m_sqkm
- avoid bold fonts
- is a low component count really better?

## Case Studies

- Run the analysis on 2 areas/2 reference datasets
- Make separate copies of all notebooks with results
- save folium plots and display them
- Add GeoDanmark attribution to all maps with reference example data!

## Random

m1.save("exercise09_example_tesselation.html")
from IPython.display import IFrame
IFrame(src='exercise09_example_tesselation.html', width=900, height=700)

## Paper

## Structure

OSM
load + sum
intrinsic + sum

REF
load + sum
intrinsic + sum

Compare OSM REF
compare + sum
feature matching + sum

DATA

OSM
STUDYAREA
raw
processed

REF
STUDYAREA
raw
processed

COMPARE
STUDYAREA
processed

RESULTS

OSM
STUDYAREA

REF
STUDYAREA

COMPARE
STUDYAREA
