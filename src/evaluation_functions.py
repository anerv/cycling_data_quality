'''
This script contain all functions used for evaluating and describing network completeness and structure.
For functions used specifically for the feature matching, see matching_functions.py
'''

import geopandas as gpd
import pandas as pd
import os.path
import osmnx as ox
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def check_settings_validity(study_area, study_area_poly_fp, study_crs, use_custom_filter, custom_filter, reference_comparison,
    reference_fp, reference_geometries, bidirectional, grid_cell_size):

    """
    Checks for most common errors when filling out analysis settings.
    OBS: Does not check for all potential errors.
    Throws an error if a variable is not filled out or is of unexpected type

    Arguments:
        study_area (str): setting to check
        study_area_poly_fp (str): setting to check
        study_crs, use_custom_filter  (str): setting to check
        custom_filter (str): setting to check
        reference_comparison (str): setting to check
        reference_fp (str): setting to check
        reference_geometries (str): setting to check
        bidirectional  (str): setting to check
        grid_cell_size  (str): setting to check

    Returns:
        none
    """
    
    assert type(study_area) == str
    assert os.path.exists(study_area_poly_fp) == True
    assert type(study_crs) == str

    if use_custom_filter == True:
        assert custom_filter != None

    if reference_comparison == True:
        assert os.path.exists(reference_fp) == True

    assert type(reference_geometries) == str
    assert type(bidirectional) == str or bidirectional in (True, False)

    assert type(grid_cell_size) == int


def fix_key_index(org_edges):

    """
    For a GeoDataFrame with network edges indexed by (u,v,key), make sure that no edges has key == 1,
    without a corresponding key == 0 (with same u,v values).
    If there is no key==0 edge, the simplification function will throw an error.
    OBS: Does not check whether a key==1 exists, in case of parallel edges

    Arguments:
        cycling_edges (gdf): Dataframe to be checked for inconsistencies in key values.

    Returns:
        cycling_edges (gdf): Same dataframe with fixed key-values
    """

    edges = org_edges.copy(

    )
    # First get all edges with key equal to 1
    selection = edges.reset_index().loc[edges.reset_index().key==1]

    grouped = selection.groupby(['u','v'])

    for name, g in grouped:
        old_index = (name[0],name[1],1)
        
        try:
            edges.loc[(name[0],name[1],0)]
    
        except KeyError:
 
            g['key'].replace(1, value=0, inplace=True)
            g.set_index(['u','v','key'],inplace=True)

            edges.drop(old_index,inplace=True)
            edges = pd.concat([edges, g])

    return edges


def find_pct_diff(row, osm_col, ref_col):


    '''
    Small helper function for computing rounded pct difference between two values.

    Arguments:
        row (row in pandas df): Row with values to be compared
        osm_col, ref_col (str): Names of columns in rows to be compared

    Returns:
        cycling_edges (gdf): Same dataframe with fixed key-values
    '''

    if row.isnull().values.any() == True:
        
        pass

    else:
        pct_diff = round((row[osm_col] - row[ref_col]) / ((row[osm_col] + row[ref_col]) / 2) * 100,2)

        return pct_diff


def create_grid_geometry(gdf, cell_size):

    '''
    Creates a geodataframe with grid cells covering the area specificed by the input gdf

    Arguments:
        gdf (gdf): geodataframe with a polygon/polygons defining the study area
        cell_size (numeric): width of the grid cells in units used by gdf crs

    Returns:
        grid (gdf): gdf with grid cells in same crs as input data
    '''

    geometry = gdf['geometry'].unary_union
    geometry_cut = ox.utils_geo._quadrat_cut_geometry(geometry, quadrat_width=cell_size)

    grid = gpd.GeoDataFrame(geometry=[geometry_cut], crs=gdf.crs)

    grid = grid.explode(index_parts=False, ignore_index=True)

    # Create arbitraty grid id col
    grid['grid_id'] = grid.index

    return grid


def get_graph_area(nodes, study_area_polygon, crs):

    '''
    Compute the size of the area covered by a graph (based on the convex hull)

    Arguments:
        nodes (gdf): geodataframe with graph nodes
        study_area_polygon (gdf): polygon defining the study area
        crs (str): CRS in format recognised by geopandas

    Returns:
        area (numeric): area in unit determined by crs (should be projected)
    '''

    poly = nodes.unary_union.convex_hull # Use convex hull for area computation
    poly_gdf = gpd.GeoDataFrame()
    poly_gdf.at[0,'geometry'] = poly
    poly_gdf = poly_gdf.set_crs(crs)

    area = poly_gdf.clip(study_area_polygon).area.values[0] # Clip in case convex hull goes beyond study area

    return area


