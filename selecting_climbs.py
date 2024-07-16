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
import broomcupboard as bc

dirpath = os.path.join(os.getcwd(), 'real_data')
fname = 'climbs_data.csv'
fpath = os.path.join(dirpath, fname)
agg_data_fpath = os.path.join(dirpath, 'aggregate_df.csv')

climbs_df = pd.read_csv(fpath, header=0,\
                 index_col=0, dtype=None, engine=None, converters=None,\
                 skipinitialspace=True, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True,\
                 na_filter=True, parse_dates=None, escapechar = '\\', comment='#')
fill_na_values = {'hold':'', 'wall':'', 'skill':''}
climbs_df = climbs_df.fillna(value = fill_na_values)


# agg_df = pd.read_csv(agg_data_fpath, header=0, index_col=0, dtype=None, engine=None,
#                               converters=None, skipinitialspace=True, skiprows=None, skipfooter=0,
#                               nrows=None, na_values=None, keep_default_na=True, na_filter=True,
#                               parse_dates=['first_attempt_date', 'latest_attempt_date', 'first_send_date'],
#                               date_format='%Y-%m-%d', dayfirst=False, comment='#')

#%% 
# basic selection

dict_select = {
                'climb_style': ['bouldering'],
                'grade': ['V3-5', 'V4-6'],
                'location': ['Rockover', 'Rockover Sharston'],
                # 'door': ['indoor'],
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

# group_agg_data = agg_df.loc[indices]

#THESE ARE FOR RETURNING INDICES!
#DON'T NEED TO DO THAT ANYMORE - QUICKER TO RETURN DATAFRAME

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

#%%

#%%

# dict_select = {'hold': ['volume'], 'skill': ['tension']}
dict_select = {'grade': ['V3-5'], 'door': ['indoor'], 'climb_style': ['bouldering'],'hold': ['jug', 'crimp'], 'wall': ['overhang']}#, 'hold': ['volume']}
# for hold, wall, and skill, we want to check if ANY of dict_select[key] are INCLUDED in the hold/wall/skill column for climb
# not if they match exactly. need to treat this as a separate case.

info_dict = {k:v for k,v in dict_select.items() if k not in ['hold', 'wall', 'skill']}
info_keys = [*info_dict.keys()]

# INITIAL SORT NOT INCLUDING HOLD, WALL, SKILL
#mymethod
if len(info_dict)==0:
    reduced_climbs_df = climbs_df
else:
    reduced_climbs_df = climbs_df.loc[(climbs_df[list(info_dict)].isin(info_dict)).all(axis=1)]
if len(reduced_climbs_df)==0:
    print("No climbs matching specified criteria of "+', '.join([f'{key}:{value}' for key, value in info_dict.items()]))

#groupby
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

# SECOND SORT INCLUDING HOLD, WALL, SKILL TESTING
# groupby is NOT going to work; we don't want to group into every possible combination of holds. 
# eg 'compression, sloper', 'compression, sloper, pinch' are separate groups! 
# we want to group by hold CONTAINING any of 'compression', 'sloper' etc

style_keys = [k for k in ['hold', 'wall', 'skill'] if k in dict_select.keys()]

# Filter climbs_df based on 'hold' column
filtered_df = climbs_df[climbs_df['hold'].map(lambda x: any(item in x for item in dict_select['hold']))] # works for just column
# Apply a lambda function to each row of the DataFrame, filter based on all keys in style_keys
filtered_df_full = climbs_df[climbs_df[style_keys].apply(
    lambda row: 
    # Check if all items in dict_select[col] are in row[col] for each column in style_keys
    all(item in row[col] for col in style_keys for item in dict_select[col]), 
    axis=1
)]
# equivalent to: 
indexs = []
for i in range(climbs_df[style_keys].shape[0]):
    iis = []
    for col in style_keys:
        iis.append(all(j in climbs_df[col].iloc[i] for j in dict_select[col]))
    if all(iis):
        indexs.append(i)
        
filtered_df_full2 = climbs_df[climbs_df[style_keys].apply(
    lambda row: 
    # Check if any item in dict_select[col] is not in row[col] for any column in style_keys
    not any(item not in row[col] for col in style_keys for item in dict_select[col]), 
    axis=1
)]
# more efficient!!
# OR add columns with true/false masks of hold, wall skill columns and then groupby these?

# faster than apply! just going to use this for now
cols = list(climbs_df.columns)
data, index = [], []
for row in climbs_df.itertuples(index=True):
    row_dict = {f:v for f,v in zip(cols, row[1:])}
    data.append((lambda row: 
    # Check if any item in dict_select[col] is not in row[col] for any column in style_keys
    not any(item not in row[col] for col in style_keys for item in dict_select[col])
)(row_dict))
    index.append(row[0])
x= pd.Series(data, index=index)
filtered_df_full3 = climbs_df[x]

#%%
testdict = {'climb_style': ['bouldering'], 'grade': ['V4-6'], 'door': ['indoor'], 'wall': ['slab']}
# testdict = {'climb_style': ['sport'], 'grade': ['V4-6'], 'door': ['moonboard'], 'wall': ['slab']}

climbs_df = pd.read_csv(fpath, header=0,\
            index_col =0, dtype=None, engine=None, converters={'climb_id':int},\
            skipinitialspace=True, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True,\
            na_filter=True, parse_dates=None, comment='#')
fill_na_values = {'hold':'', 'wall':'', 'skill':'', 'notes':'',}
climbs_df = climbs_df.fillna(value = fill_na_values)
filtered_climbs_df = bc.get_filtered_climbs(climbs_df, testdict)

dont_always_display_keys = ['climb_style', 'door', 'location', 'rope', 'climb_name', 'angle', 'mbyear', 'rock_type']
always_display_keys = ['climb_id', 'grade', 'hold', 'wall', 'skill', 'notes']

display_columns = [k for k in bc.climb_file_columns[1:]]
for k in testdict.keys():
    if k in dont_always_display_keys:
        try:
            display_columns.remove(k)
        except ValueError:
            pass

dict_try_to_delete_display_keys = {
    ('climb_style', 'bouldering'): ['rope'],
    ('climb_style', 'sport'): ['angle', 'mbyear'],
    ('door', 'indoor'): ['climb_name', 'angle', 'mbyear', 'rock_type'],
    ('door', 'outdoor'): ['angle', 'mbyear'],
    ('door', 'moonboard'): ['rock_type', 'rope'],
    ('rope') : ['angle', 'mbyear'],
    ('rock_type'):['angle', 'mbyear', 'door'],
    ('angle'):['rock_type', 'style', 'door', 'rope'],
    ('mbyear'):['rock_type', 'style', 'door', 'rope'],
}

for k in ['climb_style', 'door', 'rope', 'rock_type', 'angle', 'mbyear']:
    if k in testdict.keys():
        if k in ['climb_style', 'door']:
            kk = (k, testdict[k][0])
        else:
            kk = (k)
        for j in dict_try_to_delete_display_keys[kk]:
            try:
                display_columns.remove(j)
            except ValueError:
                pass

print(testdict)
print(display_columns)
print(filtered_climbs_df[display_columns])
#%%
import csv
with open(fpath, "r") as climbsfile:
    reader = csv.reader(climbsfile, delimiter = ',', )
    for row in reader:
        print(','.join(row))
#%%
climbs_df = pd.read_csv(fpath, header=0,\
            index_col =0, dtype=None, engine=None, converters={'climb_id':int},\
            skipinitialspace=True, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True,\
            na_filter=True, parse_dates=None, comment='#')

for row in climbs_df.itertuples(index =True, name = None):
    cid = row[0]
    style = row[1]
    grade = row[2]
    door= row[3]
