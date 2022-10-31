### FUNCTIONS FOR FOLIUM PLOTTING
import folium
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import cm, colors
import contextily as cx

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

            grid[(grid[no_data_cols[i][0]].isnull()) & (grid[no_data_cols[i][1]].isnull())].plot(
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