def simplify_cycling_tags(osm_edges):

    # TODO: Allow user to input own queries

    '''
    Function for creating two columns in gdf containing linestrings/network edges
    with cycling infrastructure from OSM, indicating whether the cycling infrastructure is
    bidirectional and whether it is mapped as true geometries or center lines.

    Does not take into account when there are differing types of cycling infrastructure in both sides
    OBS! Some features might query as True for seemingly incompatible combinations

    Arguments:
        osm_edges (gdf): geodataframe with linestrings with cycling infrastructure from OSM

    Returns:
        osm_edges (gdf): same gdf + two new columns
    '''
 
    osm_edges['cycling_bidirectional'] = None
    osm_edges['cycling_geometries'] = None

    # Assumed to be one way if not explicitly stated that it is not
    centerline_false_bidirectional_true = ["highway == 'cycleway' & (oneway=='no' or oneway_bicycle=='no')",
                                "highway == 'bicycle_road' & (oneway =='no' or oneway_bicycle =='no')",
                                "highway == 'track' & bicycle == 'designated' & (oneway=='no' or oneway_bicycle =='no')",
                                "highway == 'path' & bicycle == 'designated' & (oneway=='no' or oneway_bicycle =='no')"]

    centerline_false_bidirectional_false = ["highway == 'cycleway' & (oneway !='no' or oneway_bicycle != 'no')",
                                "highway == 'bicycle_road' & (oneway!='no' or oneway_bicycle !='no')",
                                "highway == 'track' & bicycle == 'designated' & (oneway !='no' or oneway_bicycle !='no')",
                                "highway == 'path' & bicycle == 'designated' & (oneway !='no' or oneway_bicycle !='no')"]

    # Only cycling infrastructure in one side, but it is explicitly tagged as not one-way
    # or cycling infrastructure 
    centerline_true_bidirectional_true = ["cycleway_left in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and (cycleway_right in ['no','none','separate'] or cycleway_right.isnull()) and oneway_bicycle =='no'",
                                "cycleway_right in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and (cycleway_left in ['no','none','separate'] or cycleway_left.isnull()) and oneway_bicycle =='no'",
                                "cycleway in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and (oneway_bicycle == 'no' or oneway_bicycle.isnull())",
                                "cycleway_both in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and (oneway_bicycle == 'no' or oneway_bicycle.isnull())",
                                "cycleway_left in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and cycleway_right in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway']",
                                "bicycle_road =='yes' and (oneway != 'yes' or oneway_bicycle !='yes')"]

    # Only cycling infrastructure in one side and not bidirectional (if oneway_bicycle isn't explicitly yes, we assume that this type of tagging is one way)
    centerline_true_bidirectional_false = ["cycleway_left in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and (cycleway_right in ['no','none','separate'] or cycleway_right.isnull()) and oneway_bicycle !='no'",
                                "cycleway_right in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and (cycleway_left in ['no','none','separate'] or cycleway_left.isnull() ) and oneway_bicycle != 'no'",
                                "cycleway in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and oneway_bicycle == 'yes'",
                                "cycleway_both in ['lane','track','opposite_lane','opposite_track','shared_lane','designated','crossing','share_busway','opposite'] and oneway_bicycle == 'yes'",
                                "bicycle_road =='yes' and (oneway == 'yes' or oneway_bicycle =='yes')"]

    # The order of the queries matter: To account for instances where highway=cycleway and cycleway=some value indicating cycling infrastructure, the queries classifying based on highway should be run lastest
    for c in centerline_true_bidirectional_true:
        ox_filtered = osm_edges.query(c)
        osm_edges.loc[ox_filtered.index, 'cycling_bidirectional'] = True
        osm_edges.loc[ox_filtered.index, 'cycling_geometries'] = 'centerline'
    
    for c in centerline_true_bidirectional_false:
        ox_filtered = osm_edges.query(c, engine='python')
        osm_edges.loc[ox_filtered.index, 'cycling_bidirectional'] = False
        osm_edges.loc[ox_filtered.index, 'cycling_geometries'] = 'centerline'

    for c in centerline_false_bidirectional_false:
        ox_filtered = osm_edges.query(c)
        osm_edges.loc[ox_filtered.index, 'cycling_bidirectional'] = False
        osm_edges.loc[ox_filtered.index, 'cycling_geometries'] = 'true_geometries'

    for c in centerline_false_bidirectional_true:
        ox_filtered = osm_edges.query(c)
        osm_edges.loc[ox_filtered.index, 'cycling_bidirectional'] = True
        osm_edges.loc[ox_filtered.index, 'cycling_geometries'] = 'true_geometries'


    # Assert that cycling bidirectional and cycling geometries have been filled out for all where cycling infrastructure is yes!
    assert len(osm_edges.query("cycling_infrastructure =='yes' & (cycling_bidirectional.isnull() or cycling_geometries.isnull())")) == 0, 'Not all cycling infrastructure has been classified!'

    print('Bidirectional Value Counts: \n', osm_edges.cycling_bidirectional.value_counts())
    print('Geometry Type Value Counts: \n', osm_edges.cycling_geometries.value_counts())

    return osm_edges


