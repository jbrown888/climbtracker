# -*- coding: utf-8 -*-
"""
@author: jbrown888
8/6/24
#cwd = D:\\j_Documents\\cliimbing\\
File for testing out code for adding climb data to climbs file
"""

# appending climb_df file

import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.dates as mdate
import itertools
from importlib import reload
import csv 
import add_new_climb_functions

#%%
# Append a new line to climbs_df.csv - testing methods.

dirpath = os.path.join(os.getcwd(), 'sample_data')
# climbs_df.to_csv(os.path.join(dirpath, 'climbs_df.csv'), sep=',', na_rep='NaN', float_format=None, columns=None, header=True, index=True,\
#                 index_label='climb_id', mode='x', encoding=None, compression='infer',\
#                 date_format='YYYY-MM-DD', doublequote=True, escapechar=None,\
#                 decimal='.')

# Three options: with pandas, simple print string, or use csv module

# Option 1 with pandas
# Assuming you have a new climb data dictionary
new_id = 100
newclimb_data = {
    # 'climb_id': new_id,
    'climb_style': 'bouldering',
    'grade': 'f6a',
    'door': 'indoor', 
    'location': 'Crag 2'
}
newclimb_df = pd.DataFrame(newclimb_data, index=[new_id])
# Append the new DataFrame to the existing climbs_df.csv
try:
    newclimb_df.to_csv(os.path.join(dirpath, 'climbs_df.csv'), mode='a', header=False)
    print("New line appended successfully to 'climbs_df.csv'.")
except Exception as e:
    print(f"Error appending new line to 'climbs_df.csv': {str(e)}")
# timeit: 2.62ms

# Option 2 without pandas
# Convert the dictionary to a CSV string
new_id+=1
newclimb_data_= {'climb_id': new_id} # have to recreate dictionary to put climb_id at the start
newclimb_data_.update(newclimb_data) # add all other elements of newclimb_data to new_climb_data_
newclimb_line = ','.join(map(str, newclimb_data_.values()))
# Append the new line to the existing climbs_df.csv
try:
    with open(os.path.join(dirpath, 'climbs_df.csv'), 'a', newline='') as file:
        file.write(newclimb_line + '\n')
    print("New line appended successfully to 'climbs_df.csv'.")
except Exception as e:
    print(f"Error appending new line to 'climbs_df.csv': {str(e)}")
# timeit: 1.1ms

