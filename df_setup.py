# -*- coding: utf-8 -*-
"""
@author: jbrown888
"""

# Generate sample data of climbs and attempts in a pandas dataframe
# see initial_df_setup_testing.py for process, and explanations/tips on pandas

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
    #generates random year between 2020 and 2025, and random days between 0 and 150(so not in future), adds together and returns as datetime object, normalized timestamp to midnight
    'success': np.random.choice([True, False], num_attempts),
}

# Create DataFrames
climbs_df = pd.DataFrame(climb_data)
attempts_df = pd.DataFrame(attempt_data)
attempts_grouped_climbid = attempts_df.groupby(['climb_id']) # this groups attempt dates by climb_id in groupby object


# Remove randomly generated climbs with no attempts

# as generated randomly, there won't necessarily be attempts for all climbs! when groupby is called, it drops 
# the climb_id's with no attempts, hence aggreate is shorter.
# In future, should back in the climb_id's with no attempts as null values?
# as even though will only create climbs with attempts, may want to go back and delete attempts!
# for now easier to delete.
# 1. find indexs of climbs with no attempts
all_climb_ids = range(num_climbs)
used_climb_ids = attempts_grouped_climbid.size().index
climbs_with_no_attempts = [x for x in all_climb_ids if x not in used_climb_ids]
climbs_df.drop(index = climbs_with_no_attempts,inplace = True) # drops unused indexs from climbs_df


#Aggregate data:
first_attempts = attempts_grouped_climbid['attempt_date'].apply(lambda x: x.min()) # finds first attempt date for each climb_id group
latest_attempts = attempts_grouped_climbid['attempt_date'].apply(lambda x: x.max()) # finds latest attempt date for each climb_id group
sent_statuses = attempts_grouped_climbid['success'].apply(lambda x: x.any()) # checks if success column has any trues for each climb_id group
total_number_attempts = attempts_grouped_climbid.size()


# Calculate initial send date
# testing lambda function on groups
dtest = attempts_grouped_climbid
for name_of_group, contents_of_group in dtest:
    y = contents_of_group
    z =(lambda x: x[x['success']==True]['attempt_date'].min() if x['success'].any() else None)(y)
# alternative method to check that the oneliner does work!
d = []
for x, y in attempts_grouped_climbid:
    yy = y[y['success']==True]
    d.append([x,yy['attempt_date'].min()])
# woo! both agree!
# GroupBy.transform calls the specified function for each column in each group!! so calls it on each series in each group. NOT on each group!!!
# need apply! not transform!!
first_sends = attempts_grouped_climbid.apply(lambda x: x[x["success"]==True]['attempt_date'].min() if x["success"].any() else None)

# Calculate number of attempts to send
# complicated as may have attempted and failed at some point AFTER the first send date
attempts_to_send = attempts_grouped_climbid.apply(lambda x: x[x['attempt_date'] <= x[x['success']==True]['attempt_date'].min()].shape[0] if x['success'].any() else 0)
# counts number of attempts before first True, including attempts on the same day (so>=1)
# If no successsful attempts for that climb, returns 0
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
# error! all the groupby apply operations have returned series len 98. climbid len 100. what was dropped?
# as generated randomly, there won't necessarily be attempts for all climbs! when groupby is called, it drops 
# the climb_id's with no attempts, hence aggreate is shorter.
# need to add back in the climb_id's with no attempts as null values?
# as even though will only create climbs with attempts, may want to go back and delete attempts!


agg_df = pd.DataFrame(aggregate_data)
agg_df.set_index(climbs_df.index, inplace = True)
agg_df.index.name  = 'climb_id'


#%%
# Merge climbs and attempts dataframes - does this actually need doing?
df = pd.merge(attempts_df, climbs_df, left_on='climb_id', right_index=True)
# left_on : column or index level names to join on in the left DataFrame.
# right_on : column or index level names to join on in the right DataFrame.
# right_index = True: use the index of the right DataFrame as the join key.


#%% Selecting specific groups of climbs

# my method, allows to select only some categories without new groupby object
dict_select = {
                'climb_style': ['bouldering'],
                'grade': ['V7', 'f8a'],
               }
group = climbs_df.loc[(climbs_df[list(dict_select)].isin(dict_select)).all(axis=1)]

# groupby method
gg = climbs_df.groupby([*dict_select.keys()])
df_group = pd.concat([gg.get_group(('bouldering', 'V7')), gg.get_group(('bouldering', 'f8a'))], axis = 0)  

# have checked - these are equivalent methods! return exactly the same indexs i.e. select same rows. approx same time for narrow criteria
# but return diff order

# print
want_to_print = False # set to true if want to print out groupby object.
if want_to_print:
    for name_of_group, contents_of_group in attempts_grouped_climbid:
        print(name_of_group)
        print(contents_of_group)
