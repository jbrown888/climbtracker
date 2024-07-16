# -*- coding: utf-8 -*-
"""
@author: jbrown888
8/6/24
#cwd = D:\\j_Documents\\cliimbing\\
# testing appending to attempts data file
# see write_to_climbs_file.py for trial and error process in appending
"""


import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.dates as mdate
import itertools
from importlib import reload
import csv 
from add_new_attempt_function import add_new_attempt_to_file
import add_new_attempt_function


#%%
dirpath = os.path.join(os.getcwd(), 'sample_data')

# with open(os.path.join(dirpath, 'attempts_df.csv'), 'rb') as f:
#     test = f.readlines()

#%%
# Append to attempts_df.csv file
with open(os.path.join(dirpath, 'attempts_df.csv'), 'r', newline = '') as file:
    row_count = sum(1 for row in file)

with open(os.path.join(dirpath, 'attempts_df.csv'), 'rb') as f:
    try:  # catch OSError in case of a one line file 
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
    except OSError:
        f.seek(0)
    last_line = f.readline().decode()
if last_line[:-2:-1] != '\n':
    raise Exception(f'File {os.path.join(dirpath, "attempts_df.csv")} does not end with a new line.')

newattempt_data = {
    'climb_id': 40,
    'attempt_date':dt.date(2021, 1, 22).isoformat(),
    'success': True,
    }

try:
    with open(os.path.join(dirpath, 'attempts_df.csv'), 'a', newline = '') as file:
        dictwriter = csv.DictWriter(file, fieldnames=['climb_id', 'attempt_date', 'success'], restval = '', extrasaction = 'raise') 
        dictwriter.writerow(newattempt_data)
    print("New line appended successfully to 'attempts_df.csv'.")
except Exception as e:
    print(f"Error appending new line to 'attempts_df.csv': {str(e)}")


#%%
attempts_df_read = pd.read_csv(os.path.join(dirpath, 'attempts_df.csv'), header=0,\
                 index_col=None, dtype=None, engine=None, converters=None,\
                 skipinitialspace=True, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True,\
                 na_filter=True, parse_dates=['attempt_date'],\
                 date_format='%Y-%m-%d', dayfirst=False, comment='#')

#%%
# ISSUES
# 1. Need to check that the new attempt's climb_id exists in climbs_df.csv
# 2. If it does not exist, need to append it to climbs_df.csv
# 3. If climb_id does already exist, need to update aggregate_df.csv for this climb.
# - to update aggregate_df.csv, better to read in and alter df, then save to csv?
# - or to change just the one line in aggregate_df.csv by rewriting file?
# - for now much easier to read in csv file, alter df and then rewrite file.



#%% 
# check if climb_id exists in climbs_df.csv
newattempt_data = {
    'climb_id': 22,
    'attempt_date':dt.date(2021, 1, 22).isoformat(),
    'success': False,
    }

# read first characters of each line in climbs_df.csv
with open(os.path.join(dirpath, 'climbs_df.csv'), 'r') as file:
    climb_ids = [line.split(',')[0] for line in file.readlines()]

# this one is slightly faster
climb_ids =  []
with open(os.path.join(dirpath, 'climbs_df.csv'), 'r') as file:
    next(file) # skip header line
    for line in file:
        climb_ids.append(int(line.split(',')[0]))



if newattempt_data['climb_id'] not in climb_ids:
    raise Exception(f"climb_id {newattempt_data['climb_id']} is not in existing climbs. Create climb ")
    # append new attempt

# assuming it is an existing climb: need to update aggregate_df.csv for this climb.

# first append new attempt to attempts_df.csv - safer to append and read in rather than read in, append and rewrite whole CSV
add_new_attempt_to_file(os.path.join(dirpath, 'attempts_df.csv'), newattempt_data)

# now read in updated attempts_df.csv
attempts_df_updated = pd.read_csv(os.path.join(dirpath, 'attempts_df.csv'), header=0,\
                 index_col=None, dtype=None, engine=None, converters=None,\
                 skipinitialspace=True, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True,\
                 na_filter=True, parse_dates=['attempt_date'],\
                 date_format='%Y-%m-%d', dayfirst=False, comment='#')

