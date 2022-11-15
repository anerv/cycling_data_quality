NEW comments

GENERAl 
* what is our lingo? (we, the user, you..?) - *should be more passive!*
* update the markdown cells in the scripts/notebooks?  - *ok*
* typo correction? - *ok* 
* results folder has a data subfolder - *confusing - ok*
* numbers: if we print, we plot? if we print, we save to csv? - *add csv is it is nowhere else (but check at bottom first)*
* "edges" with capital E in folium layer legend - *edit*
* global/local: make explanation more prominent, e.g. already in the loaddata notebooks? *add description of grid plot, and then add (at grid cell level) every time "local" is introduced in subsection*
* increase fontsize for geopandas titles (esp. for 03a) *do it*
* edge density in KM per km2? *no* 
* OSM/REF in small or big? *change if any*
* EPB paper

AD README
* clean up gitignore? *later --> add to todos_final*
* may I edit readme? (will you see my changes highlighted?) *yes*
* readme: numbers for steps so that it is easier to look up stuff for each step? *add as todo for Ane*
* readme: limitations: this should be in the paper? and the github repo will reference to the paper? *yes*
* how will readme_extended be used? *get rid of it*
* look at todos together? *ok*
* conda env create: after 40 mins all conflicts were resolved but "could not find env with that name" 
* add conda activate cdq_new *yes*
* in jupyter lab: i couldn't run the setup_folder.py file? *move "setup folders" to top; jupyter lab should be just one of the options!*
* move troubleshooting to the bottom? *move it --> both load_data notebooks*
* maybe have quick readmes e.g. for format of reference data set? put in folder where the file has to be and link to there from the main readme
* footnote 2: updated how? fileformat --> be clearer; *move "once has been created..." to "input requirements"*
* reference data requirements: "have start/end nodes at intersections" --> explain in more detail? *yes*
* configuration file: "that are not completely intuitive" --> remove *ok*
* get in touch: rather through github? *no*
* "next step is running all notebooks" is missing! *insert*

AD 01a
* m vs. km2: use only km? (also ref) *ok*
* barplot of loaded network? (also ref) *YES - also reference - and use same colors etc.* 

AD 02a
* give the subsections subnumbers? (also 02b, 03a, ) *YES*
* OSM tag analysis: shorten markdown by reducing section description? *ok*
* tag analysis percentages: suggestion *ok*
* tag analysis csv: add "rounded" to km *yes*
* local/global incompatible tags: not clear; heading lacking (for folium plot) *rename into: incompatible tags - per gridcell/geometries*
* tagging type folium legend: html hack? (misz) *for later*
* tagged in multiple ways: why not as folium plot? *add*
* simplification outcome: why not keep only the node degree distribution? (also in 02b, 03a) *ok*
* save ndd to csv? *no*
* multiple edges: OK to remove *ok*
* overshoot edge id: how to relate back to e.g. osm? (also ref) *add in load_data*
* overshoot csv: save length? (also ref) *ok*
* missing intersection nodes: make an "if" around saving csv (also ref) *ok*
* lcc: make it stand out more? (also ref) *yes, and add other components, and legend!*
* summary: include total network length etc.; reorder: start with absolute values, later: densities etc. (also ref) *YES*

AD 02b
* couldnt read ref graph (the non.simplified one *troubleshoot-local vresion*
* add "static" and "interactive" in description, instead of "folium" (to match the folder titles) *ok*

AD 03a
* *add simplification (node degree distribution)* 
* overview text: emphasis on what differences mean! not starting point but "baseline"; clearer example *in the title: OSM as "baseline" and say that it is a comparison with REF; add explanation: "negative"*
* "if any" --> "or discarded"
* length percentages: changed function: instead of always taking the higher value as baseline, we always take OSM as baseline *YES*
* total network infrastructure length: change to km? *YES*
* global average: rather local average!! *add "average per km2*
* local network densities color bars: is this a problem? *YES-replot*
* barplots for densities of protected/unprotected infra: bring bars together *yes*
* differences in infra type density: move title 1 up; "streets" is it the right term? *infrastructure*
* alpha beta gamma: explain also what cycles, edges etc. are (what does "possible" mean?) *ok - also because it is not in the extrinsic!*
* maybe a feature request: what would be typical *ranges*? *NO*
* abc barplot: geometric length -- km or m?
* ndd before/after: horizontal, not vertical *IMPORT the plots!*
* multiple edges: remove


OLD comments

See below: comments for 01a, 01b, and 02a for sections 1 and 2 (i didn't touch the 2a.3 Network topology section yet)


* i found a way to insert a draggable legend into the folium plots! and very excited about it see the section 02a - Folium plot of tagging types, and /settings/htmllegend.py for a link to a website where it's (kind of) explained plus the html code behind the legend. this could maybe be a "homework" for michael? he might have a good idea on how to insert our python-based specifications of color vs. legend item into the html code. i just filled it with sample colors/legend items for now.

* filenames of images: to discuss - now we have all fig filenames starting with folium_, gpd_ or plt_ but might be not relevant for user - maybe have only 2 different prefixes, 1 for folium (not "folium" but "interactive" or smth like that but shorter) and the other one for plt/gpd ("image" or the like)?

* figsize is now controlled from pdict["fsmap"] etc. (rather than defining an aspect ratio; it's the "shortcut" since we can in that way control the output within the notebook; but we can talk about it to Michael what would make more sense)

* i added filepaths for figsaving in results/.../{studyarea} subfolders to paths.py

* we could discuss figure titles in general (and whether some print statements can be omitted then, e.g. about number of gridcells etc.)

* how is the reference data coverage in sqkm computed? does it make sense to have this (as a different value than the study area?)
(based on the convex hull of the graph, if we are talking about the value in the load data notebooks)


* 02a: tag analysis percentages: not adding them to the csv export at the moment - to discuss if needed both for edgecount and for km?; 02a stats_tags.csv - to discuss if it makes sense (also with the rounding etc.)
* 02a: # @Ana - do we want to plot both the count and length of existing/missing tags? --> not sure about this! but i think it's fine to generate all the images that are there now (and to also show them). what we could talk about is whether to format them a bit differently (maybe different colors?) for length vs. edge count? or just to plot them separately (maybe in 2 separate loops, or within 2 subplots of the same figure) for length vs. edgecount.

* i'm splitting the gpd-generated plots so that they are all independent figures (rather than subplots of 1 figure) so that we can also save and process them independently later on

* tbd: folium background maps - which ones should be there by default, which ones can be made optional? (having several background maps can make it slow to load) 

* your comment on competing tagging patterns: "small multiple plot" --> i didn't get what you mean by that?
I meant that it maybe could be in the style of the plots in the old summary notebook - so they are a bit smaller and all tiled in the same plot... 
maybe it doesn't make sense, but I was thinking that it is the overview/comparison which is more important than having each plot on their own?

* 02a competing tags: for each tag combination, i'm first plotting the grid (with color="none") to get the same map everytime (otherwise geopandas zooms in) - but can maybe also be used to highlight the cells in which there is a competing tag situation? so that the competing tags that appear few times are still visible on the gpd plot). another option would be to replace this with a folium plot with one layer for each competing tagging type combination (if we manage to get the html legend to work :) and add markers etc. --> to discuss