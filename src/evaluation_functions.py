import geopandas as gpd
import pandas as pd
import os.path
import osmnx as ox
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString


def check_settings_validity(study_area, study_area_poly_fp, study_crs, use_custom_filter, custom_filter, reference_comparison,
    reference_fp, reference_geometries, bidirectional, grid_cell_size):
    # Does not check for all potential errors, but givens an indication of whether settings have been filled out correctly

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


def fix_key_index(cycling_edges):

    # First get all edges with key equal to 1
    selection = cycling_edges.reset_index().loc[cycling_edges.reset_index().key==1]

    grouped = selection.groupby(['u','v'])

    for name, g in grouped:
        old_index = (name[0],name[1],1)
        
        try:
            test = cycling_edges.loc[(name[0],name[1],0)]
        except KeyError:
            #print('No edge with same nodes and key==0')
            g['key'].replace(1, value=0, inplace=True)
            g.set_index(['u','v','key'],inplace=True)

            cycling_edges.drop(old_index)
            cycling_edges = pd.concat([cycling_edges, g])

    return cycling_edges


def check_if_cols_exist(cols, df):
    for c in cols:
        if c in df.columns:
            df.drop(c, axis=1, inplace=True)

def create_grid_geometry(gdf, cell_size):

        geometry = gdf['geometry'].unary_union
        geometry_cut = ox.utils_geo._quadrat_cut_geometry(geometry, quadrat_width=cell_size)

        grid = gpd.GeoDataFrame(geometry=[geometry_cut], crs=gdf.crs)

        grid = grid.explode(index_parts=False, ignore_index=True)

        # Create arbitraty grid id col
        grid['grid_id'] = grid.index

        return grid


def get_graph_area(nodes, study_area_polygon, crs):

    poly = nodes.unary_union.convex_hull # Use convex hull for area computation
    poly_gdf = gpd.GeoDataFrame()
    poly_gdf.at[0,'geometry'] = poly
    poly_gdf = poly_gdf.set_crs(crs)

    area = poly_gdf.clip(study_area_polygon).area.values[0] # Clip in case convex hull goes beyond study area

    return area


def simplify_cycling_tags(osm_edges):
    # Does not take into account when there are differing types of cycling infrastructure in both sides

    # OBS! Some features might query as True for seemingly incompatible combinations
        
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

    edge_length = edge.length

    # TODO: Simplify - only need cycling infrastructure and bidirectional?

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


def create_cycling_network(new_edges, original_nodes, original_graph, return_nodes=False):

    # Create new OSMnx graph from a subset of edges of a larger graph

    #Getting a list of unique nodes used by bike_edges
    new_edges_index = pd.MultiIndex.to_frame(new_edges.index)
    u = new_edges_index['u'].to_list()
    v = new_edges_index['v'].to_list()

    used_nodes = list(set().union(u,v))

    #All nodes are copied to an new dataframe
    new_nodes = original_nodes.copy(deep=True)

    #Creating new column in bike_nodes with the index value
    new_nodes['osmid'] = new_nodes.index

    #Using list of nodes to mask out unnecessary nodes
    new_nodes = new_nodes[new_nodes['osmid'].isin(used_nodes)]

    #Drop column - not needed anymore 
    new_nodes.drop(columns='osmid', inplace=True)

    #Create graph from nodes and edge geodataframe
    new_graph = ox.graph_from_gdfs(new_nodes, new_edges, graph_attrs=original_graph.graph)

    if return_nodes:
        return new_graph, new_nodes
    
    else:
        return new_graph
 
def analyse_missing_tags(edges, dict):

    cols = edges.columns.to_list()

    results = {}

    for attribute, sub_dict in dict.items():

        results[attribute] = 0
        count_not_na = 0

        for geom_type, tags in sub_dict.items():

            tags = [t for t in tags if t in cols]

            if geom_type == 'true_geometries':

                subset = edges.loc[edges.cycling_geometries=='true_geometries']

            elif geom_type == 'centerline':

                subset = edges.loc[edges.cycling_geometries=='centerline']

            elif geom_type == 'all':

                subset = edges

            if len(tags) == 1:
                
                count_not_na = len(subset.loc[subset[tags[0]].notna()])

            elif len(tags) > 1:

                count_not_na = len(subset[subset[tags].notna().any(axis=1)])

            else:
                count_not_na = 0
             
            results[attribute] += count_not_na

    return results

def check_incompatible_tags(edges, incompatible_tags_dictionary, store_edge_ids=False):

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


def check_intersection(row, gdf):
    
    intersection = gdf[gdf.crosses(row.geometry)]

    if len(intersection) > 0 and (pd.isnull(row.bridge) == True or row.bridge=='no') and (pd.isnull(row.tunnel) == True or row.bridge=='no'):

        count = 0

        for _, r in intersection.iterrows():

            if (pd.isnull(r.bridge) == True or r.bridge =='no') and (pd.isnull(r.tunnel) == True or r.bridge =='no'):
                
                print('Found problem!')
    
                count += 1

        if count:
            if count > 0:
                return count
        