attempts_on_this_climbid = attempts_df_updated.groupby('climb_id').get_group(newattempt_data['climb_id']) # selects all attempts on this climb_id

first_attempt = attempts_on_this_climbid['attempt_date'].min() # finds first attempt date for each climb_id group
latest_attempt = attempts_on_this_climbid['attempt_date'].max() # finds latest attempt date for each climb_id group
sent_status = attempts_on_this_climbid['success'].any() # checks if success column has any trues for each climb_id group
total_number_attempts = attempts_on_this_climbid.shape[0]
if sent_status:
    first_send = attempts_on_this_climbid[attempts_on_this_climbid['success'] == True]['attempt_date'].min()
    attempts_to_send = attempts_on_this_climbid[attempts_on_this_climbid['attempt_date'] <= first_send].shape[0]
else:
    first_send = None
    attempts_to_send = None

updated_aggregate_data = {
    # 'climb_id' : newattempt_data['climb_id'],
    'first_attempt_date': first_attempt,
    'latest_attempt_date': latest_attempt,
    'sent_status': sent_status,
    'total_number_attempts': total_number_attempts,
    'first_send_date': first_send,
    'attempts_to_send': attempts_to_send,
}
# if reading to str, first_attempt.date().isoformat()
line_replace = ','.join(map(str, updated_aggregate_data.values()))

agg_df_read = pd.read_csv(os.path.join(dirpath, 'aggregate_df.csv'), header=0,\
                 index_col=0, dtype=None, engine=None, converters=None,\
                 skipinitialspace=True, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True,\
                 na_filter=True, parse_dates=['first_attempt_date', 'latest_attempt_date', 'first_send_date'],\
                 date_format='%Y-%m-%d', dayfirst=False, comment='#')

# update row of climb_id
agg_df_read.loc[newattempt_data['climb_id']] = updated_aggregate_data.values()
# rewrite aggregate_df.csv file
agg_df_read.to_csv(os.path.join(dirpath, 'aggregate_df.csv'), sep=',', na_rep='NaN', float_format=None, columns=None, header=True, index=True,\
                index_label=None, mode='w', date_format='%Y-%m-%d', doublequote=True, escapechar=None,\
                decimal='.')


#%% 
# add multiple attempts at once (on different climbs)
dirpath = os.path.join(os.getcwd(), 'sample_data')
filepath = os.path.join(dirpath, 'attempts_df.csv')

attempt_file_columns = add_new_attempt_function.attempt_file_columns

num_attempts = 3
newattempts_data = {'climb_id': [33,22,1],
                    'attempt_date': [dt.date(2021, 1, 22).isoformat(), dt.date(2021, 1, 23).isoformat(), dt.date(2021, 1, 24).isoformat()],
                    'success': [False, False, True],
                    }



if not isinstance(newattempts_data, dict):
    raise TypeError(f'Expected dict of attempt data, got {type(newattempts_data)}')
if not all([x in newattempts_data.keys() for x in attempt_file_columns]):
    raise KeyError(f'Expected dict of attempt data with keys {attempt_file_columns[1:]}, got {newattempts_data.keys()}')
if not all([len(v)==num_attempts for v in newattempts_data.values()]):
    raise ValueError(f'Expected dict values to be lists of length {num_attempts}, got {[len(value) for value in newattempts_data]}')

# Check that csv file ends with new line
with open(filepath, 'rb') as f:
    try:  # catch OSError in case of a one line file 
        f.seek(-2, os.SEEK_END)
        while f.read(1)!= b'\n':
            f.seek(-2, os.SEEK_CUR)
    except OSError:
        f.seek(0)
    last_line = f.readline().decode()
if last_line[:-2:-1]!= '\n':
    raise Exception(f'File {filepath} does not end with a new line.')

# Create a new dictionary for each new attempt...
# Not sure how efficient this will be for large number of attempts.
# Might be better to use csv.writer instead? and just make strings for each line.
indiv_attempts = []
for i in range(num_attempts):
    indiv_attempts.append({})
    for k, v in newattempts_data.items():
        indiv_attempts[i].update({k: v[i]})

