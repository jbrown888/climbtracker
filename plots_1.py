# -*- coding: utf-8 -*-
"""
@author: jbrown888
6/6/24
#cwd = D:\\j_Documents\\cliimbing\\

Plot climbs - using own imported data
NOTE: for large dataframes, gp = df.groupby:
keys = [key for key, _ in gp] is much much faster than gp.groups.keys()!
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import figures_ as ff
import broomcupboard as bc
import itertools
import re
from importlib import reload

#%%
dirpath = os.path.join(os.getcwd(), 'real_data')

attempts_fpath = os.path.join(dirpath, 'attempts_data.csv')
climbs_fpath = os.path.join(dirpath, 'climbs_data.csv')

climbs_df = pd.read_csv(climbs_fpath, header=0,\
                 index_col =0, dtype=None, engine=None, converters={'climb_id':int},\
                 skipinitialspace=True, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True,\
                 na_filter=True, parse_dates=None, comment='#')

attempts_df= pd.read_csv(attempts_fpath, header=0, index_col=None, dtype=None, engine=None,
                                    converters=None, skipinitialspace=True, skiprows=None, skipfooter=0,
                                    nrows=None, na_values=None, keep_default_na=True, na_filter=True,
                                    parse_dates=['attempt_date'], date_format='%Y-%m-%d', dayfirst=False, comment='#')


attempts_grouped_climbid = attempts_df.groupby(['climb_id']) # this groups attempt dates by climb_id in groupby object

# Remove climbs with no attempst
# in future better practise to add rows with null values for climbs with no attempts.
all_climb_ids = climbs_df.index
used_climb_ids = attempts_grouped_climbid.size().index
climbs_with_no_attempts = [x for x in all_climb_ids if x not in used_climb_ids]
climbs_df.drop(index = climbs_with_no_attempts,inplace = True) # drops unused indexs from climbs_df

agg_df = bc.statistics_on_all_climbs(attempts_fpath)


#%% 
# see selecting_climbs.py for options for selection and speeds

dict_select = {
                'climb_style': ['bouldering'],
                # 'grade': ['V5-7', 'V2-4'],
                'location': ['Rockover'],
                # 'door': ['outdoor'],
                # 'wall': ['overhang']
               }

# for g in dict_select['grades']:
#     if re.match(bc.Vgrades_range_regex_pattern, g):
#         ranged_grades = bc.get_grades_in_range(g)
if dict_select.keys():
    # if 'grade' in dict_select:
    #     bc.append_equivalent_grades(dict_select['grade'])

    gg = climbs_df.groupby([*dict_select.keys()])

    if len(dict_select.keys()) == 1:
           for v in dict_select.values(): 
            indices_arr = [gg.get_group((x,)).index for x in v]
        # separate case as itertools.product returns a tuple as eg ('f6b',), and group keys look like 'f6b'
        # in future version of pandas, when grouping with length-1 list-like you will need to pass a length-1 tuple to get_group, ie '(name,)'
        # this seems a bit of an oversight...
    else:
        indices_arr = [gg.get_group(x).index for x in itertools.product(*dict_select.values()) if x in gg.groups.keys()]
    indices = list(itertools.chain.from_iterable(indices_arr))
    if len(indices) == 0:
        print("No climbs matching specified criteria of "+', '.join([f'{key}:{value}' for key, value in dict_select.items()]))

    reduced_agg_df = agg_df.loc[indices]
    reduced_climbs_df = climbs_df.loc[indices]
else:
    reduced_agg_df = agg_df
    reduced_climbs_df = climbs_df

# might be a good idea to here merge the grouping columns of climbs_df with agg_df? then don't have to keep extracting indices
# and finding agg_df[indices]

reduced_df = pd.merge(reduced_agg_df, reduced_climbs_df['grade'], how = 'inner', on='climb_id', validate = "1:1")

#%%
# graph for number of attempts to send for each grade
reduced_df = pd.merge(reduced_agg_df, reduced_climbs_df['grade'], how = 'inner', on='climb_id', validate = "1:1")
df_grouped_grades = reduced_df.groupby(['grade'])
# grade_groups_indexs = [x for x in df_grouped_grades.groups.values()] # returns indexs of each grade group
grades = [k for k in df_grouped_grades.groups.keys()]

ff.infile_figparams_vscode['labelsize'] = 20
ff.infile_figparams_vscode['ticksize'] = 15

fig, ax = plt.subplots(figsize = (10,6))
ff.standard_axes_settings(ax)

for i in range(df_grouped_grades.ngroups):
    ax.plot([grades[i]]*df_grouped_grades.size().iloc[i], df_grouped_grades.get_group((grades[i],))['attempts_to_send'], **ff.marker_plus, label = grades[i])

ax.set_xlabel('Grade')
ax.set_ylabel('Attempts to send')

leg = ax.legend(fontsize = 22, loc='best', markerfirst = True, frameon = True)
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_facecolor('w')
# ax.set_xlim([-.01, 5])
# ax.set_ylim([0, 80])
ax.set_title('Attempts till send by grade', fontsize = 24)

# %%
# graph for number of attempts to send for each grade over time, unaveraged

reduced_df = pd.merge(reduced_agg_df, reduced_climbs_df['grade'], how = 'inner', on='climb_id', validate = "1:1")
df_grouped_grades = reduced_df.groupby(['grade'])
# grade_groups_indexs = [x for x in df_grouped_grades.groups.values()] # returns indexs of each grade group
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

# format xticks
# # Set the locators for the x-axis
months = mdates.MonthLocator()  # Every month
days = mdates.WeekdayLocator()  # Every year
ax.xaxis.set_major_locator(days)
ax.xaxis.set_minor_locator(months)
# Set the date format
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(days))

for i in range(df_grouped_grades.ngroups):
    ff.marker_point.update({'mfc':cs[i], 'color':cs[i]})
    toplot = df_grouped_grades.get_group((grades[i],)).sort_values(by = 'first_send_date', axis = 0, inplace =False)
    ax.plot(toplot['first_send_date'], toplot['attempts_to_send'], **ff.marker_point, label = grades[i])

ax.set_xlabel('Grade')
ax.set_ylabel('Attempts to send')

leg = ax.legend(fontsize = 22, loc='best', markerfirst = True, frameon = True)
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_facecolor('w')
# ax.set_xlim([-.01, 5])
# ax.set_ylim([0, 80])
ax.set_title('Attempts till send by grade', fontsize = 24)
#%%
# graph for number of attempts to send for each grade over time, averaged over each month

# get grade indexs
reduced_df = pd.merge(reduced_agg_df, reduced_climbs_df['grade'], how = 'inner', on='climb_id', validate = "1:1")
df_grouped_grades = reduced_df.groupby(['grade'])
# grade_groups_indexs = [x for x in df_grouped_grades.groups.values()] # returns indexs of each grade group
grades = [k for k in df_grouped_grades.groups.keys()]
num_grades = df_grouped_grades.ngroups

# monthly averages
# group agg_df into months by first_send_date column
i = 0
# initial idea - but this sets all the first_send_date values to last day of the month, rather than just the month
test3 = df_grouped_grades.get_group((grades[i],)).groupby(pd.Grouper(key = 'first_send_date', freq = 'MS', sort = True, label = 'left'))
toplot3 = test3[['total_number_attempts', 'attempts_to_send']].mean(numeric_only=True)
# not M is freq month end, so overrides convention= 'start'. need to use freq = 'MS', don't pass convention argument
#try 2
one_grade_data = df_grouped_grades.get_group((grades[i],))
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
    ff.marker_ok_line.update({'mec':cs[i], 'color':cs[i]})
    one_grade_data = df_grouped_grades.get_group((grades[i],))
    if one_grade_data['sent_status'].any():
        toplot = one_grade_data.groupby(pd.Grouper(key = 'first_send_date', freq = 'MS', sort = True, label = 'left')).mean(numeric_only=True)
        ax.plot(toplot.index.values, toplot['attempts_to_send'], **ff.marker_ok_line, label = grades[i])
    else:
        pass


leg = ax.legend(fontsize = ff.infile_figparams_vscode['labelsize'], loc='best', markerfirst = True, frameon = True)
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_facecolor('w')
# ax.set_xlim([-.01, 5])
# ax.set_ylim([0, 80])
ax.set_title('Attempts till send by grade over time', fontsize = 12)
# %%
#%%
# graph for number of attempts to send for each grade over time, averaged over each week

# get grade indexs
reduced_df = pd.merge(reduced_agg_df, reduced_climbs_df['grade'], how = 'inner', on='climb_id', validate = "1:1")
df_grouped_grades = reduced_df.groupby(['grade'])
# grade_groups_indexs = [x for x in df_grouped_grades.groups.values()] # returns indexs of each grade group
grades = [k for k in df_grouped_grades.groups.keys()]
num_grades = df_grouped_grades.ngroups

# monthly averages
# group agg_df into week by first_send_date column
i = 0
test3 = df_grouped_grades.get_group((grades[i],)).groupby(pd.Grouper(key = 'first_send_date', freq = 'W', sort = True, label = 'left'))
toplot3 = test3[['total_number_attempts', 'attempts_to_send']].mean(numeric_only=True)
#try 2
one_grade_data = df_grouped_grades.get_group((grades[i],))
test4 = one_grade_data.groupby([one_grade_data['first_send_date'].dt.to_period('W')])
toplot4 = test4[['total_number_attempts', 'attempts_to_send']].mean(numeric_only=True)
# this method twice as fast (at least on small datasets) BUT can't plot Period objects, will then have to convert back to datetime

# create figure
ff.infile_figparams_vscode['labelsize'] = 14
ff.infile_figparams_vscode['ticksize'] = 8
ff.infile_figparams_vscode['visible'] = True

fig, ax = plt.subplots(figsize = (10,6))
ff.standard_axes_settings(ax)
ax.set_xlabel('Date')
ax.set_ylabel('Attempts to send')
# set colours
#for random colours: cm.Dark2 or cm.tab20 , for sequential: cm.cividis or cm.inferno
cs = [cm.cividis(i/num_grades, 1) for i in range(num_grades)]

# format xticks
# # Set the locators for the x-axis
months = mdates.MonthLocator()  # Every month
# days = mdates.DayLocator()  # Every day
years = mdates.YearLocator()  # Every year

ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(years)
# Set the date format
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(months))


for i in range(num_grades):
    ff.marker_ok_line.update({'mec':cs[i], 'color':cs[i]})
    one_grade_data = df_grouped_grades.get_group((grades[i],))
    if one_grade_data['sent_status'].any():
        toplot = one_grade_data.groupby(pd.Grouper(key = 'first_send_date', freq = 'W', sort = True, label = 'left')).mean(numeric_only=True)
        ax.plot(toplot.index.values, toplot['attempts_to_send'], **ff.marker_ok_line, label = grades[i])
    else:
        pass


leg = ax.legend(fontsize = ff.infile_figparams_vscode['labelsize'], loc='best', markerfirst = True, frameon = True)
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_facecolor('w')
# ax.set_xlim([-.01, 5])
# ax.set_ylim([0, 80])
ax.set_title('Attempts till send by grade over time', fontsize = 12)

#%%
# bar chart of total number of sends and attempts by grade

# get grade indexs
reduced_df = pd.merge(reduced_agg_df, reduced_climbs_df['grade'], how = 'inner', on='climb_id', validate = "1:1")
df_grouped_grades = reduced_df.groupby(['grade'])
# grade_groups_indexs = [x for x in df_grouped_grades.groups.values()] # returns indexs of each grade group
grades = [k for k in df_grouped_grades.groups.keys()]
num_grades = df_grouped_grades.ngroups

total_failures_no_repeats = np.empty(num_grades)

total_attempts = df_grouped_grades['total_number_attempts'].sum()
total_sends = df_grouped_grades['number_of_sends'].sum()
total_failures = total_attempts  - total_sends
total_sends_no_repeats = df_grouped_grades['sent_status'].sum()
# if sent_status is True, number_of_fails_without_repeats = attempts_to_send - 1. 
# if sent_status is False, number_of_attempts_without_repeats = total_number_of_attempts.
total_failures_no_repeats = np.empty(num_grades, dtype =np.int64)
for i in range(num_grades):
    g = df_grouped_grades.get_group((grades[i],))
    total_failures_no_repeats[i] = g.apply(lambda row: row['attempts_to_send'] - 1 if row['sent_status'] else row['total_number_attempts'], axis=1).sum()

climbattempts = {
    "Attempts": total_failures_no_repeats,
    "Sends": total_sends_no_repeats,
}
width = 0.5

ff.infile_figparams_vscode['labelsize'] = 14
ff.infile_figparams_vscode['ticksize'] = 8
ff.infile_figparams_vscode['visible'] = False
fig, ax = plt.subplots(figsize = (10,6))
ff.standard_axes_settings(ax)
ax.set_xlabel('Grade')
ax.set_ylabel('Attempts')
bottom = np.zeros(num_grades)

for boolean, climbattempt in climbattempts.items():
    p = ax.bar(grades, climbattempt, width, label=boolean, bottom=bottom)
    bottom += climbattempt

ax.set_title("Number of attempts")
ax.legend(loc="upper right")

plt.show()

#%%
# bar chart of number of climbs tried vs number sent - 

# get grade indexs
reduced_df = pd.merge(reduced_agg_df, reduced_climbs_df['grade'], how = 'inner', on='climb_id', validate = "1:1")
df_grouped_grades = reduced_df.groupby(['grade'])
# grade_groups_indexs = [x for x in df_grouped_grades.groups.values()] # returns indexs of each grade group
grades = [k for k in df_grouped_grades.groups.keys()]
num_grades = df_grouped_grades.ngroups

total_attempted_climbs = df_grouped_grades.size()
total_sent_climbs = df_grouped_grades['sent_status'].sum()
total_not_sent_climbs = total_attempted_climbs - total_sent_climbs

climbattempts = {
    "Attempted": total_not_sent_climbs,
    "Sent": total_sent_climbs,
}
width = 0.5

ff.infile_figparams_vscode['labelsize'] = 14
ff.infile_figparams_vscode['ticksize'] = 8
ff.infile_figparams_vscode['visible'] = False
fig, ax = plt.subplots(figsize = (10,6))
ff.standard_axes_settings(ax)
ax.set_xlabel('Grade')
ax.set_ylabel('Climbs')
bottom = np.zeros(num_grades)
colors = ['lightgray','darkgreen']
i=0
for text, climbattempt in climbattempts.items():
    p = ax.bar(grades, climbattempt, width, label=text, bottom=bottom, color = colors[i])
    bottom += climbattempt
    i+=1
ax.set_title("Number of climbs tried")
ax.legend(loc="upper right")

plt.show()

#%%
# bar chart of number of climbs tried vs number sent for a grade over time

# get grade indexs
reduced_df = pd.merge(reduced_agg_df, reduced_climbs_df['grade'], how = 'inner', on='climb_id', validate = "1:1")
df_grouped_grades = reduced_df.groupby(['grade'])
grade = 'V4-6'
one_grade_data = df_grouped_grades.get_group(grade)
grouped_by_date = one_grade_data.groupby(pd.Grouper(key = 'first_attempt_date', freq = 'MS', sort = True, label = 'left'))


total_attempted_climbs = grouped_by_date.size()
total_sent_climbs = grouped_by_date['sent_status'].sum()
total_not_sent_climbs = total_attempted_climbs - total_sent_climbs

climbattempts = {
    "Attempted": total_not_sent_climbs,
    "Sent": total_sent_climbs,
}
width = pd.Timedelta(value =15, unit = 'day')

ff.infile_figparams_vscode['labelsize'] = 16
ff.infile_figparams_vscode['ticksize'] = 14
ff.infile_figparams_vscode['visible'] = False
fig, ax = plt.subplots(figsize = (10,6))
ff.standard_axes_settings(ax)
ax.set_xlabel('Date')
ax.set_ylabel('Climbs')


months = mdates.MonthLocator()  # Every month
# days = mdates.DayLocator()  # Every day
years = mdates.YearLocator()  # Every year

ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(years)
# Set the date format
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(months))


bottom = np.zeros(grouped_by_date.ngroups)
colors = ['lightgray','darkgreen']
i=0
for text, climbattempt in climbattempts.items():
    p = ax.bar(climbattempt.index.values, climbattempt, width, label=text, bottom=bottom, color = colors[i])
    bottom += climbattempt
    i+=1
ax.set_title(f"Number of climbs tried Grade {grade}", fontsize = ff.infile_figparams_vscode['labelsize'])

leg = ax.legend(fontsize = ff.infile_figparams_vscode['labelsize'], loc='best', markerfirst = True, frameon = True)
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_facecolor('w')


plt.show()

#%%
# graph for number of attempts made for each grade over time, averaged over each week

# get grade indexs
reduced_df = pd.merge(reduced_agg_df, reduced_climbs_df['grade'], how = 'inner', on='climb_id', validate = "1:1")
df_grouped_grades = reduced_df.groupby(['grade'])
# grade_groups_indexs = [x for x in df_grouped_grades.groups.values()] # returns indexs of each grade group
grades = [k for k in df_grouped_grades.groups.keys()]
num_grades = df_grouped_grades.ngroups

# monthly averages
# group agg_df into week by first_attempt_date
i = 4
test3 = df_grouped_grades.get_group((grades[i],)).groupby(pd.Grouper(key = 'first_attempt_date', freq = 'W', sort = True, label = 'left'))
toplot3 = test3[['total_number_attempts']].mean(numeric_only=True)
#try 2
one_grade_data = df_grouped_grades.get_group((grades[i],))
test4 = one_grade_data.groupby([one_grade_data['first_attempt_date'].dt.to_period('W')])
toplot4 = test4[['total_number_attempts']].mean(numeric_only=True)
# this method twice as fast (at least on small datasets) BUT can't plot Period objects, will then have to convert back to datetime

# create figure
ff.infile_figparams_vscode['labelsize'] = 14
ff.infile_figparams_vscode['ticksize'] = 8
ff.infile_figparams_vscode['visible'] = True

fig, ax = plt.subplots(figsize = (10,6))
ff.standard_axes_settings(ax)
ax.set_xlabel('Date')
ax.set_ylabel('Total Attempts')
# set colours
#for random colours: cm.Dark2 or cm.tab20 , for sequential: cm.cividis or cm.inferno
cs = [cm.cividis(i/num_grades, 1) for i in range(num_grades)]

# format xticks
# # Set the locators for the x-axis
months = mdates.MonthLocator()  # Every month
# days = mdates.DayLocator()  # Every day
years = mdates.YearLocator()  # Every year

ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(years)
# Set the date format
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(months))


for i in range(num_grades):
    ff.marker_ok_line.update({'mec':cs[i], 'color':cs[i]})
    one_grade_data = df_grouped_grades.get_group((grades[i],))
    toplot = one_grade_data.groupby(pd.Grouper(key = 'first_attempt_date', freq = 'W', sort = True, label = 'left')).mean(numeric_only=True)
    ax.plot(toplot.index.values, toplot['total_number_attempts'], **ff.marker_ok_line, label = grades[i])


leg = ax.legend(fontsize = ff.infile_figparams_vscode['labelsize'], loc='best', markerfirst = True, frameon = True)
leg.get_frame().set_edgecolor('k')
leg.get_frame().set_facecolor('w')
# ax.set_xlim([-.01, 5])
# ax.set_ylim([0, 80])
ax.set_title('Number of attempts by grade over time', fontsize = 12)