def find_network_gaps(network_nodes, network_edges, buffer_dist):

    nodes = network_nodes.copy(deep=True)

    edges = network_edges.copy(deep=True)

    if 'u' not in edges.columns:

        edges.reset_index(inplace=True)

    nodes['osmid'] = nodes.index

    buffered_nodes = nodes[['osmid','geometry']].copy(deep=True)

    buffered_nodes['geometry'] = buffered_nodes.geometry.buffer(buffer_dist)

    join = buffered_nodes.sjoin(nodes, how='left')

    group_idx = join.groupby('osmid_left')

    snapping_issues = []

    for _, group in group_idx:

        if len(group) > 1:
            # Remove matches with the node itself
            group = group.loc[group.osmid_left != group.osmid_right]

            if len(group) > 0:

                for _, row in group.iterrows():

                    issue = [row.osmid_left, row.osmid_right]
                    issue_reversed = [row.osmid_right, row.osmid_left]

                    # Check if an edge exist between the nodes
                    edge_exist = edges.loc[edges.u.isin(issue) & edges.v.isin(issue)]

                    if issue_reversed not in snapping_issues and len(edge_exist) < 1:
                        snapping_issues.append(issue)

    return snapping_issues


def compute_alpha_beta_gamma(edges, nodes):
    
    # Assuming non-planar graph

    e = len(edges)
    v = len(nodes)

    assert edges.geom_type.unique()[0] == 'LineString'
    assert nodes.geom_type.unique()[0] == 'Point'


    # Compute alpha # between 0 and 1
    alpha = (e-v+1)/(2*v-5)
    assert alpha >= 0 and alpha <= 1

    beta = e/v

    if beta > 3:
        print('Unusually high beta value!')

    gamma = e/(3*(v-2))
    assert gamma >= 0 and gamma <= 1

    return alpha, beta, gamma


def compute_edge_node_ratio(data_tuple):
    
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
    #Function for returning all connected components as list of individual graphs

    if nx.is_directed(graph) == True:
        
        G_un = ox.get_undirected(graph)

        graphs = [G_un.subgraph(c).copy() for c in nx.connected_components(G_un)]
        #print('{} graphs have been generated from the connected components'.format(len(graphs)))

    else:
      
        graphs = [graph.subgraph(c).copy() for c in nx.connected_components(graph)]
        #print('{} graphs have been generated from the connected components'.format(len(graphs)))

    return graphs

def component_lengths(components):

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

    edges = network_edges.copy(deep=True)
    nodes = network_nodes.copy(deep=True)

    if 'u' not in edges.columns:

        all_node_occurences = edges.reset_index().u.to_list() + edges.reset_index().v.to_list()

    else:

        all_node_occurences = edges.u.to_list() + edges.v.to_list()

    dead_ends = [x for x in all_node_occurences if all_node_occurences.count(x)==1]

    dangling_nodes = nodes[nodes.index.isin(dead_ends)]

    return dangling_nodes


def count_features_in_grid(joined_data, type):

    count_features_in_grid = {}
    grouped = joined_data.groupby('grid_id')

    for name, group in grouped:
        count_features_in_grid[name] = len(group)

    count_df = pd.DataFrame.from_dict(count_features_in_grid, orient='index')
    count_df.reset_index(inplace=True)
    count_df.rename(columns={'index':'grid_id', 0:f'count_{type}'}, inplace=True)

    return count_df


def length_of_features_in_grid(joined_data, type):

    features_in_grid_length = {}
    grouped = joined_data.groupby('grid_id')

    for name, group in grouped:
        features_in_grid_length[name] = group.geometry.length.sum()

    count_df = pd.DataFrame.from_dict(features_in_grid_length, orient='index')
    count_df.reset_index(inplace=True)
    count_df.rename(columns={'index':'grid_id', 0:f'length_{type}'}, inplace=True)

    return count_df


def compute_network_density(data_tuple, area, return_dangling_nodes = False):

    area = area / 1000000

    edges, nodes = data_tuple
   
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