# Option 3 without pandas, using csv module
new_id+=1
newclimb_data_['climb_id'] = new_id
try:
    with open(os.path.join(dirpath, 'climbs_df.csv'), 'a', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow([*newclimb_data_.values()]) # writerow argument should be list of strings 

        # OR 
        dictwriter = csv.DictWriter(file, fieldnames=['climb_id', 'climb_style', 'grade', 'door', 'location']) 
        # Create an object which operates like a regular writer but maps dictionaries onto output rows
        # fieldnames identifies order in which dict values are passed to writerow() method. Useful if dict in wrong order!
        # restval = '' specifies value to write if dict is missing key in fieldnames
        # extrasaction says what to do if dict passed to writerow() key(s) not in fieldnames. if raise, ValueError, if ignore, ignore
        dictwriter.writerow(newclimb_data_)
    print("New line appended successfully to 'climbs_df.csv'.")
except Exception as e:
    print(f"Error appending new line to 'climbs_df.csv': {str(e)}")
# time it with csv.writer 1.05ms
# time it with csv.DictWriter 965microseconds

# all these methods work! added lines seemingly indistinguishable from other lines when file is read in
# importantly the new indexs are dtype int64

# Dictwriter method is significantly faster and provides a lot of functionality. let's go with that.

#%%
# Append to climbs_df.csv file
with open(os.path.join(dirpath, 'climbs_df.csv'), 'r', newline = '') as file:
    row_count = sum(1 for row in file)
# this is useful, but not guaranteed that the climb_ids are exactly sequential - some may be skipped so nrows!=next index.
# need to read last line of csv file to get the last climb_id
# as potentially large files, don't want to read entire file

# from stack overflow, nice and efficient!
# https://stackoverflow.com/questions/3346430/what-is-the-most-efficient-way-to-get-first-and-last-line-of-a-text-file/18603065#18603065
# https://stackoverflow.com/questions/46258499/how-to-read-the-last-line-of-a-file-in-python
with open(os.path.join(dirpath, 'climbs_df.csv'), 'rb') as f:
    try:  # catch OSError in case of a one line file 
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
    except OSError:
        f.seek(0)
    last_line = f.readline().decode()
if last_line[:-2:-1] != '\n':
    raise Exception(f'File {os.path.join(dirpath, "climbs_df.csv")} does not end with a new line.')

new_id = int(last_line.split(',')[0]) + 1

newclimb_data = {
    'climb_id': new_id,
    'climb_style': 'bouldering',
    'grade': 'f6a',
    'door': 'indoor', 
    'location': 'Crag 2'
}
try:
    with open(os.path.join(dirpath, 'climbs_df.csv'), 'a', newline = '') as file:
        dictwriter = csv.DictWriter(file, fieldnames=['climb_id', 'climb_style', 'grade', 'door', 'location'], restval = '', extrasaction = 'raise') 
        dictwriter.writerow(newclimb_data)
    print("New line appended successfully to 'climbs_df.csv'.")
except Exception as e:
    print(f"Error appending new line to 'climbs_df.csv': {str(e)}")

#%% 
# Import from csv

climbs_df_read = pd.read_csv(os.path.join(dirpath, 'climbs_df.csv'), header=0,\
                 index_col =0, dtype=None, engine=None, converters=None,\
                 skipinitialspace=True, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True,\
                 na_filter=True, parse_dates=None, comment='#')

# woo!
#%% Add style of climb
# for updated fullinfo climbs (generate_sample_climbs.py)

file_columns = ['climb_id','climb_style', 'grade', 'door', 'location', 'rope', 'climb_name', 'angle', 'mbyear','hold', 'wall', 'skill', 'notes']


dirpath = os.path.join(os.getcwd(), 'sample_data')
fname = 'sample_climbs.csv'
fpath = os.path.join(dirpath, fname)

with open(fpath, 'rb') as f:
    try:  # catch OSError in case of a one line file 
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
    except OSError:
        f.seek(0)
    last_line = f.readline().decode()
if last_line[:-2:-1] != '\n':
    raise Exception(f'File {fpath} does not end with a new line.')

new_id = int(last_line.split(',')[0]) + 1

newclimb_data = {
    'climb_id': new_id,
    'climb_style': 'bouldering',
    'grade': 'f6c+',
    'door': 'outdoor', 
    'location': 'Burbage',
    'rope': 'None',
    'climb_name': 'some_climb',
    'angle': 'None',
    'mbyear': 'None',
    'hold': 'crimps',
    'wall': 'roof',
    'skill': 'finger',
    'notes': 'notes',
}

try:
    with open(fpath, 'a', newline = '') as file:
        dictwriter = csv.DictWriter(file, fieldnames=file_columns, restval = '', extrasaction = 'raise') 
        dictwriter.writerow(newclimb_data)
    print(f"New line appended successfully to {fname}.")
except Exception as e:
    print(f"Error appending new line to {fname}: {str(e)}")


#%%
dirpath = os.path.join(os.getcwd(), 'sample_data')
fname = 'sample_climbs.csv'
fpath = os.path.join(dirpath, fname)

reload(add_new_climb_functions)
newclimb_data = {
    'climb_style': 'bouldering',
    'grade': 'f6c+',
    'door': 'outdoor', 
    'location': 'Burbage',
    'rope': 'None',
    'climb_name': 'some_climb',
    'angle': 'None',
    'mbyear': 'None',
    'hold': 'crimps',
    'wall': 'arete',
    'skill': 'finger',
    'notes': 'notes',
}

add_new_climb_functions.add_new_climb_to_file(fpath, newclimb_data)