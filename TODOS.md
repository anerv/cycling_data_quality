# TO-DO

## GENERAL

- ~~merge Ana's newest branch~~
- come up with name :)
- DRY-WET/refactoring/maintainability
- start thinking from end product: summary pdf, what should it contain, how should it be written, how to have plots, tables, text?
- switch to american english
- title in all notebooks
- make sure that all print statements are meaningful (e.g. generate network - good or bad?)
- Add print statements if nothing is plotted
- Create data folder structure (study area parameter) (like 'https://drivendata.github.io/cookiecutter-data-science/#directory-structure')
- Find more lightweight format than graphml for storing graphs?
- script that ensures that folders exist
- script/function that loads settings and data in all notebooks
- Export all plots and results as images and csvs (consider that results should be possible to use for fixing OSM)
- exported data/plots need metadata for parameter info (csv)
- Rethink logical structure of notebooks
- Cut average node degree? (in all notebooks)
- generate report (html to pdf) with markdown and results
- create bash setup script file
- See if we can have a legend for folium plots
- change all imported src functions to something more comprehensible
- unconnected->disconnected
- cycling --> bicycle
- Merge adjacent markdown cells
- Add summary dataframes to all notebooks

## Plots

- Don't overlap bars
- For Folium plots with potentially very few features plotted - create separate marker layer that makes it easier to find them
- Use Stamen Lite or similar as default background map
- Make titles longer/explain the content better
- Remove x-ticks from all bar-plots
- aspect ratios of exported plots all over the place
- colors: colorpicker etc

## Functions

- speed up check_intersections
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

## Config

## Load data

- plot osm and reference on top of each other?
- Consider splitting

## Intrinsinc OSM

- change colors
- comments on how differences are computed
- NA plotting
- check pct calculations

- dangling node plots - make smaller
- plot prob length of network components (complementary probability function) (Zipf)
- In the entire dataset, 22673 edges or 45.18 % have information about: surface. Could you also say the length (and its ratio?). more interesting for planners/policy
- different tagging plots: needs legend with colors
- simplification: nicer output, and possibly semilogy
- Add better explanation of component gaps + change plotting
- remove part with contributor data
- network density can be confusing (2 meanings - make clear)
- danling_node_density - spelling error in code
- add local node degree
- add components per cell
- add %cells reached?

## Intrinsic Reference

- change colors
- comments on how differences are computed
- NA plotting
- check pct calculations

- dangling node plots - make smaller
- plot prob length of network components (complementary probability function) (Zipf)
- simplification: nicer output, and possibly semilogy
- Add better explanation of component gaps + change plotting
- network density can be confusing (2 meanings - make clear)
- danling_node_density - spelling error in code
- add local node degree
- add components per cell
- add %cells reached?

## Extrinsic Notebooks

- import results from intrinsic notebooks - check that results exist!
- change colors
- comments on how differences are computed
- NA plotting
- check pct calculations

- plot prob length of network components (complementary probability function)

- node deg simplification diffs needed? is single not enough?
- make plots from intrinsic notebooks smaller and emphasize the difference plots
- wrong direction? make more clear it is diff. Edge density differences ' + study_area + " [m/km2], relative to OSM data
- don't have headlines deeper than ### ?
- don't repeat documentation
- is dangling node diff interesting?
- over/undershoots diff interesting? also hard to see
- components: use same cmap for ranking
- difference calculated only where both data available? Make it clear when this is the case, and when it isn't
- %cells reached supercool, but why not already in 02ab. nan color? more rainbowy colormap, or use "parabolic" easing (to highlight low/high probs better). rethink colormap for diff plot: red=OSM is better

## Feature Matching Notebook

- change colors
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
