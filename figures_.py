# -*- coding: utf-8 -*-
"""
@author: jbrown888
# background figure functions for optimising plot appearance
"""
import numpy as np
# import scipy as sp
import scipy.optimize as op
import scipy.interpolate as ip
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
from collections import defaultdict
# import matplotlib.ticker as ticker
# import os
import os.path as pa
import pandas as pd
import matplotlib.cm as cm
import datetime
import re
# import copy
from scipy.signal import savgol_filter
from math import isclose


###############################################################################
# Graphics
###############################################################################
#graphics objects
infile_figparams_spyder = {'offsetsize': 20,
    'labelsize': 28,
    'ec' :'r',
    'fc' :'r',
    'linewidth': 2,
    'ticksize': 22,
    }
infile_figparams_vscode = {'offsetsize': 20,
    'labelsize': 14,
    'ec' :'r',
    'fc' :'r',
    'linewidth': 2,
    'ticksize': 13,
    'visible': True,
    'tickvisible': True,
    }
marker_ok = {'linestyle' : 'None',
 'marker' : 'o',
 'mec': 'k',
 'mfc': 'None',
 'mew': 2,
 'ms': 8,
 }
marker_point = {'linestyle' : 'None',
 'marker' : '.',
 'mfc': 'k',
 'mew':0,
 'ms':16,
 }
marker_plus = {'linestyle' : 'None',
 'marker' : '+',
 'mec': 'k',
 'mfc': 'k',
 'mew':2,
 'ms':8,
 }
marker_rx ={'linestyle' : 'None',
 'marker' : 'x',
 'mec': 'r',
 'mfc': 'r',
 'mew':3,
 'ms':16,
}
marker_gd ={'linestyle' : 'None',
 'marker' : 'd',
 'mec': 'limegreen',
 'mfc': 'None',
 'mew':4.5,
 'ms':16,
}
red_line = {'linestyle' : '-',
 'marker' : 'None',
 'color' : 'r',
 'linewidth':4,
}
marker_ok_line = {'linestyle' : '-',
 'marker' : 'o',
 'mec': 'k',
 'mfc': 'None',
 'mew': 2,
 'ms': 8,
 'linewidth':2,
}

empty_handle = mpl.lines.Line2D([0], [0], linestyle = 'None', marker = 'None')

arrow_handle = (mpl.lines.Line2D([0], [0], linestyle = 'None', marker = 0, mew = 2, ms = 20), mpl.lines.Line2D([0], [0], linestyle = 'None', marker = 9, mew = 2, ms = 10))


def standard_axes_settings(ax, figparams = infile_figparams_vscode):
    """
    Set standard graph settings for appearance.

    Parameters:
    ----------
    ax : matplotlib.axes.Axes
        Axes for the graph you want to edit.
    figparams : dict, optional
        A dictionary containing values for sizes on the graph.
        Default is the global infile_figparams.

    Returns
    -------
    None.

    """
    ax.set_frame_on
    if figparams['visible']:
        ax.grid(visible=True, which='major', axis='both', c='grey', ls='-')
    else:
        ax.grid(visible=False, which='major', axis='both')
    # ax.grid(b=True, which='minor', axis='both', c='darkgrey', ls = '--', linewidth =2)
    if figparams['tickvisible']:
        ax.tick_params(axis ='both', which = 'major', direction ='in', labelsize = figparams['ticksize'])
        ax.tick_params(axis ='both', which = 'minor', direction ='in')
    else:
        ax.tick_params(axis ='both', which = 'major', direction ='in', length = 0, width = 0, labelsize = figparams['ticksize'])
        ax.tick_params(axis ='both', which = 'minor', direction ='in', length = 0, width = 0)
    ax.xaxis.label.set_size(figparams['labelsize'])
    ax.yaxis.label.set_size(figparams['labelsize'])
    ax.minorticks_on()
    ax.yaxis.get_offset_text().set_fontsize(figparams['offsetsize'])
    ax.xaxis.get_offset_text().set_fontsize(figparams['offsetsize'])
    ax.ticklabel_format(axis = 'x', style = 'sci', scilimits = (-3,3), useOffset = True)
    ax.ticklabel_format(axis = 'y', style = 'sci', scilimits = (-3,3), useOffset=True)

def figure_count():
    if plt.gcf().number !=1:
        figure_counter = plt.gcf().number+1
    else:
        figure_counter = 1
    return figure_counter


