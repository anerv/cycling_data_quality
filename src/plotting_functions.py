### FUNCTIONS FOR FOLIUM PLOTTING
import folium
import geopandas as gpd

def make_foliumplot(feature_groups, layers_dict, center_gdf, center_crs):

    '''
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
    '''

    # FIND CENTER (RELATIVE TO NODES) AND CONVERT TO EPSG 4326 FOR FOLIUM PLOTTING
    centergdf = gpd.GeoDataFrame(geometry = center_gdf.dissolve().centroid)
    centergdf.set_crs(center_crs)
    centergdf = centergdf.to_crs("EPSG:4326")
    mycenter = (centergdf["geometry"][0].y, centergdf["geometry"][0].x)

    # CREATE MAP OBJECT 
    m = folium.Map(
        location = mycenter, 
        zoom_start = 13, 
        tiles = None)
    
    # ADD TILE LAYERS
    for key in layers_dict.keys():
        layers_dict[key].add_to(m)
    
    # ADD FEATURE GROUPS
    for fg in feature_groups:
        fg.add_to(m)

    # ADD LAYER CONTROL
    folium.LayerControl().add_to(m)
    
    return m

def make_edgefeaturegroup(gdf, myweight, mycolor, nametag, show_edges = True, myalpha = 1):
    '''
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
    '''

    #### convert to espg 4326 for folium plotting
    gdf = gdf.to_crs("epsg:4326")

    locs = [] # initialize list to store coordinates
    
    for geom in gdf["geometry"]: # for each of the linestrings,
        my_locs = [(c[1], c[0]) for c in geom.coords] # extract locations as list points
        locs.append(my_locs) # add to list of coordinates for this feature group

    # make a polyline containing all edges
    my_line = folium.PolyLine(locations = locs, 
            weight = myweight, 
            color = mycolor,
            opacity = myalpha)

    # make a feature group
    fg_es = folium.FeatureGroup(name = nametag, show = show_edges)

    # add the polyline to the feature group
    my_line.add_to(fg_es)

    return fg_es

def make_nodefeaturegroup(gdf, mysize, mycolor, nametag, show_nodes = True):
    '''
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
    '''

    #### convert to espg 4326 for folium plotting
    gdf = gdf.to_crs("epsg:4326")

    fg_no = folium.FeatureGroup(name = nametag, show = show_nodes)

    for geom in gdf["geometry"]:

        folium.Circle(location = (geom.y, geom.x), 
                radius = mysize, 
                color = mycolor, 
                opacity = 1,
                fill_color = mycolor,
                fill_opacity = 1).add_to(fg_no)

    return fg_no