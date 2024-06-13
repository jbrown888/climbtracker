# -*- coding: utf-8 -*-
"""
@author: jbrown888
7/6/24
#cwd = D:\\j_Documents\\cliimbing\\
# generate random sample climb data, full options
# generate_save_data.py previous testing file
"""


import pandas as pd
import numpy as np
import datetime as dt
import os


np.random.seed(0)
# Define possible climb styles, grades, doors, and locations
climb_styles = ['bouldering', 'sport', 'moonboard']
# grades = [] # any string that matches the regex options
doors = ['indoor', 'outdoor']
# locations = [] # any string eg 'Rockover', 'Summit Up', 'Curbar Edge', 'Devils Gorge', 'Burbage'
ropes = ['lead', 'toprope', 'autobelay', 'trad']
# climb_names = [] # any string, may include numbers
angles = ['40deg', '25deg'] # integers, for moonboard angles
mbyears = ['2016', '2017', '2019'] # moonboard year - 4digit str 0000
holds = ['compression', 'crimps', 'crack', 'features', 'jug', 'pinch', 'pocket', 'sidepull', 'sloper', 'undercling', 'volume']
walls = ['arete', 'barrel', 'chimney', 'corner', 'overhang', 'roof', 'slab', 'step', 'topout', 'traverse', 'vert']
skills = ['dyno', 'finger', 'power', 'reachy', 'sustained', 'technical', 'balance', 'co-ordination', 'paddle']
font_grades_letters = ['a','b','c', 'a+', 'b+', 'c+']
gymlocations = ['Rockover', 'Summit Up', 'Big Depot', 'Parthian']
craglocations = ['Curbar Edge', 'Devils Gorge', 'Burbage']

num_climbs = 100
climb_data = {
    #dictionary of lists length num_climbs of randomly selected values
    'climb_style': np.random.choice(climb_styles, num_climbs),
}

# initialise empty arrays type <U10
climb_names_ = np.empty((num_climbs), dtype='<U10')
grades_ = np.empty((num_climbs), dtype='<U10')
locations_ = np.empty((num_climbs), dtype='<U64')
doors_ = np.empty((num_climbs), dtype='<U10')
ropes_ = np.empty((num_climbs), dtype='<U10')
angles_ = np.empty((num_climbs), dtype='<U10')
mbyears_ = np.empty((num_climbs), dtype='<U10')

# decide further values dep on climbstyle
for i, climbstyle in enumerate(climb_data['climb_style']): 
    if climbstyle == 'bouldering':
        mbyears_[i] = None
        angles_[i] = None
        ropes_[i] = None
        doors_[i] = np.random.choice(doors, 1)[0]
        if doors_[i] == 'indoor':
            # indoor bouldering
            locations_[i] = np.random.choice(gymlocations, 1)[0]
            climb_names_[i] = None
            if bool(np.random.randint(2)):
                # start grade B
                lower_grade = 'B'
                upper_grade = np.random.randint(3)
            else:
                lower_grade = np.random.randint(15)
                upper_grade = lower_grade + np.random.randint(1,4)
            grades_[i] = f'V{str(lower_grade):s}-{str(upper_grade):s}'
        else:
            # outdoor bouldering
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
            # indoor rope
            locations_[i] = np.random.choice(gymlocations, 1)[0]
            ropes_[i] = np.random.choice(['lead', 'toprope', 'autobelay'], 1)[0]
            climb_names_[i] = None
        else:
            # outdoor rope
            locations_[i] = np.random.choice(craglocations, 1)[0]
            ropes_[i] = np.random.choice(['lead', 'toprope', 'trad'], 1)[0]
            climb_names_[i] = 'some climb name'

climb_data.update({'grade': grades_,
                   'door': doors_,
                   'location': locations_,
                   'rope': ropes_,
                   'climb_name': climb_names_,
                   'angle': angles_,
                   'mbyear': mbyears_,
                   'hold': np.random.choice(holds, num_climbs), 
                   'wall': np.random.choice(walls, num_climbs),
                   'skill': np.random.choice(skills, num_climbs),
                   'notes': np.full((num_climbs), 'notes on climb\,hhg', dtype='<U100')
                   }
                )
climbs_df = pd.DataFrame(climb_data)


dirpath = os.path.join(os.getcwd(), 'sample_data')
fname = 'sample_climbs.csv'
fpath = os.path.join(dirpath, fname)
overwritefile = True
if overwritefile:
    climbs_df.to_csv(fpath, sep=',', na_rep='NaN', float_format=None, columns=None, header=True, index=True,\
                  index_label='climb_id', mode='w', encoding=None, compression='infer',\
                  date_format='YYYY-MM-DD', doublequote=True, escapechar='\\',\
                  decimal='.')
else:
    try:
        climbs_df.to_csv(fpath, sep=',', na_rep='NaN', float_format=None, columns=None, header=True, index=True,\
                    index_label='climb_id', mode='x', encoding=None, compression='infer',\
                    date_format='YYYY-MM-DD', doublequote=True, escapechar='\\',\
                    decimal='.')
    except FileExistsError:
        print("File 'climbs_df.csv' already exists. Please choose a different file name or delete the existing file.")


# Notes: there are DEFINITELY some dtype issues here.
# especially with None/NaN values...need more consistency.
# Also escaping commas - need to make sure this will work and not cause issues
