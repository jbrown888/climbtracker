# -*- coding: utf-8 -*-
"""
@author: jbrown888
6/6/24
#cwd = D:\\j_Documents\\cliimbing\\
"""

# see initial_df_setup_testing.py for process, and explanations/tips on pandas


import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import figures_ as ff
import itertools
from importlib import reload


#%%
# Generate sample data of climbs and attempts in a pandas dataframe - INPUT
np.random.seed(0)
# Define climb styles, grades, doors, and locations
climb_styles = ['bouldering', 'sport', 'trad']
grades = ['f5a', 'f6a', 'V7', 'f8a', 'V2']
doors = ['indoor', 'outdoor']
locations = ['Rockover', 'Summit Up', 'Crag 1', 'Crag 2']
# Generate random data for climbs and attempts
num_climbs = 100
climb_data = {
    #dictionary of lists length num_climbs of randomly selected values 
    #np.random.choice(list_to_selct_from, number to select) generates random sample from given 1d array
    'climb_style': np.random.choice(climb_styles, num_climbs),
    'grade': np.random.choice(grades, num_climbs),
    'door': np.random.choice(doors, num_climbs),
    'location': np.random.choice(locations, num_climbs),
}
category_from_str_dict= {'climb_style': climb_styles, 'grade': grades, 'door': doors, 'location': locations}
# selected_categories = [category_from_str_dict[key] for key in dict_select.keys()]
# qq = itertools.product(*selected_categories) # this gives ALL possible combinations of selected categories
qq = itertools.product((climb_styles, grades, doors, locations)) # this gives ALL possible combinations of selected categories




# Generate random attempt data
num_attempts = 500
attempt_data = {
    'climb_id': np.random.choice(range(num_climbs), num_attempts), #chooses 500 attempts across 100 climb_ids
    'attempt_date': (pd.to_datetime(np.random.randint(2020, 2025, num_attempts), format='%Y', utc = False) + pd.to_timedelta(np.random.randint(0, 150, num_attempts), unit='D')).normalize(),
    #generates random year between 2020 and 2025, and random days between 0 and 150(so not in future), adds together and returns as datetime object, normalized timestamp to midnight
    'success': np.random.choice([True, False], num_attempts),
}

# Create DataFrames
climbs_df = pd.DataFrame(climb_data)
attempts_df = pd.DataFrame(attempt_data)



# Remove randomly generated climbs with no attempts
attempts_grouped_climbid = attempts_df.groupby(['climb_id']) # this groups attempt dates by climb_id in groupby object

# as generated randomly, there won't necessarily be attempts for all climbs! for now easier to delete 'empty' climbs
# in future better practise to add rows with null values for climbs with no attempts.
all_climb_ids = range(num_climbs)
used_climb_ids = attempts_grouped_climbid.size().index
climbs_with_no_attempts = [x for x in all_climb_ids if x not in used_climb_ids]
climbs_df.drop(index = climbs_with_no_attempts,inplace = True) # drops unused indexs from climbs_df

# %%
# OUTPUT

#Aggregate data:
first_attempts = attempts_grouped_climbid['attempt_date'].apply(lambda x: x.min()) # finds first attempt date for each climb_id group
latest_attempts = attempts_grouped_climbid['attempt_date'].apply(lambda x: x.max()) # finds latest attempt date for each climb_id group
sent_statuses = attempts_grouped_climbid['success'].apply(lambda x: x.any()) # checks if success column has any trues for each climb_id group
total_number_attempts = attempts_grouped_climbid.size()
first_sends = attempts_grouped_climbid.apply(lambda x: x[x["success"]==True]['attempt_date'].min() if x["success"].any() else None)
attempts_to_send = attempts_grouped_climbid.apply(lambda x: x[x['attempt_date'] <= x[x['success']==True]['attempt_date'].min()].shape[0] if x['success'].any() else None)
# counts number of attempts before first True, including attempts on the same day (so>=1)
# If no successsful attempts for that climb, returns None
# Assumes you don't try again the same day after sending!
# May be more efficient to pull first send date (x[x['success']==True]['attempt_date'].min()) values from elsewhere, need to check.

