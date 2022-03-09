import momepy
import osmnx as ox
from shapely.ops import linemerge


def create_node_index(x, index_length):

    x = str(x)
    x  = x.zfill(index_length)
    x = x + 'R'

    return x

def find_parallel_edges(edges):

    '''
    Check for parallel edges in a pandas DataFrame with edges, including columns u with start node index and v with end node index.
    If two edges have the same u-v pair, the column 'key' is updated to ensure that the u-v-key combination can uniquely identify an edge.
    '''

    # Find edges with duplicate node pairs
    parallel = edges[edges.duplicated(subset=['u','v'])]

    edges.loc[parallel.index, 'key'] = 1 #Set keys to 1

    assert len(edges[edges.duplicated(subset=['u','v','key'])]) == 0, 'Edges not uniquely indexed by u,v,key!'

    return edges


def create_osmnx_graph(gdf, directed=True):

    ''''
    Function for  converting a geodataframe with LineStrings to a NetworkX graph object (MultiDiGraph), which follows the data structure required by OSMnx.
    (Nodes indexed by osmid, nodes contain columns with x and y coordinates, edges is multiindexed by u, v, key)
    Converts MultiLineStrings to LineStrings - assumes that there are no gaps between the lines in the MultiLineString

    OBS! Current version does not fix topology

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

    G = momepy.gdf_to_nx(gdf, approach='primal', directed=directed)

    nodes, edges = momepy.nx_to_gdf(G)

    # Create columns and index as required by OSMnx
    index_length = len(str(nodes['nodeID'].iloc[-1].item()))
    nodes['osmid'] = nodes['nodeID'].apply(lambda x: create_node_index(x, index_length))

    # Create x y coordinate columns
    nodes['x'] = nodes.geometry.x
    nodes['y'] = nodes.geometry.y

    edges['u'] = nodes['osmid'].loc[edges.node_start].values
    edges['v'] = nodes['osmid'].loc[edges.node_end].values

    nodes.set_index('osmid', inplace=True)

    edges['key'] = 0

    edges = find_parallel_edges(edges)

    # Create multiindex in u v key format
    edges = edges.set_index(['u', 'v', 'key'])

    # For ox simplification to work, edge geometries must be dropped. Edge geometries is defined by their start and end node
    edges.drop(['geometry'], axis=1, inplace=True)


    G_ox = ox.graph_from_gdfs(nodes, edges)

   
    return G_ox




if __name__ == "__main__":
    pass