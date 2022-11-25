## TODOS FINAL

**GENERAL REVISION/CHECKLIST**
* passive voice; typos; OSM/REF in caps; call folium maps "interactive maps" instead of "folium maps"
* all printed numbers are saved and/or plotted
* densities are given in m/km2
* meters and kilometers in figures are always correctly computed, indicated and labelled
* for all comparisons, every cell where at least one of the two (osm, ref) is missing is labelled as "no data" (and not as 0 or +-100%)

**TODO - DISCUSS // @ANE:**
* note: new: subfigure colorbar size edits (implemented in plot_func.plot_multiple_grid_results, but might be useful for other stuff as well)
* to discuss: should "no data" in comparison be a union of "no data" of osm and ref, or...?
* check new alpha beta gamma descriptions (03a) --> do they make sense?
* is current TODOS.md obsolete? (other than geodanmark attributions; no-export markdown cells)
* is that ok to use `edges` rather than `edges_simplified` for global length stats? (01a&b)
* percentage comparisons: i thought about this for a while; my conclusion is that they only make sense for gridcells where we have both osm and ref data; so where any of the 2 is missing this should be labelled as "no data" rather than "100% more/less"
* summary results: i think that it makes most sense to just *remove* the comparison in difference/percentages, and for each metric just to give the 2 absolute values for osm and ref. we can talk about this later on as well and maybe you/michael have a different opinion but for now i removed it from the 03a summary
* length vs. infrastructure length!! somebody else should review this :D
* in config file and possibly elsewhere: explain that study area name is also used for folder structure, relevant especially if the same workflow is run for several places
* next meeting: paper talk & inspirations?
* i added the explicit creation of superior folders "data", "results" etc. to the setup_folders.py file. for me it didn't seem to work otherwise - might be redundant but now it's working for sure (given that no empty folders can be saved to github, etc.).

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
* @readme: either https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository or download zip
* add somewhere that we assume meters everywhere? --> we assume a projected CRS with meters as unit length. --> add in README and in config file
* 03a ndd: which version? --> the import-plots one
* alpha beta gamma: explain also what cycles, edges etc. are (what does "possible" mean?) 
* feature request (FR): global network metrics - should this also exist in terms of length? --> YES: print information on both count and length; but plot only length. (in 01a and 01b)
* 2a tagged in multiple ways --> add as folium plot? *add* 
* 03a local network densities color bars: is this a problem? *YES-replot* *modify function!*
* summary reorder: start with absolute values, later: densities etc. 
* review 03b