def find_adjacent_components(components, buffer_dist, crs, return_edges=False):

    edge_list = []

    for i,c in enumerate(components):

        if len(c.edges) > 0:

            edges = ox.graph_to_gdfs(c, nodes=False)

            edges['component'] = i

            edge_list.append(edges)
            

    component_edges = pd.concat( edge_list)

    component_edges = component_edges.set_crs(crs)

    component_edges.reset_index(inplace=True, drop=True)
    component_edges['temp_edge_id'] = component_edges.index

    component_sjoin = gpd.sjoin(component_edges, component_edges)

    # These are actual intersections between unconnected components
    intersecting_components = component_sjoin.loc[component_sjoin.component_left != component_sjoin.component_right]

    intersections = []

    for _, row in intersecting_components.iterrows():
        intersections.append((row.temp_edge_id_left, row.temp_edge_id_right))

    # Now buffer component edges and find overlapping buffers
    component_edges_buffer = component_edges.copy()
    component_edges_buffer.geometry = component_edges_buffer.geometry.buffer(buffer_dist/2)

    component_buffer_sjoin = gpd.sjoin(component_edges_buffer, component_edges_buffer)
    intersecting_buffer_components = component_buffer_sjoin.loc[component_buffer_sjoin.component_left != component_buffer_sjoin.component_right].copy()

    # Drop intersecting buffers where edges also intersect (lack of intersection nodes are analysed elsewhere)
    indexes = []
    for i in intersections:
        ix = intersecting_buffer_components.loc[ (intersecting_buffer_components.temp_edge_id_left == i[0]) & (intersecting_buffer_components.temp_edge_id_right == i[1])].index.values[0]
        indexes.append(ix)

    indexes = set(indexes)

    intersecting_buffer_components.drop(indexes, inplace=True)

    ids = set(intersecting_buffer_components.temp_edge_id_left.to_list() + intersecting_buffer_components.temp_edge_id_right.to_list())

    issues = component_edges.loc[component_edges.temp_edge_id.isin(ids)]
    issues.reset_index(inplace=True)

    if return_edges:

        return issues, component_edges
    
    else:
        return issues

def assign_component_id(components, edges, edge_id_col):

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

    #joined_edges = edges.join(component_edges['component'], how='left')

    joined_edges = edges.merge(component_edges[['component',edge_id_col]], on=edge_id_col, how ='left')

    assert org_edge_len == len(joined_edges), 'Some edges have been dropped!'

    assert len(joined_edges.loc[joined_edges.component.isna()]) == 0, 'Not all edges have a component ID'

    return joined_edges, components_dict


def assign_component_id_to_grid(simplified_edges, edges_joined_to_grids, components, grid, prefix, edge_id_col):

    org_grid_len = len(grid)

    simplified_edges, _ = assign_component_id(components, simplified_edges, edge_id_col)

    edges_joined_to_grids = edges_joined_to_grids.merge(simplified_edges[['component','edge_id']],on='edge_id',how='right')

    grouped = edges_joined_to_grids.groupby('grid_id')

    grid_components = {}

    for g_id, data in grouped:
        comp_ids = list(set(data.component))

        grid_components[g_id] = comp_ids
        
    grid_comp_df = pd.DataFrame()
    grid_comp_df['component_ids'+'_'+prefix] = None

    for key, val in grid_components.items():
        grid_comp_df.at[key,'component_ids'+'_'+prefix] = val

    grid_comp_df.reset_index(inplace=True)
    grid_comp_df.rename(columns={'index':'grid_id'},inplace=True)

    grid = grid.merge(grid_comp_df, on='grid_id', how='left')

    assert len(grid) == org_grid_len

    return grid


# Function for doing grid analysis
def run_grid_analysis(grid_id, data, results_dict, func, *args, **kwargs):

    # This works for functions which returns a list, dict, value etc. - but not for functions that return a dataframe?
    # There will be some over counting due to edges being located in more than once cell

    # Get data based on grid id
    if type(data) == tuple:

        edges, nodes = data
        
        grid_edges = edges.loc[edges.grid_id == grid_id]
        grid_nodes = nodes.loc[nodes.grid_id == grid_id]

        if len(grid_edges) > 0 or len(grid_nodes) > 0:

            grid_data = (grid_edges, grid_nodes)

            # Run function 
            result = func(grid_data, *args, *kwargs)

            # Save to dictionary under grid id
            results_dict[grid_id] = result

            return result

        else:
            pass

    else:
        grid_data = data.loc[data.grid_id == grid_id]

        if len(grid_data) > 0:
    
            # Run function 
            result = func(grid_data, *args, *kwargs)

            # Save to dictionary under grid id
            results_dict[grid_id] = result

            return result

        else:
            pass


def count_component_cell_reach(components_df, grid, component_id_col_name):

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

    cell_count = sum([component_cell_count_dict.get(c) for c in component_lists])

    # Subtract one since this count also includes the cell itself
    cell_count = cell_count - 1

    return cell_count


def find_overshoots(dangling_nodes, edges, length_tolerance, return_overshoot_edges=True):

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