def bar_plot(ax, data, colors=None, total_width=0.8, single_width=1, legend=True):
    """Draws a bar plot with multiple bars per data point.
    source: https://stackoverflow.com/questions/14270391/how-to-plot-multiple-bars-grouped
    
    Parameters
    ----------
    ax : matplotlib.pyplot.axis
        The axis we want to draw our plot on.

    data: dictionary
        A dictionary containing the data we want to plot. Keys are the names of the
        data, the items is a list of the values.

        Example:
        ```
        data = {
            "x":[1,2,3],
            "y":[1,2,3],
            "z":[1,2,3],
        }
        ```
        If there is a `None` value in the list, the bar will be missing for the corresponding `x` and the remaining bars
        will be centered around the x tick.

    colors : array-like, optional
        A list of colors which are used for the bars. If None, the colors
        will be the standard matplotlib color cyle. (default: None)

    total_width : float, optional, default: 0.8
        The width of a bar group. 0.8 means that 80% of the x-axis is covered
        by bars and 20% will be spaces between the bars.

    single_width: float, optional, default: 1
        The relative width of a single bar within a group. 1 means the bars
        will touch eachother within a group, values less than 1 will make
        these bars thinner.

    legend: bool, optional, default: True
        If this is set to true, a legend will be added to the axis.
    """

    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Build a bars_per_x dictionary depending on the number of values that are not None
    bars_per_x = {}
    for _, values_list in data.items():
        for i, value in enumerate(values_list):
            if value is not None:
                if i not in bars_per_x:
                    bars_per_x[i] = 0
                bars_per_x[i] += 1

    # Instead of using i in calculating the offset, we now use the i_per_x[x]
    i_per_x = {}

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            if x not in i_per_x:
                i_per_x[x] = 0

            if y is not None:
                # The offset in x direction of that bar
                x_offset = (i_per_x[x] - bars_per_x[x] / 2) * bar_width + bar_width / 2
                bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])
                i_per_x[x] += 1

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys())

    return 0


def bar_plot2(ax, data, group_stretch=0.8, bar_stretch=0.95,
             legend=True, x_labels=True, label_fontsize=8,
             colors=None, barlabel_offset=1,
             bar_labeler=lambda k, i, s: str(round(s, 3))):
    """
    Draws a bar plot with multiple bars per data point.
    :param dict data: The data we want to plot, where keys are the names of each
      bar group, and items is a list of bar values for the corresponding group.
    :param float group_stretch: 1 means groups occupy the most (largest groups
      touch side to side if they have equal number of bars).
    :param float bar_stretch: If 1, bars within a group will touch side to side.
    :param bool x_labels: If true, x-axis will contain labels with the group
      names given at data, centered at the bar group.
    :param int label_fontsize: Font size for the label on top of each bar.
    :param float barlabel_offset: Distance, in y-values, between the top of the
      bar and its label.
    :param function bar_labeler: If not None, must be a functor with signature
      ``f(group_name, i, scalar)->str``, where each scalar is the entry found at
      data[group_name][i]. When given, returns a label to put on the top of each
      bar. Otherwise no labels on top of bars.
    """
    sorted_data = list(sorted(data.items(), key=lambda elt: elt[0]))
    sorted_k, sorted_v  = zip(*sorted_data)
    max_n_bars = max(len(v) for v in data.values())
    group_centers = np.cumsum([max_n_bars
                               for _ in sorted_data]) - (max_n_bars / 2)
    bar_offset = (1 - bar_stretch) / 2
    bars = defaultdict(list)
    #
    if colors is None:
        colors = {g_name: [f"C{i}" for _ in values]
                  for i, (g_name, values) in enumerate(data.items())}
    #
    for g_i, ((g_name, vals), g_center) in enumerate(zip(sorted_data,
                                                         group_centers)):
        n_bars = len(vals)
        group_radius = group_stretch * (n_bars - bar_stretch) * 0.5
        print("!!!!", vals, n_bars)
        group_beg = g_center - group_radius
        for val_i, val in enumerate(vals):
            bar = ax.bar(group_beg + (val_i + bar_offset) * group_stretch,
                         height=val, width=bar_stretch * group_stretch,
                         color=colors[g_name][val_i])[0]
            bars[g_name].append(bar)
            if  bar_labeler is not None:
                x_pos = bar.get_x() + (bar.get_width() / 2.0)
                y_pos = val + barlabel_offset
                barlbl = bar_labeler(g_name, val_i, val)
                ax.text(x_pos, y_pos, barlbl, ha="center", va="bottom",
                        fontsize=label_fontsize)
    if legend:
        ax.legend([bars[k][0] for k in sorted_k], sorted_k)
    #
    ax.set_xticks(group_centers)
    if x_labels:
        ax.set_xticklabels(sorted_k)
    else:
        ax.set_xticklabels()
    return bars, group_centers

