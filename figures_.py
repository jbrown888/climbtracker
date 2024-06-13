# -*- coding: utf-8 -*-
"""
@author: jnb19
"""
import numpy as np
# import scipy as sp
import scipy.optimize as op
import scipy.interpolate as ip
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
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
    'labelsize': 22,
    'ec' :'r',
    'fc' :'r',
    'linewidth': 2,
    'ticksize': 20,
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
    ax.grid(visible=True, which='major', axis='both', c='grey', ls='-')
    # ax.grid(b=True, which='minor', axis='both', c='darkgrey', ls = '--', linewidth =2)
    ax.tick_params(axis ='both', which = 'major', direction ='in', labelsize = figparams['ticksize'])
    ax.tick_params(axis ='both', which = 'minor', direction ='in')
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