aggregate_data = {
    # 'climb_id': climbs_df.index,
    'first_attempt_date': first_attempts,
    'latest_attempt_date': latest_attempts,
    'sent_status': sent_statuses,
    'total_number_attempts': total_number_attempts,
    'first_send_date': first_sends,
    'attempts_to_send': attempts_to_send,
}

agg_df = pd.DataFrame(aggregate_data)
agg_df.set_index(climbs_df.index, inplace = True)
agg_df.index.name  = 'climb_id'



# %%
# Merge climbs and attempts dataframes - does this actually need doing?
df = pd.merge(attempts_df, climbs_df, left_on='climb_id', right_index=True)
# left_on : column or index level names to join on in the left DataFrame.
# right_on : column or index level names to join on in the right DataFrame.
# right_index = True: use the index of the right DataFrame as the join key.


#%% Selecting specific groups of climbs

# my method, allows to select only some categories without new groupby object
dict_select = {
                'climb_style': ['bouldering', 'sport'],
                'grade': ['f6a', 'V7', 'f8a', 'V2'],
                'location': ['Rockover', 'Summit Up', 'Crag 1'],
                'door': ['indoor', 'outdoor'],
               }
group = climbs_df.loc[(climbs_df[list(dict_select)].isin(dict_select)).all(axis=1)]
group_agg_data = agg_df.loc[group.index]
# TIME IT: 4.19ms for 4 permutations, 4.41ms for 26 permutations


# groupby method 1
gg = climbs_df.groupby([*dict_select.keys()])
# there aren't necessarily climbs for all combinations of categories, want to iterate over dict_select.values
df_group = pd.concat([gg.get_group(x) for x in itertools.product(*dict_select.values()) if x in gg.groups.keys()], axis = 0)
group_agg_data2 = agg_df.loc[df_group.index] # quite wasteful - creates a new df
# TIME IT 4.79ms for 4 permutations, 12.1ms for 26 permutations
# OR 2
indices_arr = [gg.get_group(x).index for x in itertools.product(*dict_select.values()) if x in gg.groups.keys()]
group_agg_data3 = agg_df.loc[list(itertools.chain.from_iterable(indices_arr))]
# TIME IT 5.72ms for 4 permutations, 7.41ms for 26 permutations


# indices = [gg.indices[x] for x in itertools.product(*dict_select.values()) if x in gg.groups.keys()] 
# When you access the indices attribute of a GroupBy object, it returns the index labels of the groups
# not the index labels of the original DataFrame.
# have checked - these are equivalent methods! return exactly the same indexs i.e. select same rows. approx same time for narrow criteria
# but return diff order

# print
want_to_print = False # set to true if want to print out groupby object.
if want_to_print:
    for name_of_group, contents_of_group in attempts_grouped_climbid:
        print(name_of_group)
        print(contents_of_group)

# %%
# graph for number of attempts to send for each grade
df_grouped_grades = climbs_df.groupby(['grade'])
grade_groups_indexs = [x for x in df_grouped_grades.groups.values()] # returns indexs of each grade group
grades = [k for k in df_grouped_grades.groups.keys()]

ff.infile_figparams_vscode['labelsize'] = 20
ff.infile_figparams_vscode['ticksize'] = 15

fig, ax = plt.subplots(figsize = (10,6))
ff.standard_axes_settings(ax)

for i in range(df_grouped_grades.ngroups):
    ax.plot([grades[i]]*df_grouped_grades.size()[i], agg_df.loc[grade_groups_indexs[i]]['attempts_to_send'], **ff.marker_plus, label = grades[i])

ax.set_xlabel('Grade')
ax.set_ylabel('Attempts to send')

leg = ax.legend(fontsize = 22, loc='best', markerfirst = True, frameon = True)
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_facecolor('w')
# ax.set_xlim([-.01, 5])
# ax.set_ylim([0, 80])
ax.set_title('Attempts to send by grade', fontsize = 24)

