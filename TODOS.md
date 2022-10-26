# TO-DO

## GENERAL

- come up with name :) (and change title in all notebooks)
- DRY-WET/refactoring/maintainability
- start thinking from end product: summary pdf, what should it contain, how should it be written, how to have plots, tables, text?

- Find more lightweight format than graphml for storing graphs?

- Export all plots and results as images and csvs (consider that results should be possible to use for fixing OSM) (**ANA**)
- exported data/plots need metadata for parameter info (csv) (**ANA**)
- Cut average node degree? (in all notebooks) (**ANA**)

- switch to american english (**ANE**)
- switch to passive voice (**ANE**)

## MICHAEL

- colors
- DRY folium plots?

## ANASTASSIA

### Plots

- all plots: work on title; export (with adjusted aspect ratio); add metadata in plotname; add print statement if nothing is plotted; plot filepaths - if used more than once, move them to paths.py??
- remove whitespace from plots
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

- Make advanced README with input/output files

## Config

## Load data

## Intrinsinc OSM

- check pct calculations

- plot prob length of network components (complementary probability function) (Zipf) (**ANA**)
- different tagging plots: needs legend with colors (**ANA**)

- plotting of component gaps (**ANA**)

- add local node degree (later)
- add %cells reached? (**ANA**)

- update filepaths for storing figures

## Intrinsic Reference

- check pct calculations

- copy markdown from osm intrinsic (**ANE**)
- plot prob length of network components (complementary probability function) (Zipf) (**ANA**)
- plotting of component gaps (**ANA**)
- add local node degree (later)
- add %cells reached? (**ANA**)

- change grid edge density etc as 'ref_edge_density' (**ANE**)

- update filepaths for storing figures

## Extrinsic Notebooks

- SHOULD BE REDONE IN A NEW NOTEBOOK
- include summary dataframe at end
- add 'remove_cell' tag to cells that should not be included e.g. markdown above a code cell with no output) (**ANE**)

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

Folium legend:

# add draggable legend (template!)

macro = MacroElement()
macro._template = Template(legend_template)
m.get_root().add_child(macro)
