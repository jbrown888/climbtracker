# -*- coding: utf-8 -*-
"""
@author: jnb19
7/6/24
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

#Aggregate data:
first_attempts = attempts_grouped_climbid['attempt_date'].apply(lambda x: x.min()) # finds first attempt date for each climb_id group
latest_attempts = attempts_grouped_climbid['attempt_date'].apply(lambda x: x.max()) # finds latest attempt date for each climb_id group
sent_statuses = attempts_grouped_climbid['success'].apply(lambda x: x.any()) # checks if success column has any trues for each climb_id group
total_number_attempts = attempts_grouped_climbid.size()
first_sends = attempts_grouped_climbid.apply(lambda x: x[x["success"]==True]['attempt_date'].min() if x["success"].any() else None, include_groups=False)
attempts_to_send = attempts_grouped_climbid.apply(lambda x: x[x['attempt_date'] <= x[x['success']==True]['attempt_date'].min()].shape[0] if x['success'].any() else None, include_groups=False)

aggregate_data = {
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



#%% 
# Save data to file, export

dirpath = os.path.join(os.getcwd(), 'sample_data')
try:
    climbs_df.to_csv(os.path.join(dirpath, 'climbs_df.csv'), sep=',', na_rep='NaN', float_format=None, columns=None, header=True, index=True,\
                  index_label='climb_id', mode='x', encoding=None, compression='infer',\
                  date_format='YYYY-MM-DD', doublequote=True, escapechar=None,\
                  decimal='.')
except FileExistsError:
    print("File 'climbs_df.csv' already exists. Please choose a different file name or delete the existing file.")


# attempts_df['date'] = attempts_df['attempt_date'].dt.date
try:
    attempts_df.to_csv(os.path.join(dirpath, 'attempts_df.csv'), sep=',', na_rep='NaN', float_format=None, columns=None, header=True, index=False,\
                  index_label=None, mode='x', date_format='%Y-%m-%d', doublequote=True, escapechar=None,\
                  decimal='.')
    # don't need to save index for attempts_df as when read_csv will be added anyway
except FileExistsError:
    print("File 'attempts_df.csv' already exists. Please choose a different file name or delete the existing file.")

try:
    agg_df.to_csv(os.path.join(dirpath, 'aggregate_df.csv'), sep=',', na_rep='NaN', float_format=None, columns=None, header=True, index=True,\
                  index_label=None, mode='x', date_format='%Y-%m-%d', doublequote=True, escapechar=None,\
                  decimal='.')
except FileExistsError:
    print("File 'attempts_df.csv' already exists. Please choose a different file name or delete the existing file.")



# %s gives 2021-01-22 00:00:00 format
# '%Y-%m-%d' gives 2021-01-22 00:00:00 format. how to save only date? have to convert to date before saving to csv
# not sure whether or not this actually saves any space. check later? 18kb (no times) vs 12kb (with times). as is then lol.


# f = open('H:\\User\\Documents\\DataAnalysis\\Fitting_dingle_offset.txt', 'a')
# stringlist = [X._formula, scanno, X.capacitance_used, wl, offset, MinOe, MaxOe, *Dpopt_peaks, *Stderr_peaks, *Dpopt_troughs, *Stderr_troughs, step, bool(sigma)]
# string = ', '.join(map(str, stringlist))+ '\n'
# f.write(string)
# f.close()

#%% 
# Import from csv

# df = pd.read_excel(excel_file, sheet_name = 'indiv_files', header=[0], dtype = bc.dtypedict,\
#  converters={'Scan Number': '{:0>4}'.format,'Month': '{:0>2}'.format,'Year': str , 'Skiprows':bool})

climbs_df_read = pd.read_csv(os.path.join(dirpath, 'climbs_df.csv'), header=0,\
                 index_col =0, dtype=None, engine=None, converters=None,\
                 skipinitialspace=True, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True,\
                 na_filter=True, parse_dates=None, comment='#')

attempts_df_read = pd.read_csv(os.path.join(dirpath, 'attempts_df.csv'), header=0,\
                 index_col=None, dtype=None, engine=None, converters=None,\
                 skipinitialspace=True, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True,\
                 na_filter=True, parse_dates=['attempt_date'],\
                 date_format='%Y-%m-%d', dayfirst=False, comment='#')

agg_df_read = pd.read_csv(os.path.join(dirpath, 'aggregate_df.csv'), header=0,\
                 index_col=0, dtype=None, engine=None, converters=None,\
                 skipinitialspace=True, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True,\
                 na_filter=True, parse_dates=['first_attempt_date', 'latest_attempt_date', 'first_send_date'],\
                 date_format='%Y-%m-%d', dayfirst=False, comment='#')

# woo!

#%% 
# updated generate climbs_df with full information ie actual climbs
np.random.seed(0)
# Define climb styles, grades, doors, and locations
climb_styles = ['bouldering', 'sport', 'moonboard']
grades = [] # any string that matches the regex options
doors = ['indoor', 'outdoor']
locations = [] # any string eg 'Rockover', 'Summit Up', 'Curbar Edge', 'Devils Gorge', 'Burbage'
ropes = ['lead', 'toprope', 'autobelay', 'trad']
climb_names = [] # any string, may include numbers
angles = ['40deg', '25deg'] # integers, for moonboard angles
mbyears = ['2016', '2017', '2019'] # moonboard year - 4digit str 0000
holds = ['compression', 'crimps', 'crack', 'features', 'jug', 'pinch', 'pocket', 'sidepull', 'sloper', 'undercling', 'volume']
walls = ['arete', 'barrel', 'chimney', 'corner', 'overhang', 'roof', 'slab', 'step', 'topout', 'traverse', 'vert']
skills = ['dyno', 'finger', 'power', 'reachy', 'sustained', 'technical', 'balance', 'co-ordination']
font_grades_letters = ['a','b','c', 'a+', 'b+', 'c+']

gymlocations = ['Rockover', 'Summit Up', 'Big Depot', 'Parthian']
craglocations = ['Curbar Edge', 'Devils Gorge', 'Burbage']

# Generate random data for climbs and attempts
num_climbs = 100
climb_data = {
    #dictionary of lists length num_climbs of randomly selected values 
    #np.random.choice(list_to_selct_from, number to select) generates random sample from given 1d array
    'climb_style': np.random.choice(climb_styles, num_climbs),
}

climb_names_ = np.empty((num_climbs), dtype='<U10')
grades_ = np.empty((num_climbs), dtype='<U10')
locations_ = np.empty((num_climbs), dtype='<U10')
doors_ = np.empty((num_climbs), dtype='<U10')
ropes_ = np.empty((num_climbs), dtype='<U10')
angles_ = np.empty((num_climbs), dtype='<U10')
mbyears_ = np.empty((num_climbs), dtype='<U10')

for i, climbstyle in enumerate(climb_data['climb_style']): 
    if climbstyle == 'bouldering':
        mbyears_[i] = None
        angles_[i] = None
        ropes_[i] = None
        doors_[i] = np.random.choice(doors, 1)[0]
        if doors_[i] == 'indoor':
            locations_[i] = np.random.choice(gymlocations, 1)[0]
            climb_names_[i] = None
            if bool(np.random.randint(2)):
                lower_grade = 'B'
                upper_grade = np.random.randint(3)
            else:
                lower_grade = np.random.randint(15)
                upper_grade = lower_grade + np.random.randint(1,4)
            grades_[i] = f'V{str(lower_grade):s}-{str(upper_grade):s}'
        else:
            locations_[i] = np.random.choice(craglocations, 1)[0]
            climb_names_[i] = 'some climb name'
            grades_[i] = f'f{str(np.random.randint(3,13)):s}{np.random.choice(font_grades_letters, 1)[0]}'
    elif climbstyle == 'moonboard':
        mbyears_[i] = np.random.choice(mbyears, 1)[0]
        angles_[i] = np.random.choice(angles, 1)[0]
        doors_[i] = 'indoor'
        ropes_[i] = None
        locations_[i] = np.random.choice(gymlocations, 1)[0]
        grades_[i] = f'V{str(np.random.randint(2,15)):s}'
        climb_names_[i] = 'some climb name'
    else: # sport style
        mbyears_[i] = None
        angles_[i] = None
        doors_[i] = np.random.choice(doors, 1)[0]
        grades_[i] = f'f{str(np.random.randint(3,13)):s}{np.random.choice(font_grades_letters, 1)[0]}'
        if doors_[i] == 'indoor':
            locations_[i] = np.random.choice(gymlocations, 1)[0]
            ropes_[i] = np.random.choice(['lead', 'toprope', 'autobelay'], 1)[0]
            climb_names_[i] = None
        else:
            locations_[i] = np.random.choice(craglocations, 1)[0]
            ropes_[i] = np.random.choice(['lead', 'toprope', 'trad'], 1)[0]
            climb_names_[i] = 'some climb name'

climb_data.update({'grade': grades_,
                   'door': doors_,
                   'location': locations_,
                   'rope': ropes_,
                   'climb_name': climb_names_,
                   'angle': angles_,
                   'hold': np.random.choice(holds, num_climbs), 
                   'wall': np.random.choice(walls, num_climbs),
                   'skill': np.random.choice(skills, num_climbs)}
                )