def define_protected_unprotected(cycling_edges, classifying_dictionary):

    '''
    Function for classifying rows in gdf containing linestrings/network edges
    with cycling infrastructure from OSM as either protected or unprotected.
    Input dictionary with queries used in classification should have keys corresponding to types of protection level.
    Each key should contain a list of queries

    Arguments:
        cycling_edges (gdf): geodataframe with linestrings with cycling infrastructure from OSM
        classifying_dictionary (gdf): dictionary with queries used in classification.

    Returns:
        cycling_edges (gdf): same gdf +  new column 'protected'
    '''

    cycling_edges['protected'] = None
    
    for type, queries in classifying_dictionary.items():

        # Check if there already is a value for protected
        not_classified = cycling_edges[cycling_edges.protected.isna()]
        already_classified = cycling_edges[cycling_edges.protected.notna()]

        for q in queries:
            
            filtered_not_classified = not_classified.query(q)
            filtered_already_classified = already_classified.query(q)

            cycling_edges.loc[filtered_not_classified.index, 'protected'] = type
            cycling_edges.loc[filtered_already_classified.index, 'protected'] = 'mixed'

    # Assert that cycling bidirectional and cycling geometries have been filled out for all where cycling infrastructure is yes!
    assert len( cycling_edges.query( "protected.isnull()") ) == 0, 'Not all cycling infrastructure has been classified!'

    print('Protected Value Counts: \n', cycling_edges.protected.value_counts())
            
    return cycling_edges


def measure_infrastructure_length(edge, geometry_type, bidirectional, cycling_infrastructure):

    '''
    Measure the infrastructure length of edges with cycling infrastructure.
    If an edge represents a bidirectional lane/path or infrasstructure on both sides on a street,
    the infrastructure is set to two times the geometric length.
    If onesided/oneway, infrastructure length == geometric length.
    ...

    Arguments:
        edge (LineString): geometry of infrastructure
        geometry_type (str): variable used to determine if two-way or not. 
                            Can be either a variable for whole dataset OR name of column with the variable
        bidirectional (str): variable used to determine if two-way or not.
                            Can be either a variable for whole dataset OR name of column with the variable
        cycling_infrastructure: variable used to define cycling infrastructure if datasets included non-cycling infrastructure edges.
                              Can be either a variable for whole dataset OR name of column with the variable

    Returns:
        infrastructure_length (numeric): length of infrastructure
    '''
    edge_length = edge.length

    if cycling_infrastructure == 'yes' and geometry_type == 'true_geometries' and bidirectional == True:
        infrastructure_length = edge_length * 2
      
    elif cycling_infrastructure == 'yes' and geometry_type == 'true_geometries' and bidirectional == False:
        infrastructure_length = edge_length
     
    elif cycling_infrastructure == 'yes' and geometry_type == 'centerline' and bidirectional == True:
        infrastructure_length = edge_length * 2
       
    elif cycling_infrastructure == 'yes' and geometry_type == 'centerline' and bidirectional == False:
        infrastructure_length = edge_length
        

    elif cycling_infrastructure == 'yes' and (geometry_type is None or bidirectional is None):
        print('Missing information when calculating true infrastructure length!')
        infrastructure_length = None
    
    else:
        infrastructure_length = None

    return infrastructure_length

 
def analyse_missing_tags(gdf, dict):

    '''
    Analyse the extent of missing tags in a gdf with data from OSM based on custom dictionary.
    Custom dictionary should be a nested dict with top keys indicating the general attribute to be analysed.
    Next layer in the dictionary should have the keys true_geometries, centerline or all.
    These keys should contain lists of specific OSM tags to be checked.
    For example, when looking at surface, the surface of a bikelane mapped as centerline can be found under the tag
    'cycleway_surface', while it for a bikelane mapped as true geometry can be found under the osm tag 'surface'.

    Note that all ':' in osm tags have been replaced with '_'
    Look at the projects README for further explanation/illustration of concepts.
    ...

    Arguments:
        edges (gdf): data to be checked for missing tags
        dict (dictionary): dictionary defining the tags to be checked.

    Returns:
        results (dictionary): dictionary with the number of features missing 
    '''
  
    cols = gdf.columns.to_list()

    results = {}

    for attribute, sub_dict in dict.items():

        results[attribute] = 0
        count_not_na = 0

        for geom_type, tags in sub_dict.items():

            tags = [t for t in tags if t in cols]

            if geom_type == 'true_geometries':

                subset = gdf.loc[gdf.cycling_geometries=='true_geometries']

            elif geom_type == 'centerline':

                subset = gdf.loc[gdf.cycling_geometries=='centerline']

            elif geom_type == 'all':

                subset = gdf

            if len(tags) == 1:
                
                count_not_na = len(subset.loc[subset[tags[0]].notna()])

            elif len(tags) > 1:

                count_not_na = len(subset[subset[tags].notna().any(axis=1)])

            else:
                count_not_na = 0
             
            results[attribute] += count_not_na

    return results


