# -*- coding: utf-8 -*-
"""
@author: jbrown888
8/6/24
#cwd = D:\\j_Documents\\cliimbing\\climbtracker
# working and tested functions for adding to climbs data file
# superseded by broomcupboard on 24/6/24
"""

# appending climb_df file
import datetime as dt
import os
import csv 
import pandas as pd
import re
import copy

# Possible climb attributes
climb_styles = ['bouldering', 'sport', 'moonboard']
grades = [] # any string that matches the regex options
doors = ['indoor', 'outdoor']
locations = [] # any string eg 'Rockover', 'Summit Up', 'Curbar Edge', 'Devils Gorge', 'Burbage'
ropes = ['lead', 'toprope', 'autobelay', 'trad']
climb_names = [] # any string, may include numbers
angles = ['25deg', '40deg'] # integers, for moonboard angles
mbyears = ['2016', '2017', '2019'] # moonboard year - 4digit str 0000
holds = ['compression', 'crimps', 'crack', 'features', 'jug', 'pinch', 'pocket', 'sidepull', 'sloper', 'undercling', 'volume']
walls = ['arete', 'barrel', 'chimney', 'corner', 'overhang', 'roof', 'slab', 'step', 'topout', 'traverse', 'vert']
skills = ['dyno', 'finger', 'power', 'reachy', 'sustained', 'technical', 'balance', 'co-ordination', 'paddle']

# https://pythex.org/
Vgrades_regex_pattern = r'^V([0-9]|[1-9][0-9]|B)[+]?$'
Vgrades_range_regex_pattern = r'^V([0-9]|[1-9][0-9]|B)[+]?-((?!\1)[0-9]|[1-9][0-9])[+]?$' 
# can't compare values with regex. have to check afterwards
font_grades_regex_pattern = r'^f([0-9]|[1-9][0-9])[a-c]?[+]?$'
# check grade matches one of these patterns

# equivalent font and V grades dictionary
# font to V grade
font_to_V = {'f3': ['VB'],
             'f3+': ['V0'],
             'f4': ['V0'],
             'f4+': ['V0'],
             'f5': ['V0','V1'],
             'f5+': ['V1','V2'],
             'f6a': ['V2'],
             'f6a+': ['V3'],
             'f6b': ['V4'],
             'f6b+': ['V4'],
             'f6c': ['V5'],
             'f6c+': ['V5', 'V6'],
             'f7a': ['V6'],
             'f7a+': ['V7'],
             'f7b': ['V8'],
             'f7b+': ['V8', 'V9'],
             'f7c': ['V9'],
             'f7c+': ['V10'],
             'f8a': ['V11'],
             'f8a+': ['V12'],
             'f8b': ['V13'],
             'f8b+': ['V14'],
             'f8c': ['V15'],
        }

V_to_font = {'VB':['f3'],
             'V0': ['f3+', 'f4', 'f4+'],
             'V1': ['f5', 'f5+'],
             'V2': ['f5+', 'f6a'],
             'V3': ['f6a+'],
             'V4': ['f6b', 'f6b+'],
             'V5': ['f6c', 'f6c+'],
             'V6': ['f6c+', 'f7a'],
             'V7': ['f7a+'],
             'V8': ['f7b', 'f7b+'],
             'V9': ['f7b+', 'f7c'],
             'V10': ['f7c+'],
             'V11': ['f8a'],
             'V12': ['f8a+'],
             'V13': ['f8b'],
             'V14': ['f8b+'],
             'V15': ['f8c'],
        }

def get_equivalent_grades(grades):
     """
     This function takes a list of climbing grades in either V-grade or font-grade format,
     and returns a new list of equivalent grades in the other format.

     Parameters:
     grades (list): A list of strings representing climbing grades. 
     Each grade should be in either V-grade or font-grade format.

     Returns:
     list: A new list of strings representing equivalent grades in the other format.

     Raises:
     TypeError: If the input grades is not a list.
     ValueError: If any of the grades are not in either V-grade or font-grade format.

     Note:
     The function uses regular expressions to match the grade format.
     It then adds equivalent grades to the result list based on the matching format.
     """
     if not isinstance(grades, list):
          raise TypeError(f'Expected list of strings of grades, got {type(grades)}')
     equiv_grades = []
     for g in grades:
          if re.match(Vgrades_regex_pattern, g):
               equiv_grades +=  V_to_font[g]
          elif re.match(font_grades_regex_pattern, g):
               equiv_grades += font_to_V[g]
          else: 
               raise ValueError(f'Invalid grade format: {g}')

     return equiv_grades


