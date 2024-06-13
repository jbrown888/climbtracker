# -*- coding: utf-8 -*-
"""
@author: jbrown888
7/6/24
#cwd = D:\\j_Documents\\cliimbing\\
# see initial_df_setup_testing.py for process, and explanations/tips on pandas
# Generating sample data of climbs and attempts in a pandas dataframe - INPUT
# initial phases
"""


import pandas as pd
import numpy as np
import datetime as dt


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

# Generate random attempt data
num_attempts = 500
attempt_data = {
    'climb_id': np.random.choice(range(num_climbs), num_attempts), #chooses 500 attempts across 100 climb_ids
    'attempt_date': (pd.to_datetime(np.random.randint(2020, 2025, num_attempts), format='%Y', utc = False) + pd.to_timedelta(np.random.randint(0, 150, num_attempts), unit='D')).normalize(),
    #generates random year between 2020 and 2025, and random days between 0 and 150(so not in future), adds together and returns as datetime object
    #technically only need date. BUT
    # Avoid, where possible, converting your datetime64[ns] series to an object dtype series of datetime.date objects. 
    # The latter, often constructed using pd.Series.dt.date, is stored as an array of pointers and is inefficient relative 
    # to a pure NumPy-based series.
    # normalize sets timestamp to midnight on all dates.
    # .dt.floor('d') rather than .normalize() performs slightly better on large datasets, but must be called on the df column once the df is created
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




#%% Initial method of calculating initial send date and sent status for each climb, 6/6/24 

# Merge climbs and attempts dataframes - does this actually need doing?
df = pd.merge(attempts_df, climbs_df, left_on='climb_id', right_index=True)
# left_on : column or index level names to join on in the left DataFrame.
# right_on : column or index level names to join on in the right DataFrame.
# right_index = True: use the index of the right DataFrame as the join key.

df_grouped = df.groupby(['climb_id', 'climb_style', 'grade', 'door', 'location']) # this groups across all specifiers
# don't really understand why it needed doing across all columns, surely climb_id would have been sufficient. yep - group sizes are exactly the same if group only by climb_id
first_attempt_dates= df_grouped['attempt_date'].apply(lambda x: x.min())
latest_attempt_dates= df_grouped['attempt_date'].apply(lambda x: x.max())
sent_statuses = df_grouped['success'].apply(lambda x: x.any()) # checks if success column has any trues for each group. this one actually works.

# Calculate initial send date and sent status for each climb
# testing lambda function on groups
dtest = df_grouped[['climb_id','attempt_date', 'success']]
for name_of_group, contents_of_group in dtest:
    y = contents_of_group
    z =(lambda x: x[x['success']==True]['attempt_date'].min() if x['success'].any() else None)(y)
# note: groupby and transform drops the index on columns you group by.  "transformations do not include the groupings that are used to split the result"
# GroupBy.transform calls the specified function for each column in each group!! so calls it on each series in each group. NOT on each group!!!
# need apply! not transform!!
ddd = df_grouped[['climb_id','attempt_date', 'success']].apply(lambda x: x[x["success"]==True]['attempt_date'].min() if x["success"].any() else None)
#didn't work with .transform. does with .apply!!
# but apply returns a series witth rows of dataframe for some reason, so can't add to df. how to gert it to return datagrame object? or series of just send date?
# if group the attempts_df rather than merged df, then this works! apply returns a series of just send date. can be added to dataframe!
# alternative method to check that the oneliner does work!
d = []
for x, y in df_grouped[['climb_id','attempt_date', 'success']]:
    yy = y[y['success']==True]
    d.append([x[0],yy['attempt_date'].min()])
# woo! both agree!


# Calculate number of attempts to send
# complicated as may have attempted and failed at some point AFTER the first send date - so can't just count false's
attempts_grouped_climbid = attempts_df.groupby(['climb_id']) # this groups attempt dates by climb_id in groupby object
# stepbystep
num = []
for x, y in attempts_grouped_climbid:
    yy = y[y['success']==True]
    d = yy['attempt_date'].min() # initial send date
    mask = y['attempt_date'] <= d
    ybefore = y[mask] # attempts before initial send
    num.append(ybefore.shape[0])# number of attempts before initial send, including sent attempt
    # assumes you don't try again the same day after you send.
# lambda
nums = []
dtest = attempts_grouped_climbid
for name_of_group, contents_of_group in dtest:
    y = contents_of_group 
    z = (lambda x: x[x['attempt_date'] <= x[x['success']==True]['attempt_date'].min()].shape[0] if x['success'].any() else 0)(y)
    # counts number of attempts before first True, including attempts on the same day (so>=1). If no successsful attempts for that climb, returns 0
    nums.append(z)
# num = nums! methods agree!
# now oneliner
numss = attempts_grouped_climbid.apply(lambda x: x[x['attempt_date'] <= x[x['success']==True]['attempt_date'].min()].shape[0] if x['success'].any() else 0)
# all(num==numss) gives True! woo :)




# wrong methods from tabnine :
# note these columns shouldn't be added to df - they are calculated from the attempts and specific to the climb. they should be added to climb_df instead
# df['initial_send_date'] = df_grouped['attempt_date'].transform(lambda groupx: x[x].min())
# transform Returns a DataFrame having the same indexes as the original object (df, ungrouped) filled with the transformed values.
# works on one series at a time.
# df_grouped['attempt_date'] simply restricts df_grouped to only the attempt_date column. transform applies lambda function. lambda function finds the first attempt date (note NOT first sent date) 
# x is input parameter: represents panda series containing attempt_date values for each group
# x[x] is boolean indexing operation that filters the series x based on condition x. selects only attempt_date values that are not null or NaN
#  x[x] is a boolean indexing operation that creates a new Series with the same length as x.
# The boolean values in the new Series are determined by the condition x. If the value in x is not null or NaN, the corresponding value in the new Series will be True; otherwise, it will be False
# how could this ever work??


# Display the resulting dataframe
# df.head()

#%% Selecting specific groups of climbs

# my method, allows to select only some categories without new groupby object
dict_select = {
                'climb_style': ['bouldering'],
               'grade': ['V7', 'f8a'],
               }
group = df.loc[(df[list(dict_select)].isin(dict_select)).all(axis=1)]

# groupby method
gg = df.groupby([*dict_select.keys()])
df_group = pd.concat([gg.get_group(('bouldering', 'V7')), gg.get_group(('bouldering', 'f8a'))], axis = 0)  

# have checked - these are equivalent methods! return exactly the same indexs i.e. select same rows. approx same time for narrow criteria



#%%
# Some methods and useful info about groupby



df.grade.nunique() # returns unique number of grades in ungrouped df

df_grouped.ngroups # total number of groups

df_grouped.size() # returns how many rows are in each group. If grouping by many categories, will return table
# gives number of rows, irrespective of presence or absence of values

df_grouped.count() # similar to size() but counts the non-null values for each column

df_grouped.first() # or last . returns first/last row from each gruop (with non-null values in each column)

df_grouped.nth(2) # simlar to first/last but extracts nth row - takes argument. note nth returns irrespective of null values
df_grouped.groups.keys() # should return list of keys for each group

df_grouped.get_group([*df_grouped.groups.keys()][0]) # select or extract only one group from groupby object. takes str.
# if multiple grouping keys, supply same length tuple of keys eg get_group(('V7', 'Crag 2', 'bouldering', 'indoor'))
# eg df[df['grade']=='V7'] equivalent to doing g = df.groupby('grade') and g.get_group('V7'). groupby method more efficient

# remember groupby object is dictionary!. can iterate
want_to_print = False # set to true if want to print out groupby object.
if want_to_print:
    for name_of_group, contents_of_group in df_grouped:
        print(name_of_group)
        print(contents_of_group)

# aggregate functions:
df_grouped[['grade', 'door']].mean() # if numerical data
# can apply multiple at once
df_grouped[['grade', 'door']].aggregate([min, max, sum, 'mean'])

# hh
