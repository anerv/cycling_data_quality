'''
The functions defined below are used for creating creating and modifying networkx graphs using the osmnx format for indexing edges and nodes
'''
import pandas as pd
from shapely.ops import linemerge
import momepy
import osmnx as ox

def clean_col_names(df):

    # TODO: Docs!

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
    # Test okay

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
    # TODO: Test

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

def create_node_index(x, index_length):

    # TODO: Docs!

    '''
    Function for creating unique index column of specific length based on another shorter column.
    '''

    x = str(x)
    x  = x.zfill(index_length)
    
    assert len(x) == index_length

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



