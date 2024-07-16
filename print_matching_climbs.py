# -*- coding: utf-8 -*-
"""
@author: jbrown888
6/6/24
#cwd = D:\\j_Documents\\cliimbing\\
# see selecting_climbs.py for options for selection and speeds

"""

import pandas as pd
import numpy as np
import datetime as dt
import os
import broomcupboard as bc
import itertools
import re
from importlib import reload

#%%
dirpath = os.path.join(os.getcwd(), 'real_data')

climbs_fpath = os.path.join(dirpath, 'climbs_data.csv')

climbs_df = pd.read_csv(climbs_fpath, header=0,\
                 index_col =0, dtype=None, engine=None, converters={'climb_id':int},\
                 skipinitialspace=True, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True,\
                 na_filter=True, parse_dates=None, comment='#')

dict_select = {
                # 'climb_style': ['bouldering'],
                'grade': ['V5-7'],
                'location': ['Rockover'],
                # 'door': ['moonboard'],
                'wall': ['overhang'],
                'hold': ['clown']
               }

info_dict = {k:v for k,v in dict_select.items() if k not in ['hold', 'wall', 'skill']}
info_keys = [*info_dict.keys()]

# for g in dict_select['grades']:
#     if re.match(bc.Vgrades_range_regex_pattern, g):
#         ranged_grades = bc.get_grades_in_range(g)

if 'grades' in dict_select:
    bc.append_equivalent_grades(dict_select['grade'])

# INITIAL SORT NOT INCLUDING HOLD, WALL, SKILL COLUMNS
if len(info_dict)==0:
    reduced_climbs_df = climbs_df
elif len(info_dict)==1:
    gg = climbs_df.groupby(info_keys)
    try:
        reduced_climbs_df = pd.concat([gg.get_group((x,)) for x in info_dict[info_keys[0]]], axis = 0)
    except KeyError:
        print("KeyError - No climbs matching specified criteria of "+', '.join([f'{key}:{value}' for key, value in info_dict.items()]))
    # separate case as itertools.product returns a tuple as eg ('f6b',), and group keys look like 'f6b' - won't evaluate as not in gg.groups.keys()
    # in future version of pandas, when grouping with length-1 list-like you will need to pass a length-1 tuple to get_group, ie '(name,)'
    # this seems a bit of an oversight...
else:
    gg = climbs_df.groupby(info_keys)
    try:
        reduced_climbs_df = pd.concat([gg.get_group(x) for x in itertools.product(*info_dict.values()) if x in gg.groups.keys()])
    except ValueError as e:
        if str(e) != 'No objects to concatenate':
            raise e
        else:
            print("No climbs matching specified criteria of "+', '.join([f'{key}:{value}' for key, value in info_dict.items()]))
#or
# if len(info_dict)==0:
#     reduced_climbs_df = climbs_df
# else:
#     reduced_climbs_df = climbs_df.loc[(climbs_df[list(info_dict)].isin(info_dict)).all(axis=1)]
# if len(reduced_climbs_df)==0:
#     print("No climbs matching specified criteria of "+', '.join([f'{key}:{value}' for key, value in info_dict.items()]))

# SECOND SORT INCLUDING HOLD, WALL, SKILL TESTING
style_keys = [k for k in ['hold', 'wall', 'skill'] if k in dict_select.keys()]
# faster than apply! just going to use this for now
cols = list(reduced_climbs_df.columns)
data, index = [], []
for row in reduced_climbs_df.itertuples(index=True):
    row_dict = {f:v for f,v in zip(cols, row[1:])}
    data.append((lambda row: 
    # Check if any item in dict_select[col] is not in row[col] for any column in style_keys
    not any(item not in row[col] for col in style_keys for item in dict_select[col])
)(row_dict))
    index.append(row[0])
boolmask = pd.Series(data, index=index)
if not boolmask.any():
    print("No climbs matching specified criteria of "+', '.join([f'{key}:{value}' for key, value in info_dict.items()]))
else:
    fully_reduced_df = reduced_climbs_df[boolmask]
    # columns_to_list = [x for x in climbs_df.columns if x not in dict_select.keys()]
    columns_to_list = ['grade','hold', 'wall', 'skill', 'climb_name','notes'] # for indoor bouldering
    print(fully_reduced_df[columns_to_list])



#%%
dirpath = os.path.join(os.getcwd(), 'real_data')

climbs_fpath = os.path.join(dirpath, 'climbs_data.csv')

climbs_df = pd.read_csv(climbs_fpath, header=0,\
                 index_col =0, dtype=None, engine=None, converters={'climb_id':int},\
                 skipinitialspace=True, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True,\
                 na_filter=True, parse_dates=None, comment='#')

dict_select = {
                'climb_style': ['bouldering'],
                'grade': ['V4-6'],
                # 'location': ['Rockover'],
                'door': ['indoor'],
                'wall': ['slab'],
                # 'hold': ['pebble']
               }
test = {'grade': 'V3-5', 'door': 'indoor', 'climb_style': 'bouldering', 'hold': ['crimp'], 'wall': ['slab']}
x = bc.get_filtered_climbs(climbs_df, test)