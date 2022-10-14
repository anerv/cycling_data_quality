# pdict for plotting styles
pdict = {

   # grid; polygon; base barplots
    "base": "green",
    "osm": "blue", # or keep it black and grey?
    "ref": "orange", # or keep it black and grey?

    # osm network in geopandas and folium plots
    "osm_base": "black", # base: for nodes and edges
    "osm_emp": "red", # emphasis: for dangling nodes, component issues, etc. 
    "osm_emp2": "blue", # emphasis 2: for 2-fold distinctions e.g. over/undershoots

    # reference network in geopandas and folium plots
    "ref_base": "grey", # base: for nodes and edges
    "ref_emp": "orange", # emphasis: for dangling nodes, component issues, etc. 
    "ref_emp2": "purple", # emphasis 2: for 2-fold distinctions e.g. over/undershoots

    # colormaps for grid cell plots
    "edgeden": "Purples", # edge densities
    "nodeden": "Oranges", # node densities
    "dens": "Blues", # other densities: e.g. dangling nodes, protected infrastructure     
    "miss": "Reds", # missing values / issues; e.g. tags
    "diff": "seismic", # for osm-ref difference plots
    "seq": "plasma", # for sequential plots (e.g. % of grid cells reached)

    # alpha (transparency) values 
    "alpha_back": 0.5, # for unicolor plots with relevant background
    "alpha_bar": 0.7, # for partially overlapping stats barplots
    "alpha_grid": 0.8, # for multicolor/divcolor gridplots
    "alpha_nodata": 0.5, # for no data patches

    # linewidths (base, emphasis, emphasis2)
    "line_base": 2,
    "line_emp": 3,
    "line_emp2": 5,

    # widths for bar plots; single: for 1 value, double: for 2 values comparison
    "bar_single": 0.5,
    "bar_double": 0.75,

    # marker sizes (base, emphasis)
    "mark_base": 1,
    "mark_emp": 2,

    # list of colors for differing tagging patterns
    "basecols": ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "orange"],

    # for segment matching: matched vs unmatched features
    "match": "green",
    "nomatch": "red",

    # for segment matching: semistransparent segment matches plot
    "osm_seg": "blue",
    "osm_alpha": 0.4,
    "osm_weight": 4,

    "ref_seg": "yellow",
    "ref_alpha": 0.7,
    "ref_weight": 5,

    "mat_seg": "green",
    "mat_alpha": 0.5,
    "mat_weight": 3,
    
    # Colors of no-data grid cell patches
    "nodata": "black",
    "nodata_osm": "#90FFA1",
    "nodata_ref": "#FAFF90",

    # GLOBAL SETTINGS FOR PLOTS
    "dpi": 300, # resolution
    # matplotlib figure size for map plots of study area
    "fsmap": (15,7),
    
} 

# patches for geopandas plots legend of "no data"
import matplotlib.patches as mpatches
nodata_patch = mpatches.Patch(color=pdict["nodata"], label='No data')
nodata_osm_patch = mpatches.Patch(color=pdict["nodata_osm"], label='No OSM data')
nodata_ref_patch = mpatches.Patch(color=pdict["nodata_ref"], label='No reference data')