if __name__ == '__main__':

    import geopandas as gpd
    import pandas as pd
    import os.path
    import osmnx as ox
    import networkx as nx
    import numpy as np
    import matplotlib.pyplot as plt
    from shapely.geometry import LineString, Polygon, Point

    ###############################
    # Test for create_grid_geometry 
    ext = [(0,0),(0,10),(10,10),(10,0)]
    interior = [(4,4),(6,4),(6,6),(4,6)]
    poly = Polygon(ext, [interior])
    gdf = gpd.GeoDataFrame(geometry=[poly])
    grid = create_grid_geometry(gdf, 1)

    assert len(grid) == (10*10) - (2*2)
    assert len(grid.geom_type.unique()) == 1
    assert grid.geom_type.unique()[0] == 'Polygon'
    assert grid.loc[0,'geometry'].area == 1

    ###############################
    # Test get_dangling_nodes
    edges = gpd.read_file('../tests/edges.gpkg')
    nodes = gpd.read_file('../tests/nodes.gpkg')
    nodes.set_index('osmid',inplace=True)

    d_nodes = get_dangling_nodes(edges, nodes)
    assert len(d_nodes) == 9
    assert type(d_nodes) == gpd.geodataframe.GeoDataFrame

    ###############################
    # Test count features in grid
    ext = [(0,0),(0,10),(10,10),(10,0)]
    interior = [(4,4),(6,4),(6,6),(4,6)]
    poly = Polygon(ext, [interior])
    gdf = gpd.GeoDataFrame(geometry=[poly])
    grid = create_grid_geometry(gdf, 1)
    grid['grid_id'] = grid.index

    points = gpd.read_file('../tests/random_points.gpkg')
    points_joined = gpd.overlay(points, grid, how ='intersection')

    test_count = count_features_in_grid(points_joined, 'points')

    assert test_count.loc[0,'count_points'] == 2
    assert test_count.loc[18,'count_points'] == 2
    assert test_count.loc[28,'count_points'] == 1

    ###############################
    # Test length of features in grid
    ext = [(0,0),(0,10),(10,10),(10,0)]
    poly = Polygon(ext)
    gdf = gpd.GeoDataFrame(geometry=[poly])
    grid = create_grid_geometry(gdf, 1)
    grid['grid_id'] = grid.index

    # Test length_of_features_in_grid
    line_gdf = gpd.read_file('../tests/random_lines.gpkg',driver='GPKG')
    lines_joined = gpd.overlay(line_gdf, grid, how ='intersection', keep_geom_type=True)

    test_length = length_of_features_in_grid(lines_joined, 'lines')

    assert round(test_length.loc[0,'length_lines'],2) == 1.41
    assert round(test_length.loc[1,'length_lines'],2) == 2.83

    
    ###############################
    # Test check_intersection
    l1 = LineString([[1,1],[10,10]])
    l2 = LineString([[2,1],[6,10]])
    l3 = LineString([[10,10],[10,20]])
    l4 = LineString([[11,9],[5,20]])
    l5 = LineString([[1,12],[4,12]])

    lines = [l1, l2, l3,l4,l5]
    d = {'bridge':['yes','no', None,'no',None],'tunnel':['no','no',None,None,None], 'geometry':lines }
    edges = gpd.GeoDataFrame(d)

    edges['intersection_issues'] = edges.apply(lambda x: check_intersection(row = x, gdf=edges), axis=1)

    count_intersection_issues = len(edges.loc[(edges.intersection_issues.notna()) & edges.intersection_issues > 0])

    assert count_intersection_issues == 2
    assert edges.loc[2,'intersection_issues'] == 1
    assert edges.loc[3,'intersection_issues'] == 1

    ###############################
    # Test incompatible tags
    l1 = LineString([[1,1],[10,10]])
    l2 = LineString([[2,1],[6,10]])
    l3 = LineString([[10,10],[10,20]])
    l4 = LineString([[11,9],[5,20]])
    l5 = LineString([[1,12],[4,12]])

    lines = [l1, l2, l3,l4,l5]
    d = {'cycling':['yes','no', None,'yes',None],'car':['no','no',None,'yes',None], 'geometry':lines }
    edges = gpd.GeoDataFrame(d)

    dict = {'cycling': {'yes': [['bicycle', 'no'],
    ['bicycle', 'dismount'],
    ['car', 'yes']]}}

    incomp_tags_results = check_incompatible_tags(edges, dict)
    assert incomp_tags_results['cycling/car'] == 1

    ###############################
    # Test missing tags
    l1 = LineString([[1,1],[10,10]])
    l2 = LineString([[2,1],[6,10]])
    l3 = LineString([[10,10],[10,20]])
    l4 = LineString([[11,9],[5,20]])
    l5 = LineString([[1,12],[4,12]])

    lines = [l1, l2, l3,l4,l5]
    d = {'cycleway_width': [np.nan,2,2,1,np.nan],'width':[1,np.nan,2,1,0], 
        'surface':['paved', np.nan, np.nan, 'gravel',np.nan], 
        'cycling_geometries': ['true_geometries','true_geometries','centerline','centerline','centerline'],
        'geometry':lines }
    edges = gpd.GeoDataFrame(d)

    dict = {'surface': {'true_geometries': ['surface', 'cycleway_surface'],
    'centerline': ['cycleway_surface']},
    'width': {'true_geometries': ['width',
    'cycleway_width',
    'cycleway_left_width',
    'cycleway_right_width',
    'cycleway_both_width'],
    'centerline': ['cycleway_width',
    'cycleway_left_width',
    'cycleway_right_width',
    'cycleway_both_width']},
    'speedlimit': {'all': ['maxspeed']},
    'lit': {'all': ['lit']}}

    existing_tags_results = analyse_missing_tags(edges, dict)
    assert existing_tags_results['surface'] == 1
    assert existing_tags_results['width'] == 4

    ###############################
    # Test measure_infrastructure_length
    l1 = LineString([[1,1],[10,10]])
    l2 = LineString([[2,1],[6,10]])
    l3 = LineString([[10,10],[10,20]])
    l4 = LineString([[11,9],[5,20]])
    l5 = LineString([[1,12],[4,12]])

    lines = [l1, l2, l3,l4,l5]
    d = {'cycling_infrastructure': ['yes','yes','yes','yes','no'],
        'cycling_bidirectional': [True,False,False,True,False],
        'cycling_geometries': ['true_geometries','true_geometries','centerline','centerline','centerline'],
        'geometry':lines }
    edges = gpd.GeoDataFrame(d)
    edges['length'] = edges.geometry.length


    edges['infrastructure_length'] = edges.apply(lambda x: measure_infrastructure_length(edge = x.geometry, 
                                                        geometry_type=x.cycling_geometries, bidirectional=x.cycling_bidirectional, cycling_infrastructure=x.cycling_infrastructure), axis=1)


    assert edges.loc[0,'infrastructure_length'] == edges.loc[0,'length'] * 2
    assert edges.loc[1,'infrastructure_length'] == edges.loc[1,'length']
    assert edges.loc[2,'infrastructure_length'] == edges.loc[2,'length']
    assert edges.loc[3,'infrastructure_length'] == edges.loc[3,'length'] * 2
    assert pd.isnull(edges.loc[4,'infrastructure_length']) == True

    ###############################
    # Test define_protected_unprotected
    l1 = LineString([[1,1],[10,10]])
    l2 = LineString([[2,1],[6,10]])
    l3 = LineString([[10,10],[10,20]])
    l4 = LineString([[11,9],[5,20]])
    l5 = LineString([[1,12],[4,12]])

    lines = [l1, l2, l3,l4,l5]
    d = {'highway': ['cycleway','primary','secondary','path','track'],
        'cycleway': [np.nan,'track',np.nan,'lane','no'],
        'cycleway_both': [np.nan,np.nan,'shared_lane','track',np.nan],
        'bicycle_road': [0,0,0,0,'yes'],
        'cycleway_right': [np.nan,np.nan,np.nan,np.nan,np.nan],
        'cycleway_left': [np.nan,np.nan,np.nan,np.nan,np.nan],
        'geometry':lines }
    edges = gpd.GeoDataFrame(d)
    edges['length'] = edges.geometry.length


    queries = {'protected': ["highway == 'cycleway'",
    "cycleway in ['track','opposite_track']",
    "cycleway_left in ['track','opposite_track']",
    "cycleway_right in ['track','opposite_track']",
    "cycleway_both in ['track','opposite_track']"],
    'unprotected': ["cycleway in ['lane','opposite_lane','shared_lane','crossing']",
    "cycleway_left in ['lane','opposite_lane','shared_lane','crossing']",
    "cycleway_right in ['lane','opposite_lane','shared_lane','crossing']",
    "cycleway_both in ['lane','opposite_lane','shared_lane','crossing']",
    "bicycle_road == 'yes'"],
    'unknown': ["cycleway in ['designated']",
    "cycleway_left in ['designated']",
    "cycleway_right in ['designated']",
    "cycleway_both in ['designated']"]}

    edges = define_protected_unprotected(edges,queries)

    assert edges.loc[0, 'protected'] == 'protected'
    assert edges.loc[1, 'protected'] == 'protected'
    assert edges.loc[2, 'protected'] == 'unprotected'
    assert edges.loc[3, 'protected'] == 'mixed'
    assert edges.loc[4, 'protected'] == 'unprotected'

    ###############################
    # Test find_network_gaps
    G = nx.MultiDiGraph() # construct the graph
    G.add_node(1, x=10, y=10)
    G.add_node(2, x=20, y=20)
    G.add_node(3, x=25, y=30)
    G.add_node(4, x=25, y=40)
    G.add_node(5, x=24, y=40)

    # add length and osmid just for the osmnx function to work
    G.add_edge(1, 2, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(2, 3, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(3, 4, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(1, 5, 0, length=10, osmid=np.random.randint(1, 999999))

    G.graph['crs'] = 'epsg:25832'
    nodes, edges = ox.graph_to_gdfs(G)

    test_gaps = find_network_gaps(nodes, edges, 1)
    assert len(test_gaps) == 1
    assert test_gaps[0][0] == 4
    assert test_gaps[0][1] == 5

    ###############################
    # Test component_lengths
    G = nx.MultiDiGraph()
    # One component
    G.add_node(1, x=10, y=10)
    G.add_node(2, x=20, y=20)
    G.add_node(3, x=25, y=30)
    G.add_node(4, x=25, y=40)
    G.add_node(5, x=24, y=40)

    # add length and osmid just for the functions to work
    G.add_edge(1, 2, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(2, 3, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(3, 4, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(1, 5, 0, length=10, osmid=np.random.randint(1, 999999))

    # Second component
    G.add_node(6, x=50, y=50)
    G.add_node(7, x=47, y=47)
    G.add_node(8, x=53, y=50)
    G.add_node(9, x=45, y=60)
    G.add_node(10, x=44, y=60)

    # add length and osmid just for the functions to work
    G.add_edge(6, 7, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(7, 8, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(8, 9, 0, length=30, osmid=np.random.randint(1, 999999))
    G.add_edge(9, 10, 0, length=17, osmid=np.random.randint(1, 999999))

    G.graph['crs'] = 'epsg:25832'
    nodes, edges = ox.graph_to_gdfs(G)

    components = return_components(G)
    test_c_lengths = component_lengths(components)

    assert test_c_lengths.loc[0,'component_length'] == 40
    assert test_c_lengths.loc[1,'component_length'] == 67

    ###############################
    # Test find_adjacent_components
    G = nx.MultiDiGraph()
    # One component
    G.add_node(1, x=10, y=10)
    G.add_node(2, x=20, y=20)
    G.add_node(3, x=25, y=30)
    G.add_node(4, x=25, y=40)
    G.add_node(5, x=24, y=40)

    # add length and osmid just for the functions to work
    G.add_edge(1, 2, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(2, 3, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(3, 4, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(1, 5, 0, length=10, osmid=np.random.randint(1, 999999))

    # Second component
    G.add_node(6, x=50, y=50)
    G.add_node(7, x=47, y=47)
    G.add_node(8, x=53, y=50)
    G.add_node(9, x=45, y=60)
    G.add_node(10, x=44, y=60)

    G.add_edge(6, 7, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(7, 8, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(8, 9, 0, length=30, osmid=np.random.randint(1, 999999))
    G.add_edge(9, 10, 0, length=17, osmid=np.random.randint(1, 999999))

    # Third component
    G.add_node(11, x=53, y=55)
    G.add_node(12, x=70, y=70)
    G.add_node(13, x=80, y=85)
    G.add_node(14, x=75, y=85)

    G.add_edge(11, 12, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(12, 13, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(13, 14, 0, length=30, osmid=np.random.randint(1, 999999))

    G.graph['crs'] = 'EPSG:25832'
    nodes, edges = ox.graph_to_gdfs(G)

    components = return_components(G)
    adj_comps = find_adjacent_components(components,buffer_dist=5, crs='EPSG:25832')

    assert adj_comps.loc[0,'component'] == 1
    assert adj_comps.loc[1,'component'] == 2
    assert len(adj_comps) == 2
    assert adj_comps.loc[0,'from'] == 8 and adj_comps.loc[0,'to'] == 9
    assert adj_comps.loc[1,'from'] == 11 and adj_comps.loc[1,'to'] == 12

    ###############################
    # Test assign_component_id
    G = nx.MultiDiGraph()
    # One component
    G.add_node(1, x=10, y=10)
    G.add_node(2, x=20, y=20)
    G.add_node(3, x=25, y=30)
    G.add_node(4, x=25, y=40)
    G.add_node(5, x=24, y=40)

    # add length and osmid just for the functions to work
    G.add_edge(1, 2, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(2, 3, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(3, 4, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(1, 5, 0, length=10, osmid=np.random.randint(1, 999999))

    # Second component
    G.add_node(6, x=50, y=50)
    G.add_node(7, x=47, y=47)
    G.add_node(8, x=53, y=50)
    G.add_node(9, x=45, y=60)
    G.add_node(10, x=44, y=60)

    G.add_edge(6, 7, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(7, 8, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(8, 9, 0, length=30, osmid=np.random.randint(1, 999999))
    G.add_edge(9, 10, 0, length=17, osmid=np.random.randint(1, 999999))

    # Third component
    G.add_node(11, x=53, y=55)
    G.add_node(12, x=70, y=70)
    G.add_node(13, x=80, y=85)
    G.add_node(14, x=75, y=85)

    G.add_edge(11, 12, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(12, 13, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(13, 14, 0, length=30, osmid=np.random.randint(1, 999999))

    G.graph['crs'] = 'EPSG:25832'
    nodes, edges = ox.graph_to_gdfs(G)
    edges['edge_id'] = edges['osmid']

    components = return_components(G)
    edges_comp_ids, comp_dict = assign_component_id(components, edges, edge_id_col='osmid')

    assert len(edges_comp_ids) == 11
    assert len(comp_dict) == 3
    assert list(comp_dict.keys()) == [0,1,2]
    assert edges_comp_ids[0:4]['component'].unique()[0] == 0
    assert edges_comp_ids[4:8]['component'].unique()[0] == 1
    assert edges_comp_ids[8:10]['component'].unique()[0] ==2

    ###############################
    # Test assign_component_id_to_grid
    G = nx.MultiDiGraph()
    # One component
    G.add_node(1, x=10, y=10)
    G.add_node(2, x=20, y=20)
    G.add_node(3, x=25, y=30)
    G.add_node(4, x=25, y=40)
    G.add_node(5, x=24, y=40)

    # add length and osmid just for the functions to work
    G.add_edge(1, 2, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(2, 3, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(3, 4, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(1, 5, 0, length=10, osmid=np.random.randint(1, 999999))

    # Second component
    G.add_node(6, x=50, y=50)
    G.add_node(7, x=47, y=47)
    G.add_node(8, x=53, y=50)
    G.add_node(9, x=45, y=60)
    G.add_node(10, x=44, y=60)

    G.add_edge(6, 7, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(7, 8, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(8, 9, 0, length=30, osmid=np.random.randint(1, 999999))
    G.add_edge(9, 10, 0, length=17, osmid=np.random.randint(1, 999999))

    # Third component
    G.add_node(11, x=53, y=55)
    G.add_node(12, x=70, y=70)
    G.add_node(13, x=80, y=85)
    G.add_node(14, x=75, y=85)

    G.add_edge(11, 12, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(12, 13, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(13, 14, 0, length=30, osmid=np.random.randint(1, 999999))

    G.graph['crs'] = 'EPSG:25832'
    nodes, edges = ox.graph_to_gdfs(G)
    edges['edge_id'] = edges['osmid']

    components = return_components(G)
    edges_comp_ids, comp_dict = assign_component_id(components, edges, edge_id_col='osmid')

    # Create test grid and joined data
    grid = gpd.read_file('../tests/grid_component_test.gpkg',driver='GPKG')
    edges_joined = gpd.overlay(edges, grid, how ='intersection', keep_geom_type=True)

    test_id_to_grid = assign_component_id_to_grid(simplified_edges=edges, edges_joined_to_grids=edges_joined, components=components, grid=grid, prefix='osm', edge_id_col='osmid')

    assert len(test_id_to_grid) == len(grid)
    assert test_id_to_grid.loc[5,'component_ids_osm'][0] == 0
    assert test_id_to_grid.loc[7,'component_ids_osm'][0] == 0
    assert test_id_to_grid.loc[14,'component_ids_osm'][0] == 0
    assert test_id_to_grid.loc[26,'component_ids_osm'][0] == 1
    assert test_id_to_grid.loc[27,'component_ids_osm'][0] == 1
    assert test_id_to_grid.loc[28,'component_ids_osm'][0] == 1
    assert test_id_to_grid.loc[35,'component_ids_osm'][0] == 1
    assert test_id_to_grid.loc[35,'component_ids_osm'][1] == 2
    assert test_id_to_grid.loc[48,'component_ids_osm'][0] == 2
    assert test_id_to_grid.loc[49,'component_ids_osm'][0] == 2


    ###############################

    # Test count_component_cell_reach
    G = nx.MultiDiGraph()
    # One component
    G.add_node(1, x=10, y=10)
    G.add_node(2, x=20, y=20)
    G.add_node(3, x=25, y=30)
    G.add_node(4, x=25, y=40)
    G.add_node(5, x=24, y=40)

    # add length and osmid just for the functions to work
    G.add_edge(1, 2, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(2, 3, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(3, 4, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(1, 5, 0, length=10, osmid=np.random.randint(1, 999999))

    # Second component
    G.add_node(6, x=50, y=50)
    G.add_node(7, x=47, y=47)
    G.add_node(8, x=53, y=50)
    G.add_node(9, x=45, y=60)
    G.add_node(10, x=44, y=60)

    G.add_edge(6, 7, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(7, 8, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(8, 9, 0, length=30, osmid=np.random.randint(1, 999999))
    G.add_edge(9, 10, 0, length=17, osmid=np.random.randint(1, 999999))

    # Third component
    G.add_node(11, x=53, y=55)
    G.add_node(12, x=70, y=70)
    G.add_node(13, x=80, y=85)
    G.add_node(14, x=75, y=85)

    G.add_edge(11, 12, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(12, 13, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(13, 14, 0, length=30, osmid=np.random.randint(1, 999999))

    G.graph['crs'] = 'EPSG:25832'
    nodes, edges = ox.graph_to_gdfs(G)
    edges['edge_id'] = edges['osmid']

    components = return_components(G)

    components_df = component_lengths(components)

    # Create test grid and joined data
    grid = gpd.read_file('../tests/grid_component_test.gpkg',driver='GPKG')

    edges_joined = gpd.overlay(edges, grid, how ='intersection', keep_geom_type=True)
    grid = assign_component_id_to_grid(simplified_edges=edges, edges_joined_to_grids=edges_joined, components=components, grid=grid, prefix='osm', edge_id_col='osmid')

    test_comp_cell_reach = count_component_cell_reach(components_df, grid, 'component_ids_osm')

    assert len(test_comp_cell_reach) == len(components)
    assert list(test_comp_cell_reach.keys()) == components_df.index.to_list()
    assert test_comp_cell_reach[0] == 6
    assert test_comp_cell_reach[1] == 4
    assert test_comp_cell_reach[2] == 6

    ###############################
    # Test simplify cycling tags
    l1 = LineString([[1,1],[10,10]])
    l2 = LineString([[2,1],[6,10]])
    l3 = LineString([[10,10],[10,20]])
    l4 = LineString([[11,9],[5,20]])
    l5 = LineString([[1,12],[4,12]])

    lines = [l1, l2, l3,l4,l5]
    d = {'highway': ['cycleway','primary','secondary','path','track'],
        'cycling_infrastructure': ['yes','yes','yes','yes','yes'],
        'cycleway': [np.nan,'track',np.nan,np.nan,'no'],
        'cycleway_both': [np.nan,np.nan,'shared_lane','track',np.nan],
        'bicycle_road': [0,0,0,0,'yes'],
        'bicycle': [np.nan,np.nan,np.nan,'designated','designated'],
        'cycleway_right': [np.nan,np.nan,np.nan,np.nan,np.nan],
        'cycleway_left': [np.nan,np.nan,np.nan,np.nan,np.nan],
        'oneway': ['no','yes',np.nan,'yes',np.nan],
        'oneway_bicycle': [np.nan,'yes',np.nan, 'no',np.nan],
        'geometry':lines }
    edges = gpd.GeoDataFrame(d)
    edges['length'] = edges.geometry.length

    edges = simplify_cycling_tags(edges)

    assert edges.loc[0,'cycling_bidirectional'] == True and edges.loc[0,'cycling_geometries'] == 'true_geometries'
    assert edges.loc[1,'cycling_bidirectional'] == False and edges.loc[1,'cycling_geometries'] == 'centerline'
    assert edges.loc[2,'cycling_bidirectional'] == True and edges.loc[2,'cycling_geometries'] == 'centerline'
    assert edges.loc[3,'cycling_bidirectional'] == True and edges.loc[3,'cycling_geometries'] == 'true_geometries'
    assert edges.loc[4,'cycling_bidirectional'] == False and edges.loc[4,'cycling_geometries'] == 'true_geometries'


    ###############################
    # Test find_overshoots function
    G = nx.MultiDiGraph() # construct the graph
    G.add_node(1, x=10, y=10)
    G.add_node(2, x=20, y=20)
    G.add_node(3, x=25, y=30)
    G.add_node(4, x=25, y=28)
    G.add_node(5, x=20, y=15)

    # add length and osmid just for the osmnx function to work
    G.add_edge(1, 2, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(2, 3, 0, length=10, osmid=np.random.randint(1, 999999))
    G.add_edge(3, 4, 0, length=2, osmid=np.random.randint(1, 999999))
    G.add_edge(2, 5, 0, length=5, osmid=np.random.randint(1, 999999))

    G.graph['crs'] = 'epsg:25832'
    nodes, edges = ox.graph_to_gdfs(G)
    edges['length'] = edges.geometry.length
    dn_nodes = get_dangling_nodes(edges, nodes)

    overshoots_2 = find_overshoots(dn_nodes, edges, 2)
    overshoots_5 = find_overshoots(dn_nodes, edges, 5)

    assert len(overshoots_2) == 1
    assert len(overshoots_5) == 2
    assert overshoots_2['u'].values[0] == 3
    assert overshoots_2['v'].values[0] == 4
    assert overshoots_5['u'].values[0] == 2
    assert overshoots_5['v'].values[0] == 5
    assert overshoots_5['u'].values[1] == 3
    assert overshoots_5['v'].values[1] == 4

    # Test find_undershoots function
    G = nx.MultiDiGraph() # construct the graph
    G.add_node(1, x=1, y=1)
    G.add_node(2, x=1, y=20)
    G.add_node(3, x=1, y=30)
    G.add_node(4, x=10, y=20)
    G.add_node(5, x=20, y=20)
    G.add_node(6, x=12, y=18)
    G.add_node(7, x=12, y=1)
    G.add_node(8, x=5, y=18)
    G.add_node(9, x=5, y=1)
    G.add_node(10, x=20, y=22)


    # add length and osmid just for the osmnx function to work
    G.add_edge(1, 2, 0, length=10, osmid=12)
    G.add_edge(2, 3, 0, length=10, osmid=23)
    G.add_edge(2, 4, 0, length=5, osmid=24)
    G.add_edge(4, 5, 0, length=2, osmid=45)
    G.add_edge(4, 6, 0, length=2, osmid=46)
    G.add_edge(6, 7, 0, length=2, osmid=67)
    G.add_edge(8, 9, 0, length=2, osmid=89)
    G.add_edge(5, 10, 0, length=2, osmid=510)

    G.graph['crs'] = 'epsg:25832'

    nodes, edges = ox.graph_to_gdfs(G)
    edges['length'] = edges.geometry.length
    edges['edge_id'] = edges.osmid
    dangling_nodes = get_dangling_nodes(edges, nodes)

    undershoot_dict_3, undershoot_nodes_3 = find_undershoots(dangling_nodes, edges, 3, 'edge_id')

    undershoot_dict_5, undershoot_nodes_5 = find_undershoots(dangling_nodes, edges, 5, 'edge_id')

    assert len(undershoot_dict_3) == 1
    assert len(undershoot_dict_5) == 3
    assert list(undershoot_dict_3.keys()) == [8]
    assert list(undershoot_dict_3.values()) == [[24]]

    assert list(undershoot_dict_5.keys()) == [1,8,9]
    assert list(undershoot_dict_5.values()) == [[89], [12, 24, 23], [12]]