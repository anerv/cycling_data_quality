### FUNCTIONS FOR FOLIUM PLOTTING
import folium
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import cm, colors
import contextily as cx
from collections import Counter

exec(open("../settings/yaml_variables.py").read())
exec(open("../settings/plotting.py").read())
exec(open("../settings/tiledict.py").read())
exec(open("../settings/yaml_variables.py").read())


def make_foliumplot(feature_groups, layers_dict, center_gdf, center_crs):

    """
    Creates a folium plot from a list of already generated feature groups,
    centered around the centroid of the center_gdf.

    Parameters
    ----------
    feature_groups : list
        List of folium FeatureGroup objects to display on the map in desired order
    layers_dict : dict
        Dictionary of folium TileLayers to include in the map
    center_gdf : geopandas GeoDataFrame
        GeoDataFrame with shapely Point objects as geometries; its centroid will be used for map centering.
    center_crs: epsg crs
        Coordinate system of the center_gdf.
    Returns
    ----------
    folium map object
    """

    # FIND CENTER (RELATIVE TO NODES) AND CONVERT TO EPSG 4326 FOR FOLIUM PLOTTING
    centergdf = gpd.GeoDataFrame(geometry=center_gdf.dissolve().centroid)
    centergdf.set_crs(center_crs)
    centergdf = centergdf.to_crs("EPSG:4326")
    mycenter = (centergdf["geometry"][0].y, centergdf["geometry"][0].x)

    # CREATE MAP OBJECT
    m = folium.Map(location=mycenter, zoom_start=13, tiles=None)

    # ADD TILE LAYERS
    for key in layers_dict.keys():
        layers_dict[key].add_to(m)

    # ADD FEATURE GROUPS
    for fg in feature_groups:
        fg.add_to(m)

    # ADD LAYER CONTROL
    folium.LayerControl().add_to(m)

    return m


def make_edgefeaturegroup(gdf, myweight, mycolor, nametag, show_edges=True, myalpha=1):
    """
    Parameters
    ----------
    gdf : geopandas GeoDataFrame
        geodataframe containing the edges to be plotted as LineStrings in the geometry column.
    myweight : int
        numerical value - weight of plotted edges
    mycolor : str
        color of plotted edges (can be hex code)
    nametag : str
        feature group name to be displayed in the legend
    show_edges : bool
        for display of edges upon map generation, default is true
    Returns
    ----------
    folium FeatureGroup object
    """

    #### convert to espg 4326 for folium plotting
    gdf = gdf.to_crs("epsg:4326")

    locs = []  # initialize list to store coordinates

    for geom in gdf["geometry"]:  # for each of the linestrings,
        my_locs = [
            (c[1], c[0]) for c in geom.coords
        ]  # extract locations as list points
        locs.append(my_locs)  # add to list of coordinates for this feature group

    # make a polyline containing all edges
    my_line = folium.PolyLine(
        locations=locs, weight=myweight, color=mycolor, opacity=myalpha
    )

    # make a feature group
    fg_es = folium.FeatureGroup(name=nametag, show=show_edges)

    # add the polyline to the feature group
    my_line.add_to(fg_es)

    return fg_es


def make_nodefeaturegroup(gdf, mysize, mycolor, nametag, show_nodes=True):
    """
    Creates a feature group ready to be added to a folium map object from a geodataframe of points.

    Parameters
    ----------
    gdf : geopandas GeoDataFrame
        GeoDataFrame containing the nodes to be plotted as Points in the geometry column.
    myweight : int
        weight of plotted edges
    mycolor : str
        (can be hex code) - color of plotted edges
    nametag : str
        feature group name to be displayed in the legend
    show_edges : bool
        for display of edges upon map generation, default is true
    Returns
    ----------
    folium FeatureGroup object
    """

    #### convert to espg 4326 for folium plotting
    gdf = gdf.to_crs("epsg:4326")

    fg_no = folium.FeatureGroup(name=nametag, show=show_nodes)

    for geom in gdf["geometry"]:

        folium.Circle(
            location=(geom.y, geom.x),
            radius=mysize,
            color=mycolor,
            opacity=1,
            fill_color=mycolor,
            fill_opacity=1,
        ).add_to(fg_no)

    return fg_no


