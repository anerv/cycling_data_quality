import matplotlib as mpl
from matplotlib import cm, colors

mpl.rcParams["savefig.bbox"] = "tight"
mpl.rcParams["xtick.minor.visible"] = False
mpl.rcParams["xtick.major.size"] = 0
mpl.rcParams["xtick.labelbottom"] = True
mpl.rcParams["ytick.major.size"] = 3
mpl.rcParams["font.size"] = 12
mpl.rcParams["figure.titlesize"] = 12
mpl.rcParams["legend.title_fontsize"] = 10
mpl.rcParams["legend.fontsize"] = 9
mpl.rcParams["figure.labelsize"] = 10
mpl.rcParams["axes.labelsize"] = 10
mpl.rcParams["xtick.labelsize"] = 9
mpl.rcParams["ytick.labelsize"] = 9

def convert_cmap_to_hex(cmap_name, n=None):

    if n is None:
        cmap = cm.get_cmap(cmap_name)

    else:
        cmap = cm.get_cmap(cmap_name, n)

    hex_codes = []

    for i in range(cmap.N):

        hex_codes.append(mpl.colors.rgb2hex(cmap(i)))

    return hex_codes


# Exact colors used
pink_green_cmap = convert_cmap_to_hex("PiYG", 10)
pink = pink_green_cmap[1]
green = pink_green_cmap[-2]

orange_cmap = convert_cmap_to_hex("Oranges", 10)
orange = orange_cmap[5]
light_orange = orange_cmap[4]
dark_orange = orange_cmap[8]

purple_cmap = convert_cmap_to_hex("Purples", 10)
purple = purple_cmap[6]
light_purple = purple_cmap[4]
dark_purple = purple_cmap[8]


blue_cmap = convert_cmap_to_hex("Blues", 10)
blue = blue_cmap[6]
light_blue = blue_cmap[4]
dark_blue = blue_cmap[8]

red_cmap = convert_cmap_to_hex("Reds", 10)
red = red_cmap[6]
light_red = red_cmap[4]
dark_red = red_cmap[8]


# pdict for plotting styles
pdict = {
    # grid; polygon; base barplots
    "base": "black",  # green,
    "base2": "grey",
    # "osm": purple,  # or keep it black and grey?
    # "ref": dark_orange,  # or keep it black and grey?
    # osm network in geopandas and folium plots
    "osm_base": purple,  # base: for nodes and edges
    "osm_emp": dark_purple,  # emphasis: for dangling nodes, component issues, etc.
    "osm_emp2": light_purple,  # emphasis 2: for 2-fold distinctions e.g. over/undershoots
    "osm_contrast": convert_cmap_to_hex("cool", 10)[1],
    "osm_contrast2": convert_cmap_to_hex("cool", 10)[-1],
    # reference network in geopandas and folium plots
    "ref_base": orange,  # base: for nodes and edges
    "ref_emp": dark_orange,  # emphasis: for dangling nodes, component issues, etc.
    "ref_emp2": light_orange,  # emphasis 2: for 2-fold distinctions e.g. over/undershoots
    "ref_contrast": convert_cmap_to_hex("RdYlBu", 10)[1],
    "ref_contrast2": convert_cmap_to_hex("autumn", 10)[-2],
    # colormaps for grid cell plots
    "edgeden": "Blues",  # edge densities
    "nodeden": "Greens",  # node densities
    "dang_nodeden": "Oranges",  # dangling node densities
    "dens": "Purples",  # "Blues"  # other densities: e.g. dangling nodes, protected infrastructure
    "miss": "Reds",  # missing values / issues; e.g. tags
    "diff": "PRGn",  # for osm-ref difference plots (alternatives: "PiYG", "PRGn", "PuOr")
    "seq": "PuBu",  # for sequential plots (e.g. % of grid cells reached)
    # alpha (transparency) values (alternatives: PuRd, RdPu, PbBuGn)
    "alpha_back": 0.5,  # for unicolor plots with relevant background
    "alpha_bar": 0.7,  # for partially overlapping stats barplots
    "alpha_grid": 0.8,  # for multicolor/divcolor gridplots
    "alpha_nodata": 0.5,  # for no data patches
    # linewidths (base, emphasis, emphasis2)
    "line_base": 1,
    "line_emp": 3,
    "line_emp2": 5,
    # widths for bar plots; single: for 1 value, double: for 2 values comparison
    "bar_single": 0.4,
    "bar_double": 0.75,
    # marker sizes (base, emphasis)
    "mark_base": 2,
    "mark_emp": 4,
    # list of colors for differing tagging patterns
    "basecols": convert_cmap_to_hex("tab20"),
    # for segment matching: matched vs unmatched features
    "match": green,
    "nomatch": pink,
    # for segment matching: semistransparent segment matches plot
    "osm_seg": light_purple,
    "osm_alpha": 0.7,
    "osm_weight": 4,
    "ref_seg": light_orange,
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
    "fsmap": (16, 9),
    # size for bar plots
    "fsbar": (8, 8),
    "fsbar_short": (8, 4),
    "fsbar_sub": (16, 8),
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
    facecolor=dark_blue,
    edgecolor=dark_blue,
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
