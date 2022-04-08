import geopandas as gpd
import pandas as pd
import os.path
import osmnx as ox
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


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


def create_grid_geometry(gdf, cell_size):

        geometry = gdf['geometry'].unary_union
        geometry_cut = ox.utils_geo._quadrat_cut_geometry(geometry, quadrat_width=cell_size)

        grid = gpd.GeoDataFrame(geometry=[geometry_cut], crs=gdf.crs)

        grid = grid.explode(index_parts=False, ignore_index=True)

        return grid

def get_graph_area(nodes, study_area_polygon, crs):

    poly = nodes.unary_union.convex_hull # Use convex hull for area computation
    poly_gdf = gpd.GeoDataFrame()
    poly_gdf.at[0,'geometry'] = poly
    poly_gdf = poly_gdf.set_crs(crs)

    area = poly_gdf.clip(study_area_polygon).area.values[0] # Clip in case convex hull goes beyond study area

    return area


def simplify_cycling_tags(osm_edges):
    # Does not take into account when there are differing types of cycling infrastructure in both sides?
        
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

    # Only cycling infrastructure in one side, but it is explicitly tagged as not oneway
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

    
    for c in centerline_false_bidirectional_true:
        ox_filtered = osm_edges.query(c)
        osm_edges.loc[ox_filtered.index, 'cycling_bidirectional'] = True
        osm_edges.loc[ox_filtered.index, 'cycling_geometries'] = 'true_geometries'

    for c in centerline_false_bidirectional_false:
        ox_filtered = osm_edges.query(c)
        osm_edges.loc[ox_filtered.index, 'cycling_bidirectional'] = False
        osm_edges.loc[ox_filtered.index, 'cycling_geometries'] = 'true_geometries'


    # Assert that cycling bidirectional and cycling geometries have been filled out for all where cycling infrastructure is yes!
    assert len(osm_edges.query("cycling_infrastructure =='yes' & (cycling_bidirectional.isnull() or cycling_geometries.isnull())")) == 0, 'Not all cycling infrastructure has been classified!'

    print(osm_edges.cycling_bidirectional.value_counts())
    print(osm_edges.cycling_geometries.value_counts())

    return osm_edges


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

        for geom_type, tags in sub_dict.items():

            tags = [t for t in tags if t in cols]

            if geom_type == 'true_geometries':

                subset = edges.loc[edges.cycling_geometries=='true_geometries']

            elif geom_type == 'centerline':

                subset = edges.loc[edges.cycling_geometries=='centerline']

            elif geom_type == 'all':

                subset = edges

            if len(tags) == 1:

                count_na = len(subset.loc[subset[tags[0]].isna()])

            elif len(tags) > 1:

                count_na = len(subset[subset[tags].isnull().all(axis=1)])

            results[attribute] += count_na

    return results


def check_incompatible_tags(edges, incompatible_tags_dictionary):

    cols = edges.columns.to_list()
    results = {}

    for tag, subdict in incompatible_tags_dictionary.items():

        for value, combinations in subdict.items():

            for  c in combinations:

                if c[0] in cols:
                    results[tag +'/'+c[0]] = 0
                    count = len( edges.loc[ ( edges[tag]==value) & (edges[c[0]]==c[1])])
                    results[tag +'/'+c[0]] += count
    
    return results


def check_intersection(row, gdf):
    
    intersection = gdf[gdf.crosses(row.geometry)]

    if len(intersection) > 0 and pd.isnull(row.bridge) == True and pd.isnull(row.tunnel) == True:

        count = None

        for _, r in intersection.iterrows():

            if pd.isnull(r.bridge) == True and pd.isnull(r.tunnel) == True:
                
                print('Found problem!')
    
                count += 1

        if count:
            if count > 0:
                return count
            

def find_network_gaps(network_nodes, network_edges, buffer_dist):

    nodes = network_nodes.copy(deep=True)

    edges = network_edges.copy(deep=True)

    edges.reset_index(inplace=True)

    nodes['osmid'] = nodes.index

    buffered_nodes = nodes[['osmid','geometry']].copy(deep=True)

    buffered_nodes['geometry'] = buffered_nodes.geometry.buffer(buffer_dist)

    join = buffered_nodes.sjoin(nodes, how='left')

    group_idx = join.groupby('osmid_left')

    snapping_issues = []

    for _, group in group_idx:

        if len(group) > 1:
            group = group.loc[group.osmid_left != group.osmid_right]

        if len(group) > 1:

            for _, row in group.iterrows():

                issue = [row.osmid_left, row.osmid_right]
                issue_reversed = [row.osmid_right, row.osmid_left]

                # Check if an edge exist between the nodes
                edge_exist = edges.loc[edges.u.isin(issue) & edges.v.isin(issue)]

                if issue_reversed not in snapping_issues and len(edge_exist) < 1:
                    snapping_issues.append(issue)

    return snapping_issues


def compute_alpha_beta_gamma(nodes, edges):
    
    # Assuming non-planar graph

    e = len(edges)
    v = len(nodes)

    # Compute alpha # between 0 and 1
    alpha = (e-v+1)/(2*v-5)
    assert alpha >= 0 and alpha <= 1

    beta = e/v

    if beta > 3:
        print('Unusually high beta value!')

    gamma = e/(3*(v-2))
    assert gamma >= 0 and gamma <= 1

    return alpha, beta, gamma


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

    all_node_occurences = edges.reset_index().u.to_list() + edges.reset_index().v.to_list()

    dead_ends = [x for x in all_node_occurences if all_node_occurences.count(x)==1]

    dangling_nodes = nodes[nodes.index.isin(dead_ends)]

    return dangling_nodes


if __name__ == '__main__':
    
    from shapely.geometry  import LineString

    # Start on test for check for intersection
    l1 = LineString([[1,1],[10,10]])
    l2 = LineString([[2,1],[6,10]])
    l3 = LineString([[10,10],[10,20]])
    lines = [l1, l2, l3]
    d = {'bridge':['yes','no', None], 'geometry':lines }
    gdf = gpd.GeoDataFrame(d)