def check_incompatible_tags(edges, incompatible_tags_dictionary, store_edge_ids=False):


    '''
    Check incompatible tags in gdf with data from OSM.
    Input dictionary should be a nested dictionary, with the top level keys indicating columns to be analysed,
    and the sub-dicts keys indicating the column values to be analysed.
    Each sub-dict key should refer to a list or tupple with first a column to compare to and secondly a column value 
    that is incompatible with the value defined in the second layer key.

    Arguments:
        edges (gdf): gdf with data to be analysed
        incompatible_tags_dictionary (dict): dictionary with tag combinations to analyse
        store_edge_ids (True/False): setting for whether to return ids of edges w. incompatible tags

    Returns:
        results (dict): dictionary with the count of incompatible tags for each type
    '''

    cols = edges.columns.to_list()
    results = {}

    for tag, subdict in incompatible_tags_dictionary.items():

        for value, combinations in subdict.items():

            for  c in combinations:

                if c[0] in cols:
                    results[tag +'/'+c[0]] = 0
                    count = len( edges.loc[ ( edges[tag]==value) & (edges[c[0]]==c[1])])
                    results[tag +'/'+c[0]] += count
                    if count > 0 and store_edge_ids == True:
                        results[tag +'/'+c[0] + '_edge_ids'] = list(edges['edge_id'].loc[ ( edges[tag]==value) & (edges[c[0]]==c[1])])
    
    return results


def check_intersection(row, gdf, print_check=True):

    '''
    Detects topological errors in gdf with edges from OSM data.
    If two edges are intersecting (i.e. no node at intersection) and neither is tagged as a bridge or a tunnel,
    it is considered an error in the data.

    Arguments:
        row (row): row currently analysed
        gdf (gdf): gdf with other edges to check for intersections iwth
        print_check: setting for whether to print when a missing intersection node is detected

    Returns:
        count (int): number of intersection issues for each row
    '''

    intersection = gdf[gdf.crosses(row.geometry)]

    if len(intersection) > 0 and (pd.isnull(row.bridge) == True or row.bridge=='no') and (pd.isnull(row.tunnel) == True or row.bridge=='no'):

        count = 0

        for _, r in intersection.iterrows():

            if (pd.isnull(r.bridge) == True or r.bridge =='no') and (pd.isnull(r.tunnel) == True or r.bridge =='no'):
                
                if print_check:
                    print('Found problem!')
    
                count += 1

        if count:
            if count > 0:
                return count
        


def compute_alpha_beta_gamma(edges, nodes, planar=True):

    '''
    Computes alpha, beta and gamma for a network

    Arguments:
        edges (gdf): network edges
        nodes (gdf): network nodes
        planar: whether network is (approx.) planar or not

    Returns:
        alpha, beta, gamma (float): values for each metric

    '''
    
    e = len(edges)
    v = len(nodes)

    assert edges.geom_type.unique()[0] == 'LineString'
    assert nodes.geom_type.unique()[0] == 'Point'


    if planar:
        alpha = (e-v+1)/(2*v-5)

    else:
        alpha = (e-v)/((v*(v-1)/2) - (v-1))

    assert alpha >= 0 and alpha <= 1

    beta = e/v

    if beta > 3:
        print('Unusually high beta value!')

    if planar:
        gamma = e/(3*(v-2))

    else:
        gamma = e / ((v*(v-1))/2)

    assert gamma >= 0 and gamma <= 1

    return alpha, beta, gamma


def compute_edge_node_ratio(data_tuple):

    '''
    Computes the ratio between edges and nodes in a network.

    Arguments:
        data_tuple (tuple): tuple with edges and nodes
        
    Returns:
        ratio (float): the ratio between edges and nodes

    '''
    
    edges, nodes = data_tuple
    
    e = len(edges)
    v = len(nodes)

    if len(nodes) > 0 and len(edges) > 0:
        
        assert edges.geom_type.unique()[0] in ['LineString','MultiLineString']
        assert nodes.geom_type.unique()[0] == 'Point'

        # Compute alpha # between 0 and 1
        ratio = e / v
        
        return ratio



