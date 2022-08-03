import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl



# TODO: Add docstrings!

def style_pct_value_completeness(v, osm_bigger='', osm_smaller=''):

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

    if v > 0:
        return osm_bigger
    elif v < 0:
        return osm_smaller
    else:
        None

def style_pct_value(v, osm_better='', osm_worse=''):

    if v > 0:
        return osm_better
    elif v < 0:
        return osm_worse
    else:
        None

def style_pct_value_inversed(v, osm_better='', osm_worse=''):
    if v > 0:
        return osm_worse
    elif v < 0:
        return osm_better
    else:
        None


