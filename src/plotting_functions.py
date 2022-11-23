### FUNCTIONS FOR FOLIUM PLOTTING
import folium
import geopandas as gpd
import matplotlib as mpl
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

    """
    Make multiple choropleth maps of e.g. grid with analysis results based on a list of geodataframe columns to be plotted

    Arguments:
        grid (gdf): geodataframe with polygons to be plotted
        plot_cols (list): list of column names (strings) to be plotted
        plot_titles (list): list of strings to be used as plot titles
        cmaps (list): list of color maps
        alpha(numeric): value between 0-1 for setting the transparency of the plots
        cx_tile(cx tileprovider): name of contextily tile to be used for base map
        no_data_cols(list): list of column names used for generating no data layer in each plot
        na_facecolor(string): name of color used for the no data layer fill
        na_edegcolor(string): name of color used for the no data layer outline
        na_hatch: hatch pattern used for no data layer
        na_alpha (numeric): value between 0-1 for setting the transparency of the plots
        na_legend(matplotlib Patch): patch to be used for the no data layer in the legend
        figsize(tuple): size of each plot
        dpi(numeric): resolution of saved plots
        crs (string): name of crs used for the grid (to set correct crs of basemap)
        legend (bool): True if a legend/colorbar should be plotted
        set_axis_off (bool): True if axis ticks and values should be omitted
        legend_loc (string): Position of map legend (see matplotlib doc for valid entries)
        use_norm (bool): True if colormap should be defined based on provided min and max values
        norm_min(numeric): min value to use for norming color map
        norm_max(numeric): max value to use for norming color map


    Returns:
        None
    """

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

    """
    Helper function for printing saved plots/maps/images (up to two maps plotted side by side)

    Arguments:
        filepaths(list): list of filepaths of images to be plotted
        figsize(tuple): figsize
        alpha(list): list of len(filepaths) with values between 0-1 for setting the image transparency

    Returns:
        None
    """

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

    """
    Helper function for printing the node degree counts before and after network simplification.

    Arguments:
        degree_sequence_before(list): sorted list with node degrees from non-simplified graph
        degree_sequence_after(dict): sorted list with node degrees from simplified graph

    Returns:
        None
    """

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

    """
    Helper function for printing the network densities

    Arguments:
        density_dictionary (dict): dictionary with results of computation of network densities
        data_label(string): name of dataset

    Returns:
        None
    """

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
    ylim = None
):

    """
    Make a bar plot using matplotlib.

    Arguments:
        data (list): list of values to be plotted
        bar_labels (list): list of labels for x-axis/bars
        y_label (string): label for the y-axis
        x_positions (list): list of positions on x-axis where ticks and labels should be placed
        title (string): title of plot
        bar_colors (list): list of colors to be used for bars. Must be same length as data.
        filepath (string): Filepath where plot will be saved
        alpha (numeric): value between 0-1 used to set bar transparency
        figsize (tuple): size of the plot
        bar_width (numeric): width of each bar
        dpi (numeric): resolution of the saved plot
        ylim (numeric): upper limit for y-axis

    Returns:
        fig (matplotlib figure): the plot figure
    """

    fig, ax = plt.subplots(1, 1, figsize=figsize)

    for i, d in enumerate(data):
        ax.bar(x_positions[i], d, width=bar_width, alpha=alpha, color=bar_colors[i])

    ax.set_title(title)
    ax.set_xticks(x_positions, bar_labels)
    ax.set_ylabel(y_label)
    if ylim is not None:
        ax.set_ylim([0,ylim])

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
    x_label,
    y_label,
    filepath,
    bar_colors,
    width=pdict["bar_single"],
    alpha=pdict["alpha_bar"],
    figsize=pdict["fsbar"],
    dpi=pdict["dpi"],
):

    """
    Make a bar subplot using matplotlib where two datasets with corresponding values are plotted side by side.

    Arguments:
        x_axis (list): list of positions on x-axis. Expected input is len(x_axis) == number of values to be plotted
        data_osm (list): values to be plotted
        data_ref (list): values to be plotted
        legend_labels (list): list of legend labels for the bars (one for each dataset)
        title (string): title of plot
        x_ticks (list): list of x-tick locations
        x_labels (list): list of tick labesl
        y_label (string): label for the y-axis
        filepath (string): Filepath where plot will be saved
        bar_colors (list): list of colors to be used for bars. Expects one color for each dataset.
        width (numeric): width of each bar
        alpha (numeric): value between 0-1 used to set bar transparency
        figsize (tuple): size of the plot
        dpi (numeric): resolution of the saved plot

    Returns:
        fig (matplotlib figure): the plot figure
    """

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
    ax.set_xlabel(x_label)
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

    """
    Make a bar plot with several subplots using matplotlib

    Arguments:
        subplot_data (list): nested list with values to be plotted
        nrows (int): number of rows in subplot
        ncols (int): number of cols in subplot
        bar_labels (): lables for x-axis
        y_label (string): label for the y-axis
        x_positions (list): list of positions on x-axis. Expected input is len(x_axis) == number of values to be plotted (len of nested list)
        title (string): title of plot
        bar_colors (list): list of colors to be used for bars. Expects a list with the same length as the longest nested list in subplot_data
        filepath (string): Filepath where plot will be saved
        alpha (numeric): value between 0-1 used to set bar transparency
        figsize (tuple): size of the plot
        bar_width (numeric): width of bars
        dpi (numeric): resolution of the saved plot

    Returns:
        fig (matplotlib figure): the plot figure
    """

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