def return_components(graph):

    '''
    Return all connected components as list of individual graphs.
    If the graph is directed, an undirected version of the graph is used.

    Arguments:
        graph (gdf): networkx graph

    Returns:
        graphs (list): list with all connected components as networkx graphs

    '''

    if nx.is_directed(graph) == True:
        
        G_un = ox.get_undirected(graph)

        graphs = [graph.subgraph(c).copy() for c in nx.connected_components(G_un)]
        #print('{} graphs have been generated from the connected components'.format(len(graphs)))

    else:
      
        graphs = [graph.subgraph(c).copy() for c in nx.connected_components(graph)]
        #print('{} graphs have been generated from the connected components'.format(len(graphs)))

    return graphs



def component_lengths(components):

    '''
    Return the length of all components

    Arguments:
        components (list): list of networkx graphs

    Returns:
        components_df (df): dataframe with length of components and the component id
                            (component id = position in input list with components)

    '''

    components_length = {}

    for i, c in enumerate(components):

        c_length = 0

        for (_, _, l) in c.edges(data='length'):

            c_length += l
        
        components_length[i] = c_length

    components_df = pd.DataFrame.from_dict(components_length, orient='index')

    components_df.rename(columns={0:'component_length'}, inplace=True)

    return components_df



def plot_components(components):

    #Plot components with each their color
    fig, ax = plt.subplots(figsize=(20,20))

    for c in components:
        rgb = np.random.rand(3,)
        if len(c.edges) > 0:
            edges = ox.graph_to_gdfs(c, nodes=False)
    
            edges.plot(ax=ax, color=rgb)
            
    ax.set_title('Connected components')
    plt.show()

    return fig



def get_dangling_nodes(network_edges, network_nodes):

    '''
    Return all dangling (degree one) nodes in a network
    Assumes an undirected network - if two parallel nodes representing a two-way street end in the same
    node, it will not be considered dangling.

    Arguments:
        network edges (gdf): gdf with network edges indexed by their start and end nodes
        network nodes (gdf): gdf with network nodes

    Returns:
        dangling_nodes (gdf): geodataframe with all dangling nodes
    '''

    edges = network_edges.copy(deep=True)
    nodes = network_nodes.copy(deep=True)

    if 'u' not in edges.columns:

        all_node_occurences = edges.reset_index().u.to_list() + edges.reset_index().v.to_list()

    else:

        all_node_occurences = edges.u.to_list() + edges.v.to_list()

    dead_ends = [x for x in all_node_occurences if all_node_occurences.count(x)==1]

    dangling_nodes = nodes[nodes.index.isin(dead_ends)]

    return dangling_nodes



def count_features_in_grid(joined_data, label):

    '''
    Count the number of features in each grid cell based on a dataset already joined to the grid 
    (i.e. having a column with reference to intersecting grid cell ids)

    Arguments:
        joined_data (gdf): gdf with network edges indexed by their start and end nodes
        label (str): name of joined_data for naming column with feature count

    Returns:
        count_df (df): dataframe with the count of all features in each grid cell, indexed by grid cell id
    '''

    count_features_in_grid = {}
    grouped = joined_data.groupby('grid_id')

    for name, group in grouped:
        count_features_in_grid[name] = len(group)

    count_df = pd.DataFrame.from_dict(count_features_in_grid, orient='index')
    count_df.reset_index(inplace=True)
    count_df.rename(columns={'index':'grid_id', 0:f'count_{label}'}, inplace=True)

    return count_df



def length_of_features_in_grid(joined_data, label):

    '''
    Compute the length of all features of one dataset for each grid cell.
    Assumes that the data have already been joined to the grid (all rows must have a reference to the intersecting grid cell id)
    OBS! Returns geometric length, not infrastructure length

    Arguments:
        joined_data (gdf): gdf with network edges indexed by their start and end nodes
        label (str): name of joined_data for naming column with feature count

    Returns:
        len_df (df): dataframe with the length of all features in each grid cell, indexed by grid cell id
    '''

    features_in_grid_length = {}
    grouped = joined_data.groupby('grid_id')

    for name, group in grouped:
        features_in_grid_length[name] = group.geometry.length.sum()

    len_df = pd.DataFrame.from_dict(features_in_grid_length, orient='index')
    len_df.reset_index(inplace=True)
    len_df.rename(columns={'index':'grid_id', 0:f'length_{label}'}, inplace=True)

    return len_df



