'''
The functions defined below are used for XXX
'''
import pandas as pd
from shapely.ops import linemerge
import momepy
import osmnx as ox

def clean_col_names(df):

    # TODO: Docs!
    # Test!

    '''
    Remove upper-case letters and : from OSM key names
    '''

    df.columns = df.columns.str.lower()

    df_cols = df.columns.to_list()

    new_cols = [c.replace(':','_') for c in df_cols]

    df.columns = new_cols

    return df


def create_osmnx_graph(gdf):

    # TODO: Docs!
    # TODO: Test!

    ''''
    Function for  converting a geodataframe with LineStrings to a NetworkX graph object (MultiDiGraph), which follows the data structure required by OSMnx.
    (I.e. Nodes indexed by osmid, nodes contain columns with x and y coordinates, edges is multiindexed by u, v, key).
    Converts MultiLineStrings to LineStrings - assumes that there are no gaps between the lines in the MultiLineString

    OBS! Current version does not fix issues with topology.

    Parameters
    ----------
    gdf: GeoDataFrame
        The data to be converted to a graph format
    directed: bool
        Whether the resulting graph should be directed or not. Directionality is based on the order of the coordinates.

    Returns
    -------
    graph: NetworkX MultiDiGraph object
        The original data in a NetworkX graph format.

    '''

    gdf['geometry'] = gdf['geometry'].apply( lambda x: linemerge(x) if x.geom_type == 'MultiLineString' else x)

    # If Multilines cannot be merged do to gaps, use explode
    geom_types = gdf.geom_type.to_list()
    #unique_geom_types = set(geom_types)

    if 'MultiLineString' in geom_types:
        gdf = gdf.explode(index_parts=False)

    G = momepy.gdf_to_nx(gdf, approach='primal', directed=True)

    nodes, edges = momepy.nx_to_gdf(G)

    # Create columns and index as required by OSMnx
    index_length = len(str(nodes['nodeID'].iloc[-1].item()))
    nodes['osmid'] = nodes['nodeID'].apply(lambda x: create_node_index(x, index_length, add_letter=False))

    # Create x y coordinate columns
    nodes['x'] = nodes.geometry.x
    nodes['y'] = nodes.geometry.y

    edges['u'] = nodes['osmid'].loc[edges.node_start].values
    edges['v'] = nodes['osmid'].loc[edges.node_end].values

    nodes.set_index('osmid', inplace=True)

    edges['length'] = edges.geometry.length # Length is required by some functions

    edges['key'] = 0

    edges = find_parallel_edges(edges)

    # Create multiindex in u v key format
    edges = edges.set_index(['u', 'v', 'key'])

    # For ox simplification to work, edge geometries must be dropped. Edge geometries is defined by their start and end node
    #edges.drop(['geometry'], axis=1, inplace=True) # Not required by new simplification function

    G_ox = ox.graph_from_gdfs(nodes, edges)

   
    return G_ox


##############################

def find_parallel_edges(edges):

    # TODO: Docs!

    '''
    Check for parallel edges in a pandas DataFrame with edges, including columns u with start node index and v with end node index.
    If two edges have the same u-v pair, the column 'key' is updated to ensure that the u-v-key combination can uniquely identify an edge.
    '''

    # Find edges with duplicate node pairs
    parallel = edges[edges.duplicated(subset=['u','v'])]

    edges.loc[parallel.index, 'key'] = 1 #Set keys to 1

    k = 1

    while len(edges[edges.duplicated(subset=['u','v','key'])]) > 0:

        k += 1

        parallel = edges[edges.duplicated(subset=['u','v','key'])]

        edges.loc[parallel.index, 'key'] = k #Set keys to 1

    assert len(edges[edges.duplicated(subset=['u','v','key'])]) == 0, 'Edges not uniquely indexed by u,v,key!'

    return edges

##############################

def create_node_index(x, index_length, add_letter='R'):

    # TODO: Docs!
    # TODO: Test

    '''
    Function for creating unique index column of specific length based on another shorter column.
    Possibility of adding additional letter for identifying ID (useful when creating 'false' OSM IDs)
    '''

    x = str(x)
    x  = x.zfill(index_length)
    
    assert len(x) == index_length

    if add_letter:
        x = x + 'R'

    return x

##############################

def explode_multilinestrings(gdf):

    # TODO: Docs!
    # TODO: Test

    individual_linestrings = gdf.explode(index_parts=True)

    new_ix_col = ['_'.join(map(str, i)) for i in zip(individual_linestrings.index.get_level_values(0), individual_linestrings.index.get_level_values(1))]
    individual_linestrings['index_split'] =  new_ix_col
    individual_linestrings.set_index('index_split', inplace=True)

    return individual_linestrings

##############################


def create_cycling_network(new_edges, original_nodes, original_graph, return_nodes=False):

    '''
    Create new OSMnx graph from a subset of edges of a larger OSMnx graph

    Arguments:
        new_edges (geodataframe): the edges defining the new graph
        original_nodes (geodataframe): the nodes from the larger graph
        original_graph (NetworkX graph object): the larger graph
        return_nodes (True/False): if True, return a tuple of the new graph and the nodes in the graph.

    Returns:
        new_graph: the new OSMnx graph object
        new_nodes (geodataframe): The nodes in the new graph
    '''

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




if __name__ == '__main__':

    pass