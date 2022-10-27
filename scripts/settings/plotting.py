import matplotlib as mpl

mpl.rcParams["savefig.bbox"] = "tight"
mpl.rcParams["xtick.minor.visible"] = False
mpl.rcParams["xtick.major.size"] = 0
mpl.rcParams["xtick.labelbottom"] = True
mpl.rcParams["ytick.major.size"] = 3

# Exact colors used
green = "#58ad6f"  # "#4dac26"
pink = "#d01c8b"
purple = "#5c40c5"
dark_orange = "#c55c40"
red = "#B72b05"
blue = "#40a9c5"
yellow = "#F1cd18"
light_blue = "#A8EBEC"

# pdict for plotting styles
pdict = {
    # grid; polygon; base barplots
    "base": green,  # green,
    "osm": purple,  # or keep it black and grey?
    "ref": dark_orange,  # or keep it black and grey?
    # osm network in geopandas and folium plots
    "osm_base": "black",  # base: for nodes and edges
    "osm_emp": red,  # emphasis: for dangling nodes, component issues, etc.
    "osm_emp2": blue,  # emphasis 2: for 2-fold distinctions e.g. over/undershoots
    # reference network in geopandas and folium plots
    "ref_base": "grey",  # base: for nodes and edges
    "ref_emp": dark_orange,  # emphasis: for dangling nodes, component issues, etc.
    "ref_emp2": purple,  # emphasis 2: for 2-fold distinctions e.g. over/undershoots
    # colormaps for grid cell plots
    "edgeden": "Purples",  # edge densities
    "nodeden": "Oranges",  # node densities
    "dens": "Blues",  # other densities: e.g. dangling nodes, protected infrastructure
    "miss": "Reds",  # missing values / issues; e.g. tags
    "diff": "PRGn",  # for osm-ref difference plots
    "seq": "PuBu",  # "inferno",  # for sequential plots (e.g. % of grid cells reached)
    # alpha (transparency) values
    "alpha_back": 0.5,  # for unicolor plots with relevant background
    "alpha_bar": 0.7,  # for partially overlapping stats barplots
    "alpha_grid": 0.8,  # for multicolor/divcolor gridplots
    "alpha_nodata": 0.5,  # for no data patches
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
    "basecols": [
        blue,
        green,
        red,
        light_blue,
        purple,
        yellow,
        "black",
        dark_orange,
    ],
    # for segment matching: matched vs unmatched features
    "match": green,
    "nomatch": pink,
    # for segment matching: semistransparent segment matches plot
    "osm_seg": blue,
    "osm_alpha": 0.7,
    "osm_weight": 4,
    "ref_seg": dark_orange,
    "ref_alpha": 0.7,
    "ref_weight": 6,
    "mat_seg": "#4dac26",
    "mat_alpha": 1,
    "mat_weight": 3,
    # Colors of no-data grid cell patches
    "nodata": "grey",
    "nodata_osm": "grey",  # purple,
    "nodata_ref": "grey",  # orange,
    "nodata_face": "none",
    "nodata_osm_face": "none",
    "nodata_ref_face": "none",
    "nodata_edge": "grey",
    "nodata_osm_edge": "grey",  # purple,
    "nodata_ref_edge": "grey",  # orange,
    "nodata_hatch": "//",
    "nodata_osm_hatch": "||",
    "nodata_ref_hatch": "o",
    # GLOBAL SETTINGS FOR PLOTS
    "dpi": 300,  # resolution
    # matplotlib figure size for map plots of study area
    "fsmap": (15, 7),
}

# patches for geopandas plots legend of "no data"
import matplotlib.patches as mpatches

nodata_patch = mpatches.Patch(
    facecolor=pdict["nodata_face"],
    edgecolor=pdict["nodata_edge"],
    label="No data",
    hatch=pdict["nodata_hatch"],
    alpha=pdict["alpha_nodata"],
)
nodata_osm_patch = mpatches.Patch(
    facecolor=pdict["nodata_osm_face"],
    edgecolor=pdict["nodata_osm_edge"],
    label="No OSM data",
    hatch=pdict["nodata_osm_hatch"],
    alpha=pdict["alpha_nodata"],
)
nodata_ref_patch = mpatches.Patch(
    facecolor=pdict["nodata_ref_face"],
    edgecolor=pdict["nodata_ref_edge"],
    label="No reference data",
    hatch=pdict["nodata_ref_hatch"],
    alpha=pdict["alpha_nodata"],
)

incompatible_true_patch = mpatches.Patch(
    facecolor=purple,
    edgecolor=purple,
    label="Incompatible tag combinations",
    alpha=pdict["alpha_grid"],
)

incompatible_false_patch = mpatches.Patch(
    facecolor=light_blue,
    edgecolor=light_blue,
    label="No incompatible tag combinations",
    alpha=pdict["alpha_grid"],
)

import contextily as cx

cx_tile_1 = cx.providers.CartoDB.Voyager
cx_tile_2 = cx.providers.Stamen.TonerLite