def compute_network_density(data_tuple, area, return_dangling_nodes = False):
    
    '''
    Compute the network density (edge density, node density and optionally, dangling ndoe density)
    Uses infrastructure length, not geometric length.
    Requires a column with infrastructure length in edges dataset.
    The function is written to be used to compute local network density on a grid cell level.

    Arguments:
        data_tuple (tuple): tuple with gdfs with network edges and nodes
        area (numeric): area of study area in square meters
        return_dangling_nodes (boolean): Set to True if the density of the dangling nodes should be returned

    Returns:
        edge_density, node_density (dangling_node_density) (numeric): network densities
    '''


    area = area / 1000000

    edges, nodes = data_tuple

    assert 'infrastructure_length' in edges.columns
   
    if len(edges) > 0:

        edge_density = edges.infrastructure_length.sum() / area
    
    else:
        edge_density = 0

    if len(nodes) > 0:
        
        node_density = len(nodes)/area

    else:
        node_density = 0

    if return_dangling_nodes and len(nodes) > 0:

        dangling_nodes = get_dangling_nodes(edges, nodes)

        dangling_node_density = len(dangling_nodes) / area

        return  edge_density, node_density, dangling_node_density

    else:
        return  edge_density, node_density



def find_adjacent_components(components, edge_id, buffer_dist, crs, return_edges=False):

    '''
    Find edges in different (unconnected) components that are within a specified distance from each other.
    
    Arguments:
        components (list): list with network components (networkx graphs)
        edge_id (str): name of column with unique edge id
        buffer_dist (numeric): max distance for which edges in different components are considered 'adjacent'
        crs (str): crs to use when computing distances between edges
        return_edges (boolean): Set to True if all edges incl. information about their component should be returned

    Returns:
        issues (gdf): edges which are within the buffer dist of another component
        component_edges (gdf): all edges in the components
    '''

    edge_list = []

    for i,c in enumerate(components):

        if len(c.edges) > 0:

            edges = ox.graph_to_gdfs(c, nodes=False)

            edges['component'] = i

            edge_list.append(edges)
            

    component_edges = pd.concat( edge_list)

    component_edges = component_edges.set_crs(crs)

    # Buffer component edges and find overlapping buffers
    component_edges_buffer = component_edges.copy()
    component_edges_buffer.geometry = component_edges_buffer.geometry.buffer(buffer_dist/2)

    component_buffer_sjoin = gpd.sjoin(component_edges_buffer, component_edges_buffer)
    # Drop matches between edges on the same component
    intersecting_buffer_components = component_buffer_sjoin.loc[component_buffer_sjoin.component_left != component_buffer_sjoin.component_right].copy()

    ids = set(intersecting_buffer_components[edge_id+'_left'].to_list() + intersecting_buffer_components[edge_id+'_right'].to_list())

    issues = component_edges.loc[component_edges[edge_id].isin(ids)]
    issues.reset_index(inplace=True)

    if return_edges:

        return issues, component_edges
    
    else:
        return issues



def assign_component_id(components, edges, edge_id_col):

    '''
    Assign a component id to all edges
    
    Arguments:
        components (list): list with network components (networkx graphs)
        edge_id_col (str): name of column with unique edge id
        edges (gdf): edges from network used to generate components
    
    Returns:
        edges (gdf): edges with a new column 'component' referencing the component the edge is part of
        components_dict (dict): dictionary with all components indexed by the component ids used in the edge component column
    '''

    components_dict = {}
    edge_list = []

    org_edge_len = len(edges)

    for i,c in enumerate(components):

        if len(c.edges) < 1:
            print('Empty component')

        elif len(c.edges) > 0:

            c_edges = ox.graph_to_gdfs(c, nodes=False)

            c_edges['component'] = i

            edge_list.append(c_edges)

            components_dict[i] = c

    component_edges = pd.concat(edge_list)

    joined_edges = edges.merge(component_edges[['component',edge_id_col]], on=edge_id_col, how ='left')

    assert org_edge_len == len(joined_edges), 'Some edges have been dropped!'

    assert len(joined_edges.loc[joined_edges.component.isna()]) == 0, 'Not all edges have a component ID'

    return joined_edges, components_dict