try:
    with open(filepath, 'a', newline = '') as file:
        dictwriter = csv.DictWriter(file, fieldnames=attempt_file_columns, restval = '', extrasaction = 'raise') 
        for attempt in indiv_attempts:
            dictwriter.writerow(attempt)
    print("New lines appended successfully to {filepath}.")
except Exception as e:
    print(f"Error appending new line to {filepath}: {str(e)}")

#%%
# add multiple attempts on same day on same climb, NO SEND

dirpath = os.path.join(os.getcwd(), 'sample_data')
filepath = os.path.join(dirpath, 'attempts_df.csv')

attempt_file_columns = add_new_attempt_function.attempt_file_columns

num_attempts = 3
climb_id = 17
attempt_date = dt.date(2021, 1, 22).isoformat()

# Check that csv file ends with new line
with open(filepath, 'rb') as f:
    try:  # catch OSError in case of a one line file 
        f.seek(-2, os.SEEK_END)
        while f.read(1)!= b'\n':
            f.seek(-2, os.SEEK_CUR)
    except OSError:
        f.seek(0)
    last_line = f.readline().decode()
if last_line[:-2:-1]!= '\n':
    raise Exception(f'File {filepath} does not end with a new line.')

# appending exactly the same line num_attempts times
# so only need to create one dictionary
newattempt_data = {'climb_id': climb_id,
                    'attempt_date': attempt_date,
                    'success': False, # all False as this is for NO SEND
                    }
try:
    with open(filepath, 'a', newline = '') as file:
        dictwriter = csv.DictWriter(file, fieldnames=attempt_file_columns, restval = '', extrasaction = 'raise') 
        for i in range(num_attempts):
            dictwriter.writerow(newattempt_data)
    print("New lines appended successfully to {filepath}.")
except Exception as e:
    print(f"Error appending new line to {filepath}: {str(e)}")

#%%
# add multiple attempts on same day on same climb, SEND FINAL TRY
dirpath = os.path.join(os.getcwd(), 'sample_data')
filepath = os.path.join(dirpath, 'attempts_df.csv')

attempt_file_columns = add_new_attempt_function.attempt_file_columns

num_attempts = 1
climb_id = 17
attempt_date = dt.date(2021, 1, 22).isoformat()

if num_attempts < 1:
    raise ValueError(f'Expected num_attempts to be at least 1, got {num_attempts}')
# Check that csv file ends with new line
with open(filepath, 'rb') as f:
    try:  # catch OSError in case of a one line file 
        f.seek(-2, os.SEEK_END)
        while f.read(1)!= b'\n':
            f.seek(-2, os.SEEK_CUR)
    except OSError:
        f.seek(0)
    last_line = f.readline().decode()
if last_line[:-2:-1]!= '\n':
    raise Exception(f'File {filepath} does not end with a new line.')

# appending exactly the same line num_attempts times
# so only need to create one dictionary
newattempt_data = {'climb_id': climb_id,
                    'attempt_date': attempt_date,
                    'success': False, # first N-1 are False
                    }

try:
    with open(filepath, 'a', newline = '') as file:
        dictwriter = csv.DictWriter(file, fieldnames=attempt_file_columns, restval = '', extrasaction = 'raise')
        for i in range(num_attempts-1): # if num_attempts==1, this for loop won't be executed
            dictwriter.writerow(newattempt_data)
        newattempt_data['success'] = True # send/success on final try
        dictwriter.writerow(newattempt_data)
    print(f"New lines appended successfully to {filepath}.")
except Exception as e:
    print(f"Error appending new line to {filepath}: {str(e)}")

#%%
# testing functions
dirpath = os.path.join(os.getcwd(), 'sample_data')
filepath = os.path.join(dirpath, 'attempts_df.csv')

num_attempts = 2
climb_id = 18
attempt_date = dt.date(2022, 1, 22)

add_new_attempt_function.add_N_failed_attempts_on_one_climb_same_date(filepath, climb_id, attempt_date, num_attempts)
add_new_attempt_function.add_N_attempts_send_final_try_on_one_climb_same_date(filepath, climb_id, attempt_date, num_attempts)