def make_markerfeaturegroup(gdf, nametag="Show markers", show_markers=False):
    """
    Parameters
    ----------
    gdf : geopandas GeoDataFrame
        geodataframe containing the geometries which map markers should be plotted on.
    nametag : str
        feature group name to be displayed in the legend
    show_edges : bool
        for display of markers upon map generation, default is false
    Returns
    ----------
    folium FeatureGroup object
    """

    #### convert to espg 4326 for folium plotting
    gdf = gdf.to_crs("epsg:4326")

    locs = []  # initialize list to store coordinates

    for geom in gdf["geometry"]:  # for each of the linestrings,
        my_locs = [
            (c[1], c[0]) for c in geom.coords
        ]  # extract locations as list points
        locs.append(my_locs[0])  # add to list of coordinates for this feature group

    # make a feature group
    fg_ms = folium.FeatureGroup(name=nametag, show=show_markers)

    for loc in locs:
        folium.Marker(loc).add_to(fg_ms)

    return fg_ms


def plot_grid_results(
    grid,
    plot_cols,
    plot_titles,
    filepaths,
    cmaps,
    alpha,
    cx_tile,
    no_data_cols,
    na_facecolor=pdict["nodata_face"],
    na_edgecolor=pdict["nodata_edge"],
    na_hatch=pdict["nodata_hatch"],
    na_alpha=pdict["alpha_nodata"],
    na_legend=nodata_patch,
    figsize=pdict["fsmap"],
    dpi=pdict["dpi"],
    crs=study_crs,
    legend=True,
    set_axis_off=True,
    legend_loc="upper left",
    use_norm=False,
    norm_min=None,
    norm_max=None,
):

    if use_norm is True:
        assert norm_min is not None, print("Please provide a value for norm_min")
        assert norm_max is not None, print("Please provide a value for norm_max")

    for i, c in enumerate(plot_cols):

        fig, ax = plt.subplots(1, figsize=figsize)

        if use_norm is True:

            cbnorm = colors.Normalize(vmin=norm_min[i], vmax=norm_max[i])

            grid.plot(
                ax=ax,
                column=c,
                legend=legend,
                alpha=alpha,
                norm=cbnorm,
                cmap=cmaps[i],
            )

        else:
            grid.plot(
                ax=ax,
                column=c,
                legend=legend,
                alpha=alpha,
                cmap=cmaps[i],
            )
        cx.add_basemap(ax=ax, crs=crs, source=cx_tile)
        ax.set_title(plot_titles[i])

        if set_axis_off:
            ax.set_axis_off()

        # add patches in grid cells with no data on edges
        if type(no_data_cols[i]) == tuple:

            grid[
                (grid[no_data_cols[i][0]].isnull())
                & (grid[no_data_cols[i][1]].isnull())
            ].plot(
                ax=ax,
                facecolor=na_facecolor,
                edgecolor=na_edgecolor,
                hatch=na_hatch,
                alpha=na_alpha,
            )

        else:
            grid[grid[no_data_cols[i]].isnull()].plot(
                ax=ax,
                facecolor=na_facecolor,
                edgecolor=na_edgecolor,
                hatch=na_hatch,
                alpha=na_alpha,
            )

        ax.legend(handles=[na_legend], loc=legend_loc)

        fig.savefig(filepaths[i], dpi=dpi)


def compute_folium_bounds(gdf):

    gdf_wgs84 = gdf.to_crs("EPSG:4326")

    gdf_wgs84["Lat"] = gdf_wgs84.geometry.y
    gdf_wgs84["Long"] = gdf_wgs84.geometry.x
    sw = gdf_wgs84[["Lat", "Long"]].min().values.tolist()
    ne = gdf_wgs84[["Lat", "Long"]].max().values.tolist()

    return [sw, ne]


def plot_saved_maps(filepaths, figsize=pdict["fsmap_sub"], alpha=None):

    assert len(filepaths) <= 2, print(
        "This function cam max plot two images at a time!"
    )

    fig = plt.figure(figsize=figsize)

    for i, f in enumerate(filepaths):

        img = plt.imread(f)
        ax = fig.add_subplot(1, 2, i + 1)

        if alpha is not None:

            plt.imshow(img, alpha=alpha[i])

        else:
            plt.imshow(img)

        ax.set_axis_off()