def assign_component_id_to_grid(edges, edges_joined_to_grids, components, grid, prefix, edge_id_col):

    '''
    Join component id to intersecting grid cells.

    Arguments:
        simplified_edges (gdf): network edges
        edges_joined_to_grid (gdf): network edges joined with grid (must have a column 'grid_id' identifying intersecting grid cell)
        components (list): list of network components (networkx graphs)
        grid (gdf): grid used for the local analysis
        prefix (str): label to identify the network type (e.g. 'OSM' or 'reference')
        edge_id_col (str): name of column with unique edge id
    
    Returns:
        grid (gdf): grid gdf with column ('component_ids_'+prefix) identifying components in each cell
    '''

    org_grid_len = len(grid)

    edges, _ = assign_component_id(components, edges, edge_id_col)

    edges_joined_to_grids = edges_joined_to_grids.merge(edges[['component','edge_id']],on='edge_id',how='right')

    grouped = edges_joined_to_grids.groupby('grid_id')

    grid_components = {}

    for g_id, data in grouped:
        comp_ids = list(set(data.component))

        grid_components[g_id] = comp_ids
        
    grid_comp_df = pd.DataFrame()
    grid_comp_df['component_ids_'+prefix] = None

    for key, val in grid_components.items():
        grid_comp_df.at[key,'component_ids_'+prefix] = val

    grid_comp_df.reset_index(inplace=True)
    grid_comp_df.rename(columns={'index':'grid_id'},inplace=True)

    grid = grid.merge(grid_comp_df, on='grid_id', how='left')

    assert len(grid) == org_grid_len

    return grid


def run_grid_analysis(grid_id, data, results_dict, func, *args, **kwargs):

    '''
    Run a function for each cell in a spatial grid.
    This works for functions which returns a list, dict, value etc. - but not for functions that return a dataframe, since the meta-function does not return anything
    There will be some over-counting comparen to non-grid analysis due to edges being clipped by the grid cell boundaries

    Arguments:
        grid_id (undefined): unique identifier for grid cell
        data (gdf/df/tuple): data to be used in the analysis. Each row must have a key referencing the intersecting grid cell's id.
        results_dict (dict): dictionary to store results in
        func (function): name of function to run
        *args (undefined): additional parameters
        **kwargs (undefined): additional parameters

    Returns:
        None
    '''


    if type(data) == tuple:

        edges, nodes = data
        
        grid_edges = edges.loc[edges.grid_id == grid_id]
        grid_nodes = nodes.loc[nodes.grid_id == grid_id]

        if len(grid_edges) > 0 or len(grid_nodes) > 0:

            grid_data = (grid_edges, grid_nodes)

            result = func(grid_data, *args, *kwargs)

            results_dict[grid_id] = result

            return result

        else:
            pass

    else:
        grid_data = data.loc[data.grid_id == grid_id]

        if len(grid_data) > 0:
    
            result = func(grid_data, *args, *kwargs)

            results_dict[grid_id] = result

            return result

        else:
            pass
 

def count_component_cell_reach(components_df, grid, component_id_col_name):

    '''
    Count the number of cells in a grid reached/intersected by each component.

    Arguments:
        components_df (df): dataframe returned by component_lengths function (df with length of components and the component id)
        component_id_col_name (str): name of column with component ids in components_df

    Returns:
        component_cell_count (df): dataframe with count of reachable cells for each component
    '''

    component_ids = components_df.index.to_list()

    component_cell_count = {}

    for c_id in component_ids:

        selector = [str(c_id)]

        col_name_str = component_id_col_name + '_str'
        grid[col_name_str] = grid[component_id_col_name].apply(lambda x: [str(i) for i in x] if type(x) == list else x)

        mask = grid[col_name_str].apply(lambda x: any(item for item in selector if item in x) if type(x) == list else False)

        selection = grid[mask]

        component_cell_count[c_id] = len(selection)

    grid.drop(col_name_str, axis=1, inplace=True)

    return component_cell_count


def count_cells_reached(component_lists, component_cell_count_dict):

    '''
    Count the number of cells in a grid reachable from each grid cell, based on the network components intersected by that grid cell.

    Arguments:
        component_lists (list): list with network components as networkx graphs
        component_cell_count_dict (dict): dictionary with the count of cells reached by each component

    Returns:
        cell_count (int): count of reachable cells
    '''

    cell_count = sum([component_cell_count_dict.get(c) for c in component_lists])

    # Subtract one since this count also includes the cell itself?
    # cell_count = cell_count - 1

    return cell_count


