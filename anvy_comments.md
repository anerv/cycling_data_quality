**GENERAL REVISION/CHECKLIST**
* passive voice
* typos
* OSM/REF in caps
* folium legend starting with caps
* replace "folium" by static/interactive everywhere in descriptive text
* all printed numbers are saved and/or plotted 
* densities are given in m/km2
* meters vs. kilometers vs. squarekilometers (check normalization etc.)

**TODO - CURRENT:**
* 03a local network densities color bars: is this a problem? *YES-replot* *modify function!*
* @readme: either https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository or download zip

**TODO - UPCOMING:**
* readme fig with step numbers (**ANE**)
* 2a tagged in multiple ways --> add as folium plot? *add* 
* summary reorder: start with absolute values, later: densities etc. 
* alpha beta gamma: explain also what cycles, edges etc. are (what does "possible" mean?) 
* review 03b
* add somewhere that we assume meters everywhere? --> we assume a projected CRS with meters as unit length. --> add in README and in config file
* 03a ndd: which version? --> the import-plots one
* feature request (FR): global network metrics - should this also exist in terms of length? --> YES: print information on both count and length; but plot only length. (in 01a and 01b)

**MONDAY DISCUSSED POINTS**

* simp outcome - always first
* 03a dangling_node_density_count_sqkm don't divide by 1000
* plot_func.make_bar_plot_side: added x_label (singular) 
* 03a from collections import Counter: is this an issue?
* added readme technical requirements: should we also add that we recommend VS code?
* added readme step of downloading repo: description?
* added in load_data: edge id description. enough?
* simplify simplification plot in 03a?
* rcParam settings for fontsize ok? maybe outsource to michael? (need to edit make_bar_subplots function!) https://matplotlib.org/3.1.1/tutorials/introductory/customizing.html#temporary-styling  
* missing intersection nodes for 2b?

**TODO - AFTER MONDAY**
* EPB paper
* tagging type folium legend: html hack? (misz) *for later*

**DONE**
* updated readme
* "next step is running all notebooks" is missing! *insert*
* footnote 2: updated how? fileformat --> be clearer; *move "once has been created..." to "input requirements"*
* reference data requirements: "have start/end nodes at intersections" --> explain in more detail? *yes*
* configuration file: "that are not completely intuitive" --> remove *ok*
* global/local: make explanation more prominent, e.g. already in the loaddata notebooks? *add description of grid plot, and then add (at grid cell level) every time "local" is introduced in subsection*
* clean up gitignore? *later --> add to todos_final*
* OSM tag analysis: shorten markdown by reducing section description? *ok*
* move troubleshooting to the bottom? *move it --> both load_data notebooks*
* give the subsections subnumbers? (also 02b, 03a, ) *YES*
* barplot of loaded network? (also ref) *YES - also reference - and use same colors etc.* 
* increase fontsize for geopandas titles (esp. for 03a) *do it*
* tag analysis percentages: suggestion *ok*
* tag analysis csv: add "rounded" to km *yes*
* local/global incompatible tags: not clear; heading lacking (for folium plot) *rename into: incompatible tags - per gridcell/geometries*
* simplification outcome: why not keep only the node degree distribution? (also in 02b, 03a) *ok*
* multiple edges: OK to remove *ok*
* overshoot csv: save length? (also ref) *ok*
* lcc: make it stand out more? (also ref) *yes, and add other components, and legend!*
* add xticks to ndd plot in 2b too
* overshoot csv: save length? (also ref) *ok*
* "if any" --> omit in 03a
* total network infrastructure length: change to km? *YES*
* length percentages: changed function: instead of always taking the higher value as baseline, we always take OSM as baseline *YES*
* ndd before/after: horizontal, not vertical *IMPORT the plots!*
* global average: rather local average!! *add "average per km2*
* maybe a feature request: what would be typical *ranges*? *NO*
* barplots for densities of protected/unprotected infra: bring bars together *yes*
* differences in infra type density: move title 1 up; "streets" is it the right term? *infrastructure*
* abc barplot: geometric length -- km or m?
* 03a overview text: emphasis on what differences mean! not starting point but "baseline"; clearer example *in the title: OSM as "baseline" and say that it is a comparison with REF; add explanation: "negative"*
* overshoot edge id: how to relate back to e.g. osm? (also ref) *add in load_data*