# plot dictionary folium: fdict
# plot dictionary geopandas: gdict
# plot dictionary matplotlib: mdict

pdict = {

   # grid; polygon; base barplots
    "base": "green",
    "osm": "blue", # or keep it black and grey?
    "ref": "orange", # or keep it black and grey?

    # osm network
    "osm_base": "black", # base: for nodes and edges
    "osm_emp": "red", # emphasis: for dangling nodes, component issues, etc. 
    "osm_emp2": "blue", # emphasis 2: for 2-fold distinctions e.g. over/undershoots

    # reference network
    "ref_base": "grey", # base: for nodes and edges
    "ref_emp": "orange", # emphasis: for dangling nodes, component issues, etc. 
    "ref_emp2": "purple", # emphasis 2: for 2-fold distinctions e.g. over/undershoots

    # density plot colormaps
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

    # linewidths
    "line_base": 2,
    "line_emp": 3,
    "line_emp2": 5,

    # bar widths
    "bar_single": 0.5,
    "bar_double": 0.75,

    # marker sizes
    "mark_base": 1,
    "mark_emp": 2,

    # separate def for 02: tagging patterns multicolored - list of base colors:
    "basecols": ["b", "g", "r", "c", "m", "y", "k", "w"],

    # separate def for 03b: matched vs unmatched
    "match": "green",
    "nomatch": "red",

    # separate def for 03b: semistransparent segment matches plot
    "osm_seg": "blue",
    "osm_alpha": 0.4,
    "osm_weight": 4,

    "ref_seg": "yellow",
    "ref_alpha": 0.7,
    "ref_weight": 5,

    "mat_seg": "green",
    "mat_alpha": 0.5,
    "mat_weight": 3,

} 