def append_equivalent_grades(grades):
     """
     This function takes a list of climbing grades in either V-grade or font-grade format,
     and appends equivalent grades in the other format to the original list in-place.

     Parameters:
     grades (list): A list of strings representing climbing grades. 
     Each grade should be in either V-grade or font-grade format.

     Returns:
     int: 0 if the function executes successfully, otherwise an error code.

     Raises:
     TypeError: If the input grades is not a list.
     ValueError: If any of the grades are not in either V-grade or font format.
     Note:
     The function uses regular expressions to match the grade format.
     It then adds equivalent grades to the original list based on the matching format.
     A deep copy of the input list is iterated over.
     """
     if not isinstance(grades, list):
          raise TypeError(f'Expected list of strings of grades, got {type(grades)}')
     gs = copy.deepcopy(grades)
     for g in gs: # ensure don't end up in endless loop of adding grades to original list
          if re.match(Vgrades_regex_pattern, g):
               grades += V_to_font[g]               
          elif re.match(font_grades_regex_pattern, g):
               grades += font_to_V[g]      
          else:
               raise ValueError(f'Invalid grade format: {g}')         
     return 0

def get_grades_in_range(grade_range):
     """
     This function returns a list of V-grades within a given range.

     Parameters:
     grade_range (str): A string representing a range of V-grades in the format 'V[lower]-[upper]'.
          The lower and upper bounds can be integers or 'B' for V0 and '8+' for V9.
          For example, 'VB-8', 'V3-6', 'V1-8+', 'VB-8+' are valid inputs.

     Returns:
     list: A list of strings representing V-grades within the given range.
          The grades are in the format 'V[grade]'.
          For example, for the input 'VB-V2', the output would be ['VB', 'V0', 'V1', 'V2'].

     Raises:
     ValueError: If the grade_range is not in the correct format or if the lower grade is greater than or equal to the upper grade.

     """
     if not re.match(Vgrades_range_regex_pattern, grade_range):
          raise ValueError(f'Invalid grade range format: {grade_range}')
     
     lower_grade = grade_range.split('-')[0][1:]
     upper_grade = grade_range.split('-')[1]
     if lower_grade == 'B':
          # assume unlikely input of VB-8+, so can treat as separate cases
          incl_grades = ['B'] + list(range(int(upper_grade)+1))
     elif upper_grade == '8+':
          incl_grades = list(range(int(lower_grade), 10)) # assume 8+ includes 8,9
     else:
          if int(lower_grade) >= int(upper_grade):
               raise ValueError(f'Lower grade {lower_grade} must be less than upper grade {upper_grade}')
          incl_grades = list(range(int(lower_grade), int(upper_grade)+1))

     return [f'V{grade}' for grade in incl_grades]




climb_file_columns = ['climb_id','climb_style', 'grade', 'door', 'location', 'rope', 'climb_name', 'angle', 'mbyear','hold', 'wall', 'skill', 'notes']
def add_new_climb_to_file(filepath, newclimb_data):
     """
     This function adds a new climb as line of data to a CSV file.

     Parameters:
     filepath (str): The path to the CSV file where the new climb data will be appended.
     newclimb_data (dict): A dictionary containing the new climb data. The keys should match the column names in the CSV file.

     Returns:
     int: 0 if the function executes successfully, otherwise an error code.

     Raises:
     TypeError: If the newclimb_data is not a dictionary.
     KeyError: If the newclimb_data dictionary does not contain all the required keys.
     Exception: If the file does not end with a new line.

     Note:
     The function reads the last line of the file to get the previous climb_id and increments it to generate the new climb_id.
     The new climb data is then appended to the file using the csv.DictWriter.
     """
     if not isinstance(newclimb_data, dict):
          raise TypeError(f'Expected dict of climb data, got {type(newclimb_data)}')
     if not all([x in newclimb_data for x in climb_file_columns[1:]]):
          raise KeyError(f'Expected dict of climb data with keys {climb_file_columns[1:]}, got {newclimb_data.keys()}')

     # get previous climb_id from last line of file
     with open(filepath, 'rb') as f:
          try:  # catch OSError in case of a one line file 
               f.seek(-2, os.SEEK_END)
               while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
          except OSError:
               f.seek(0)
          last_line = f.readline().decode()
     if last_line[:-2:-1] != '\n':
          raise Exception(f'File {filepath} does not end with a new line.') # poorly formatted file
     new_id = int(last_line.split(',')[0]) + 1

     newclimb_data.update({'climb_id': new_id}) # doesn't matter that this is added to the end of the dictionary
     # since fieldnames param in dictwriter writerow sets order of keys to write into file
     # append data to file
     try:
          with open(filepath, 'a', newline = '') as file:
               dictwriter = csv.DictWriter(file, fieldnames=climb_file_columns, restval = '', extrasaction = 'raise')
               dictwriter.writerow(newclimb_data)
          print(f"New line appended successfully to {filepath}.")
     except Exception as e:
          print(f"Error appending new line to {filepath}: {str(e)}")

     return 0