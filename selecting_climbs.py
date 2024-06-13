# -*- coding: utf-8 -*-
"""
@author: jbrown888
10/6/24
#cwd = D:\\j_Documents\\cliimbing\\
# working on selecting groups of climbs based on multiple criteria
# for all possibilities
"""



import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
# import figures_ as ff
import itertools
from importlib import reload
import re
import add_new_climb_functions
import copy 

dirpath = os.path.join(os.getcwd(), 'sample_data')
fname = 'sample_climbs.csv'
fpath = os.path.join(dirpath, fname)
agg_data_fpath = os.path.join(dirpath, 'aggregate_df.csv')

climbs_df = pd.read_csv(fpath, header=0,\
                 index_col=0, dtype=None, engine=None, converters=None,\
                 skipinitialspace=True, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True,\
                 na_filter=True, parse_dates=None, escapechar = '\\', comment='#')

agg_df = pd.read_csv(agg_data_fpath, header=0, index_col=0, dtype=None, engine=None,
                              converters=None, skipinitialspace=True, skiprows=None, skipfooter=0,
                              nrows=None, na_values=None, keep_default_na=True, na_filter=True,
                              parse_dates=['first_attempt_date', 'latest_attempt_date', 'first_send_date'],
                              date_format='%Y-%m-%d', dayfirst=False, comment='#')

#%% 
# basic selection

dict_select = {
                'climb_style': ['bouldering'],
                'grade': ['V3-5'],
                # 'location': ['Rockover', 'Summit Up', 'Crag 1'],
                'door': ['indoor'],
               }
# my method
group = climbs_df.loc[(climbs_df[list(dict_select)].isin(dict_select)).all(axis=1)]
indices = group.index
if len(indices) == 0:
    print("No climbs matching specified criteria of "+', '.join([f'{key}:{value}' for key, value in dict_select.items()]))
# TIME IT: 4.19ms for 4 permutations, 4.41ms for 26 permutations

# groupby method 1
gg = climbs_df.groupby([*dict_select.keys()])
# there aren't necessarily climbs for all combinations of categories, want to iterate over dict_select.values
try:
    df_group = pd.concat([gg.get_group(x) for x in itertools.product(*dict_select.values()) if x in gg.groups.keys()], axis = 0)
    indices = df_group.index
except ValueError as e:
    if str(e) != 'No objects to concatenate':
        raise e
    else: 
        indices = []
        print("No climbs matching specified criteria of "+', '.join([f'{key}:{value}' for key, value in dict_select.items()]))
# TIME IT 4.79ms for 4 permutations, 12.1ms for 26 permutations

# OR 2
indices_arr = [gg.get_group(x).index for x in itertools.product(*dict_select.values()) if x in gg.groups.keys()]
indices = list(itertools.chain.from_iterable(indices_arr))
if len(indices) == 0:
    print("No climbs matching specified criteria of "+', '.join([f'{key}:{value}' for key, value in dict_select.items()]))

# TIME IT 5.72ms for 4 permutations, 7.41ms for 26 permutations

# careful - these 3 methods don't return same dtype. first two return pd.core.indexes.base.Index w/ int64
# third returns list of int.
# if no matching climbs, first returns empty pd.core.indexes.base.Index object, second and third return empty list

group_agg_data = agg_df.loc[indices]

#%% 
# grade selection equivalent font and V grades (not including ranges)
dict_select = {
                'grade': ['V7','f6c'],
               }

Vgrades_regex_pattern = r'^V([0-9]|[1-9][0-9]|B)[+]?$'

# can't compare values with regex. have to check afterwards
font_grades_regex_pattern = r'^f([0-9]|[1-9][0-9])[a-c]?[+]?$'

grades = copy.deepcopy(dict_select['grade'])
for g in grades:
    if re.match(Vgrades_regex_pattern, g):
        font_equivs = add_new_climb_functions.V_to_font[g]
        dict_select['grade']+= font_equivs
    elif re.match(font_grades_regex_pattern, g):
        V_equivs = add_new_climb_functions.font_to_V[g]
        dict_select['grade']+= V_equivs

#%% 
# grade selection ranges : get all grades included in range
Vgrades_range_regex_pattern = r'^V([0-9]|[1-9][0-9]|B)[+]?-((?!\1)[0-9]|[1-9][0-9])[+]?$' 
dict_select = {
                'grade': ['V3-5'],
               }

grades = copy.deepcopy(dict_select['grade'])
for g in grades:
    if re.match(Vgrades_range_regex_pattern, g):
        lower_grade = g.split('-')[0][1:]
        upper_grade = g.split('-')[1]
        if lower_grade == 'B':
            # assume unlikely input of VB-8+, so can treat as separate cases
            incl_grades = ['B'] + list(range(int(upper_grade)+1))
        elif upper_grade == '8+':
            incl_grades = list(range(int(lower_grade), 10)) # assume 8+ includes 8,9
        else:
            if int(lower_grade) >= int(upper_grade):
                raise ValueError(f'Lower grade {lower_grade} must be less than upper grade {upper_grade}')
            incl_grades = list(range(int(lower_grade), int(upper_grade)+1))
        dict_select['grade']+= [f'V{grade}' for grade in incl_grades]


#%%
# reverse range: include ranges of grades when specifying single grade ie V4 includes V2-4, V3-5 and V4-6

# 
g_single = 'VB'

# get list of all grades included in range
g = 'V5-6' # grade to test
lower_grade = g.split('-')[0][1:]
upper_grade = g.split('-')[1]
if lower_grade == 'B':
    # assume unlikely input of VB-8+, so can treat as separate cases
    incl_grades = ['B'] + list(range(int(upper_grade)+1))
elif upper_grade == '8+':
    incl_grades = list(range(int(lower_grade), 10)) # assume 8+ includes 8,9
else:
    if int(lower_grade) >= int(upper_grade):
        raise ValueError(f'Lower grade {lower_grade} must be less than upper grade {upper_grade}')
    incl_grades = list(range(int(lower_grade), int(upper_grade)+1))
all_grades = [f'V{grade}' for grade in incl_grades]

# check if specified single grade is included in range
check = g_single in all_grades
