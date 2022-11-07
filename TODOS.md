# TO-DO

## GENERAL

- come up with name :) (and change title in all notebooks)

- DRY-WET/refactoring/maintainability

- start thinking from end product: summary pdf, what should it contain, how should it be written, how to have plots, tables, text?

- Find more lightweight format than graphml for storing graphs?

- Cut average node degree? (in all notebooks) (**ANA**)

- color scheme??

## MICHAEL

- colors
- DRY folium plots?

## ANASTASSIA

### Plots

- all plots: work on title; export (with adjusted aspect ratio); add metadata in plotname; add print statement if nothing is plotted;

- folium plots: add marker layer; add legend?!; default parameters in all functions
- more rainbowy colormap, or use "parabolic" easing (to highlight low/high probs better). rethink colormap for diff plot: red=OSM is better
- components - plot components of size less than XX in the same color? (speedup)

- plot prob length of network components (complementary probability function) (Zipf) (**ANA**)

### Other

- remove "average node degree"

## Functions

- speed up matching?

## README

- Make advanced README with input/output files

## Config

## Load data

## Intrinsinc OSM

- check pct calculations

- plot prob length of network components (complementary probability function) (Zipf) (**ANA**)
- different tagging plots: needs legend with colors (**ANA**)

- add local node degree (later)

## Intrinsic Reference

- check pct calculations

- plot prob length of network components (complementary probability function) (Zipf) (**ANA**)
- add local node degree (later)

## Extrinsic Notebooks

- markdown

- 'Relative to OSM data' - makes me think that negative values is less than OSM - but is the opposite?

- add 'no_export' tag to cells that should not be included e.g. markdown above a code cell with no output) (**ANE**)

- comments on how differences are computed in all places

- check pct calculations

- plot prob length of network components (complementary probability function) (**ANA**)

- node deg simplification diffs needed? is single not enough? (add pct plot)

- wrong direction? make more clear it is diff. Edge density differences ' + study_area + " [m/km2], relative to OSM data

- is dangling node diff interesting?
- over/undershoots diff interesting? also hard to see
- components: use same cmap for ranking
- difference calculated only where both data available? Make it clear when this is the case, and when it isn't

## Feature Matching Notebook

- comments on how differences are computed
- NA plotting
- check pct calculations
- legend/explanation of folium map

## Case Studies

- Run the analysis on 2 areas/2 reference datasets
- Make separate copies of all notebooks with results
- save folium plots and display them
- Add GeoDanmark attribution to all maps with reference example data!

## Random

m1.save("exercise09_example_tesselation.html")
from IPython.display import IFrame
IFrame(src='exercise09_example_tesselation.html', width=900, height=700)

Folium legend:

# add draggable legend (template!)

macro = MacroElement()
macro._template = Template(legend_template)
m.get_root().add_child(macro)

## Paper
