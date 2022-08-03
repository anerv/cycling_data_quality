import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def style_pct_value_completeness(v, osm_bigger='color:blue;',osm_smaller='color:green;'):

    '''
    Helper function for styling the dataframe with results for data completeness.

    Arguments:
        v (numeric: value in cell to be styled
        osm_bigger (str): color to use if v is above zero
        osm_smaller (str): color to use if v is smaller than zero

    Returns:
        osm_bigger (str): color
        osm_smaller (str): color
    '''

    if v > 0:
        return osm_bigger
    elif v < 0:
        return osm_smaller
    else:
        None


def style_pct_value(v, osm_better='color:blue;',osm_worse='color:green;'):

    '''
    Helper function for styling the dataframe with results for data topology.

    Arguments:
        v (numeric: value in cell to be styled
        osm_better (str): color to use if v is above zero
        osm_worse (str): color to use if v is smaller than zero

    Returns:
        osm_better (str): color
        osm_worse (str): color
    '''

    if v > 0:
        return osm_better
    elif v < 0:
        return osm_worse
    else:
        None


def style_pct_value_inversed(v, osm_better='color:blue;',osm_worse='color:green;'):

    '''
    Helper function for styling the dataframe with results for data topology.

    Arguments:
        v (numeric: value in cell to be styled
        osm_better (str): color to use if v is above zero
        osm_worse (str): color to use if v is smaller than zero

    Returns:
        osm_better (str): color
        osm_worse (str): color
    '''

    if v > 0:
        return osm_worse
    elif v < 0:
        return osm_better
    else:
        None


