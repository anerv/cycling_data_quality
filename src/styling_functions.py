import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def style_pct_value_completeness(v, osm_bigger='', osm_smaller=''):
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

def get_equal_interval_bins(min_value, max_value, num_levels):

    step_size = (abs(min_value) + max_value ) / num_levels

    if step_size > 100:
        step_size = round(step_size,-2)

    elif step_size < 100:
        step_size = round(step_size,-1)

    step_size = round(step_size,)

    if step_size > 0:

        if min_value < 0:

            bins = []

            bin_level = None

            for i in range(num_levels):

                if bin_level is None:
               
                    bin_level = min_value + step_size

                else: 
                    bin_level += step_size

                if bin_level > 100:
                    bin_level = round(bin_level,-2)

                else:
                    bin_level = round(bin_level,-1)

                bins.append(bin_level)
    
        else:
            bins = []

            for i in range(num_levels):
                bins.append((i+1)*step_size)

        return bins


def create_color_scale_around_midpoint(num_levels, vmin, vmax, colorscale='seismic', midpoint=0):

    #levels = np.linspace(vmin, vmax, num_levels)
    levels = get_equal_interval_bins(vmin, vmax, num_levels)

    midp = np.mean(np.c_[levels[:-1], levels[1:]], axis=1)
    vals = np.interp(midp, [vmin, midpoint, vmax], [0, 0.5, 1])
    colors = plt.cm.get_cmap(colorscale)(vals)
    cmap, norm = mpl.colors.from_levels_and_colors(levels, colors)

    return cmap, norm