def compare_print_network_length(osm_length, ref_length):

    h = max([ref_length, osm_length])
    l = min([ref_length, osm_length])

    diff = h - l

    percent_diff = (osm_length - ref_length) / osm_length * 100

    # basel = diff / l * 100 # High is x percent higher than l
    baseh = diff / h * 100  # Low is x percent lower than h

    if ref_length > osm_length:
        hlab = "reference"
        llab = "OSM"
    elif osm_length > ref_length:
        hlab = "OSM"
        llab = "reference"

    print(f"Length of the OSM data set: {osm_length/1000:.2f} km")
    print(f"Length of the reference data set: {ref_length/1000:.2f} km")
    print("\n")
    print(f"The {hlab} data set is {diff/1000:.2f} km longer than the {llab} data set.")
    print(f"The {hlab} data set is {baseh:.2f}% longer than the {llab} data set.")


def print_node_sequence_diff(degree_sequence_before, degree_sequence_after, name):

    before = dict(Counter(degree_sequence_before))
    after = dict(Counter(degree_sequence_after))

    print(f"Before the network simplification the {name} graph had:")

    for k, v in before.items():
        print(f"- {v} node(s) with degree {k}")

    print("\n")

    print(f"After the network simplification the {name} graph had:")

    for k, v in after.items():
        print(f"- {v} node(s) with degree {k}")

    print("\n")


def print_network_densities(density_dictionary, data_label):

    edge_density = density_dictionary["network_density"]["edge_density_m_sqkm"]
    node_density = density_dictionary["network_density"]["node_density_count_sqkm"]
    dangling_node_density = density_dictionary["network_density"][
        "dangling_node_density_count_sqkm"
    ]

    print(f"In the {data_label} data, there are:")
    print(f" - {edge_density:.2f} meters of cycling infrastructure per square km.")
    print(f" - {node_density:.2f} nodes in the cycling network per square km.")
    print(
        f" - {dangling_node_density:.2f} dangling nodes in the cycling network per square km."
    )

    print("\n")


def make_bar_plot(
    data,
    bar_labels,
    y_label,
    x_positions,
    title,
    bar_colors,
    filepath,
    alpha=pdict["alpha_bar"],
    figsize=pdict["fsbar"],
    bar_width=pdict["bar_double"],
    dpi=pdict["dpi"],
):

    fig, ax = plt.subplots(1, 1, figsize=figsize)

    for i, d in enumerate(data):
        ax.bar(x_positions[i], d, width=bar_width, alpha=alpha, color=bar_colors[i])

    ax.set_title(title)
    ax.set_xticks(x_positions, bar_labels)
    ax.set_ylabel(y_label)

    fig.savefig(filepath, dpi=dpi)

    return fig


def make_bar_plot_side(
    x_axis,
    data_osm,
    data_ref,
    legend_labels,
    title,
    x_ticks,
    x_labels,
    y_label,
    filepath,
    bar_colors,
    width=pdict["bar_single"],
    alpha=pdict["alpha_bar"],
    figsize=pdict["fsbar"],
    dpi=pdict["dpi"],
):

    fig, ax = plt.subplots(1, 1, figsize=figsize)

    ax.bar(
        x=x_axis[0],
        height=data_osm,
        label=legend_labels[0],
        width=width,
        alpha=alpha,
        color=bar_colors[0],
    )
    ax.bar(
        x=x_axis[1],
        height=data_ref,
        label=legend_labels[1],
        width=width,
        alpha=alpha,
        color=bar_colors[1],
    )
    ax.set_xticks(x_ticks, x_labels)
    ax.set_title(title)
    ax.set_ylabel(y_label)
    ax.legend()

    fig.savefig(filepath, dpi=dpi)

    return fig


def make_bar_subplots(
    subplot_data,
    nrows,
    ncols,
    bar_labels,
    y_label,
    x_positions,
    title,
    bar_colors,
    filepath,
    alpha=pdict["alpha_bar"],
    figsize=pdict["fsbar_sub"],
    bar_width=pdict["bar_double"],
    dpi=pdict["dpi"],
):

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

    axes = axes.flatten()

    for i, data in enumerate(subplot_data):

        for z, d in enumerate(data):
            axes[i].bar(
                x_positions[z], d, width=bar_width, alpha=alpha, color=bar_colors[z]
            )

        axes[i].set_ylabel(y_label[i])

        axes[i].set_xticks(x_positions, bar_labels)

        axes[i].set_title(title[i])

    fig.savefig(filepath, dpi=dpi)

    return fig