def find_overshoots(dangling_nodes, edges, length_tolerance, return_overshoot_edges=True):
    
    '''
    Find overshoots in a network based on specified tolerance.

    Arguments:
        dangling_nodes (gdf): gdf with dangling nodes in network
        edges (gdf): gdf with network edges
        length_tolerance (numeric): threshold for when an edge is considered an overshoot 
        return_undershoot_edges (boolean): Set to False if the edges identified as overshoots should not be returned.
                                            If it is set to False, the index of the edges will be returned instead.

    Returns:
        overshoot_edges (gdf): gdf with edges identified as overshoots
        overshoot_ix (list): list with index values of edges identified as overshoots
    ''' 

    # Get index of all dangling nodes
    dn_index = dangling_nodes.index.to_list()

    if 'u' not in edges.columns:
        
        u_list = edges.reset_index().u.to_list()
        v_list = edges.reset_index().v.to_list()

        edges['u'] = u_list
        edges['v'] = v_list

    # Get edges connected to a dangling node
    subset_edges = edges.loc[ edges.u.isin(dn_index) | edges.v.isin(dn_index)]

    # Select dangling node edges with a length below threshold (overshoot edges)
    overshoots = subset_edges.loc[subset_edges.length <= length_tolerance].copy()

    # If both u and v are in dangling nodes, remove from overshoots
    short_edges = overshoots.loc[ overshoots.u.isin(dn_index) & overshoots.v.isin(dn_index)]
    short_edges_ix = short_edges.index

    overshoots.drop(short_edges_ix, inplace=True)

    # Get index of overshoot edges
    overshoot_ix = overshoots.index.to_list()

    if return_overshoot_edges:

        return overshoots

    else:
        return overshoot_ix


def find_undershoots(dangling_nodes, edges, length_tolerance, edge_id_col, return_undershoot_nodes=True):

    '''
    Find undershoots in a network, based on specified tolerance.

    Arguments:
        dangling_nodes (gdf): gdf with dangling nodes in network
        edges (gdf): gdf with network edges
        length_tolerance (numeric): threshold for when a node is considered an undershoot 
        edge_id_col (str): name of column with unique edge id in edges gdf
        return_undershoot_nodes (boolean): Set to False if the nodes identified as undershoots should not be returned

    Returns:
        undershoots (dict): dictionary with nodes identified as undershoots.
        undershoot_nodes (gdf): node identified as undershoots. Dictionary key is osmid, values are edges that nodes (potentially) should be snapped to
    '''

    # For each node in dangling nodes, get all edges within specified distance
    dangling_nodes['osmid'] = dangling_nodes.index
    buffered_nodes = dangling_nodes[['osmid','geometry']].copy(deep=True)
    buffered_nodes['geometry'] = buffered_nodes.geometry.buffer(length_tolerance)

    if 'v' not in edges.columns:

        u_list = edges.reset_index().u.to_list()
        v_list = edges.reset_index().v.to_list()

        edges['u'] = u_list
        edges['v'] = v_list


    joined = buffered_nodes.sjoin(edges, how='left')

    grouped = joined.groupby('osmid_left')

    undershoots = {}

    for name, group in grouped:

        # Check if there are edges within the threshold distance that are not connected to the node
        if len(group.loc[(group.osmid_left != group.u) & (group.osmid_left != group.v)]) > 0:

            group.reset_index(inplace=True)

            # Get all edges connected to the node
            connected_edges = edges.loc[(edges.u == name) | (edges.v == name)]

            # Get their other node
            connected_edges_nodes = list(set(connected_edges.u.to_list() + connected_edges.v.to_list()))

            connected_edges_nodes.remove(name)

            # Get adjacent edges and remove them from potential undershoot issues
            adjacent_edges = group.loc[(group.u.isin(connected_edges_nodes)) | (group.v.isin(connected_edges_nodes))]
            group.drop(adjacent_edges.index, inplace=True)
            
            # Remove edges connected to the node
            group = group.loc[(group.osmid_left != group.u) & (group.osmid_left != group.v)]

            if len(group) > 0:
                unconnected_edge_ids = group[edge_id_col].to_list()

                undershoots[name] = unconnected_edge_ids

    if return_undershoot_nodes:
        return undershoots, dangling_nodes.loc[dangling_nodes.osmid.isin(undershoots.keys())]

    else:
        return undershoots



def get_component_edges(components, crs):

    '''
    Get all edges from one or more network components, including a reference to their component's id

    Arguments:
        components (list): list of components as networkx graphs
        crs (str): crs for the graph data

    Returns:
        edges (gdf): edges from all components with the column 'component_id' identifying the component they belonged to.
        (id is based on position in list of components)
    '''

    comp_ids = []
    edge_geometries = []

    for i, c in enumerate(components):

        if len(c.edges) > 0:

            attr = nx.get_edge_attributes(c,'geometry')

            geoms = list(attr.values())
            edge_geometries = edge_geometries + geoms

            ids = [i]*len(geoms)

            comp_ids = comp_ids + ids

    assert len(comp_ids) == len(edge_geometries)

    edges = gpd.GeoDataFrame(data={'component_id': comp_ids}, geometry=edge_geometries, crs=crs)

    return edges

 