# %%
# graph for number of attempts to send for each grade over time
df_grouped_grades = climbs_df.groupby(['grade'])
grade_groups_indexs = [x for x in df_grouped_grades.groups.values()] # returns indexs of each grade group
grades = [k for k in df_grouped_grades.groups.keys()]
num_grades = df_grouped_grades.ngroups
ff.infile_figparams_vscode['labelsize'] = 20
ff.infile_figparams_vscode['ticksize'] = 15

fig, ax = plt.subplots(figsize = (10,6))
ff.standard_axes_settings(ax)

# set colours
#for random colours: cm.Dark2 or cm.tab20 
#for sequential: cm.cividis or cm.inferno
cs = [cm.tab20(i/num_grades, 1) for i in range(num_grades)]

for i in range(df_grouped_grades.ngroups):
    toplot = agg_df.loc[grade_groups_indexs[i]].sort_values(by = 'first_send_date', axis = 0, inplace =False)
    ax.plot(toplot['first_send_date'], toplot['attempts_to_send'], ls = '-', marker = 'None', lw = 1, color = cs[i], label = grades[i])

ax.set_xlabel('Grade')
ax.set_ylabel('Attempts to send')

leg = ax.legend(fontsize = 22, loc='best', markerfirst = True, frameon = True)
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_facecolor('w')
# ax.set_xlim([-.01, 5])
# ax.set_ylim([0, 80])
ax.set_title('Attempts to send by grade', fontsize = 24)
#%%
# graph for number of attempts to send for each grade over time, averaged over each month

# get grade indexs
df_grouped_grades = climbs_df.groupby(['grade'])
grade_groups_indexs = [x for x in df_grouped_grades.groups.values()] # returns indexs of each grade group
grades = [k for k in df_grouped_grades.groups.keys()]
num_grades = df_grouped_grades.ngroups

# monthly averages
# group agg_df into months by first_send_date column
i = 0
# initial idea - but this sets all the first_send_date values to last day of the month, rather than just the month
test3 = agg_df.loc[grade_groups_indexs[i]].groupby(pd.Grouper(key = 'first_send_date', freq = 'MS', sort = True, label = 'left'))
toplot3 = test3[['total_number_attempts', 'attempts_to_send']].mean(numeric_only=True)
# not M is freq month end, so overrides convention= 'start'. need to use freq = 'MS', don't pass convention argument
#try 2
one_grade_data = agg_df.loc[grade_groups_indexs[i]]
test4 = one_grade_data.groupby([one_grade_data['first_send_date'].dt.to_period('M')])
toplot4 = test4[['total_number_attempts', 'attempts_to_send']].mean(numeric_only=True)
# this method twice as fast (at least on small datasets) BUT can't plot Period objects, will then have to convert back to datetime

# create figure
ff.infile_figparams_vscode['labelsize'] = 14
ff.infile_figparams_vscode['ticksize'] = 8
fig, ax = plt.subplots(figsize = (10,6))
ff.standard_axes_settings(ax)
ax.set_xlabel('Date')
ax.set_ylabel('Attempts to send')
# set colours
#for random colours: cm.Dark2 or cm.tab20 , for sequential: cm.cividis or cm.inferno
cs = [cm.tab20(i/num_grades, 1) for i in range(num_grades)]

# format xticks
# # Set the locators for the x-axis
months = mdates.MonthLocator(interval=4)  # Every month
years = mdates.YearLocator()  # Every year
ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(years)
# Set the date format
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(months))


for i in range(num_grades):
    toplot = agg_df.loc[grade_groups_indexs[i]].groupby(pd.Grouper(key = 'first_send_date', freq = 'MS', sort = True, label = 'left')).mean(numeric_only=True)
    ff.marker_ok_line.update({'mec':cs[i], 'color':cs[i]})
    ax.plot(toplot.index.values, toplot['attempts_to_send'], **ff.marker_ok_line, label = grades[i])


leg = ax.legend(fontsize = ff.infile_figparams_vscode['labelsize'], loc='best', markerfirst = True, frameon = True)
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_facecolor('w')
# ax.set_xlim([-.01, 5])
# ax.set_ylim([0, 80])
ax.set_title('Attempts to send by grade over time', fontsize = 12)
