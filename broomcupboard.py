# -*- coding: utf-8 -*-
"""
@author: jbrown888
24/6/24
#cwd = D:\\j_Documents\\cliimbing\\climbtracker
# working and tested functions for all data processes.
"""

import datetime as dt
import os
import csv 
import pandas as pd
import re
import copy


# CLIMB INFORMATION #################################################################

# IMPORTANT! Titles of columns in climb data file
climb_file_columns = ['climb_id','climb_style', 'grade', 'door', 'location', 'rope', 'climb_name', 'angle', 'mbyear','hold', 'wall', 'skill', 'notes']

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

# Functions to find equivalent grades
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

# ALTERING CLIMBS FILE
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


# ATTEMPTS #########################################################################

# IMPORTANT! Titles of columns in attempt data file
attempt_file_columns = ['climb_id', 'attempt_date','success']

# Altering attempts data file
# add single new attempt
def add_new_attempt_to_file(filepath, newattempt_data):
    """
    This function appends a new attempt date (climb_id, date, success) to a csv file.

    Parameters:
    filepath (str): The path to the csv file where the data will be appended.
    newattempt_data (dict): A dictionary containing the data of the new attempt to be appended.
        Should have keys 'climb_id', 'attempt_date', and 'success'.

    Returns:
    0 if the function executes successfully, otherwise an error code.

    Raises:
    TypeError: If the newattempt_data is not a dictionary.
    ValueError: If the newattempt_data dictionary does not contain all the required keys.
    Exception: If the file to write to does not end with a new line.

    
    """
    if type(newattempt_data) is not dict:
        raise TypeError(f'Expected dict of attempt data, got {type(newattempt_data)}')
    if not all([x in newattempt_data for x in attempt_file_columns]):
        raise KeyError(f'Expected dict of attempt data with keys {attempt_file_columns[1:]}, got {newattempt_data.keys()}')

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

    try:
        with open(filepath, 'a', newline = '') as file:
            dictwriter = csv.DictWriter(file, fieldnames=attempt_file_columns, restval = '', extrasaction = 'raise') 
            dictwriter.writerow(newattempt_data)
        print(f"New line appended successfully to {filepath}.")
    except Exception as e:
        print(f"Error appending new line to {filepath}: {str(e)}")

    return 0

# add multiple new attempts from a dictionary
def add_new_attempts_to_file(filepath, newattempts_data, num_attempts):
    """
    This function appends a dictionary of new attempts (climb_id, date, success) to a csv file

    Parameters:
    filepath (str): The path to the csv file where the data will be appended.
    newattempts_data (dict): A dictionary containing the data of the new attempt.
        Should have keys 'climb_id', 'attempt_date', and 'success'.
    num_attempts (int): The number of attempts to add to the file.

    Returns:
    0 if the function executes successfully, otherwise an error code.

    Raises:
    TypeError: If the newattempts_data is not a dictionary.
    KeyError: If the newattempts_data dictionary does not contain all the required keys.
    ValueError: If the newattempts_data dictionary values are not lists of length num_attempts
    Exception: If the file to write to does not end with a new line.

    Notes: 
    This function does NOT assume that all attempts are on the same climb. 
    The climb_ids can be different for each attempt.
    Realistically not that useful a function
    """
    
    if type(newattempts_data) is not dict:
        raise TypeError(f'Expected dict of attempt data, got {type(newattempts_data)}')
    if not all([x in newattempts_data.keys() for x in attempt_file_columns]):
        raise KeyError(f'Expected dict of attempt data with keys {attempt_file_columns[1:]}, got {newattempts_data.keys()}')
    if not all([len(v)==num_attempts for v in newattempts_data.values()]):
        raise ValueError(f'Expected dict values to be lists of length {num_attempts}, got {[len(v) for v in newattempts_data]}')

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

    return 0

# add N failed attempts on same climb, same date, to file
def add_N_failed_attempts_on_one_climb_same_date(filepath, climb_id, attempt_date, num_attempts):
    """
    This function appends a number of failed attempts on the same date and climb to attempts data csv file.

    Parameters:
    filepath (str): The path to the csv file where the data will be appended.
    climb_id (int): The id of the climb for which the attempts are being added.
    attempt_date (datetime.date): The date of the attempts being added.
    num_attempts (int): The number of failed attempts to add to the file.

    Returns:
    0 if the function executes successfully, otherwise an error code.

    Raises:
    TypeError: If climb_id is not an integer, attempt_date is not a datetime.date or num_attempts is not an integer.
    ValueError: If attempt_date is in the future.
    ValueError: If num_attempts is less than 1.
    Exception: If the file to write to does not end with a new line.
    """

    if type(climb_id) is not int:
        raise TypeError(f'Expected int for climb_id, got {type(climb_id)}')
    if type(attempt_date) is not dt.date:
        # NOTE! this may not be a good idea. Might be better to read in as isoformat string and compare to regex pattern
        # tying it into numpy datetime format might not be a great idea for transferability...
        raise TypeError(f'Expected dt.date for attempt_date, got {type(attempt_date)}')
    if attempt_date > dt.date.today():
        raise ValueError("Attempt date cannot be in the future.")
    if type(num_attempts) is not int:
        raise TypeError(f'Expected int for num_attempts, got {type(num_attempts)}')
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

    return 0

# add N attempts with fail until final send on same climb, same date, to file
def add_N_attempts_send_final_try_on_one_climb_same_date(filepath, climb_id, attempt_date, num_attempts):
    """
    This function appends N-1 failed attempts and 1 successful attempt on the same date and climb to attempts data csv file.

    Parameters:
    filepath (str): The path to the csv file where the data will be appended.
    climb_id (int): The id of the climb for which the attempts are being added.
    attempt_date (datetime.date): The date of the attempts being added.
    num_attempts (int): The number of failed attempts to add to the file.

    Returns:
    0 if the function executes successfully, otherwise an error code.

    Raises:
    TypeError: If climb_id is not an integer, attempt_date is not a datetime.date or num_attempts is not an integer.
    ValueError: If attempt_date is in the future.
    ValueError: If num_attempts is less than 1.
    Exception: If the file to write to does not end with a new line.
    """

    if type(climb_id) is not int:
        raise TypeError(f'Expected int for climb_id, got {type(climb_id)}')
    if type(attempt_date) is not dt.date:
        # NOTE! this may not be a good idea. Might be better to read in as isoformat string and compare to regex pattern
        # tying it into numpy datetime format might not be a great idea for transferability...
        raise TypeError(f'Expected dt.date for attempt_date, got {type(attempt_date)}')
    if attempt_date > dt.date.today():
        raise ValueError("Attempt date cannot be in the future.")
    if type(num_attempts) is not int:
        raise TypeError(f'Expected int for num_attempts, got {type(num_attempts)}')
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

    # appending exactly the same line N-1 times
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
        print("New lines appended successfully to {filepath}.")
    except Exception as e:
        print(f"Error appending new line to {filepath}: {str(e)}")

    return 0

# check if a given climb id exists already in climb data
def check_climb_id_exists(climbs_filepath, climb_id):
    """
    This function checks if a given climb_id exists in a csv file containing climbs data

    Parameters:
    climbs_filepath (str): The path to the csv file containing climb data.
    climb_id (int): The climb_id to check for existence.

    Returns:
    bool: True if the climb_id exists in the csv file, False otherwise.

    Raises:
    None

    Note:
    The csv file should have a header line and the climb_id should be the first column.
    """
    climb_ids =  []
    with open(climbs_filepath, 'r') as file:
        next(file) # skip header line
        for line in file:
            climb_ids.append(int(line.split(',')[0])) # gets climb_id from line
    return climb_id in climb_ids


# STATISTICS FUNCTIONS #################################################################



def statistics_on_single_climb(attempts_filepath : str | os.PathLike, climbid : int):
    """
    This function calculates and returns statistics for a single climb from a given file containing attempts data.

    Parameters:
    attempts_filepath (str | os.PathLike): The file path to the CSV file containing the attempts data.
    climbid (int): The unique identifier of the climb for which statistics are to be calculated.

    Returns:
    pd.DataFrame: A DataFrame containing the calculated statistics for the specified climb.

    Raises:
    TypeError: If the climbid is not an integer.
    TypeError: If attempts_filepath is not a string or os.PathLike
    """
    if not isinstance(climbid, int):
        raise TypeError(f'Expected int for climbid, got {type(climbid)}')
    if not isinstance(attempts_filepath, (str, os.PathLike)):
        raise TypeError(f'Expected str or os.PathLike for attempts_filepath, got {type(attempts_filepath)}')

    # read in updated attempts file
    attempts_df= pd.read_csv(attempts_filepath, header=0, index_col=None, dtype=None, engine=None,
                                        converters=None, skipinitialspace=True, skiprows=None, skipfooter=0,
                                        nrows=None, na_values=None, keep_default_na=True, na_filter=True,
                                        parse_dates=['attempt_date'], date_format='%Y-%m-%d', dayfirst=False, comment='#')

    # selects all attempts on this climb_id
    attempts_on_this_climbid = attempts_df.groupby('climb_id').get_group(climbid) 

    # following functions act on a single Series of data for one climb.
    first_attempt = attempts_on_this_climbid['attempt_date'].min() # finds first attempt date (format pd._libs.tslibs.timestamps.Timestamp)
    latest_attempt = attempts_on_this_climbid['attempt_date'].max() # finds latest attempt date 
    sent_status = attempts_on_this_climbid['success'].any() # checks if success column has any trues for each climb_id 
    total_number_attempts = attempts_on_this_climbid.shape[0] # number of attempts
    if sent_status:
        first_send = attempts_on_this_climbid[attempts_on_this_climbid['success'] == True]['attempt_date'].min() # first send date
        attempts_to_send = attempts_on_this_climbid[attempts_on_this_climbid['attempt_date'] <= first_send].shape[0] # number of attempts to send including sent attempt
    else:
        first_send = None # will be converted to pd._libs.tslibs.nattype.NaTType NaT when added to dataframe
        attempts_to_send = None # will be converted to NaN np.float64 when added to dataframe

    # dictionary of updated data to pass to replace row in dataframe
    aggregate_data = {
        # 'climb_id' : climbid,
        'first_attempt_date': first_attempt, # if reading to str, first_attempt.date().isoformat() etc
        'latest_attempt_date': latest_attempt,
        'sent_status': sent_status,
        'total_number_attempts': total_number_attempts,
        'first_send_date': first_send,
        'attempts_to_send': attempts_to_send,
    }

    agg_df = pd.DataFrame(aggregate_data, index = [climbid]) # creates dataframe with single row
    agg_df.index.name  = 'climb_id'

    return agg_df


def statistics_on_all_climbs(attempts_filepath: str | os.PathLike):
    """
    This function calculates and returns statistics for all climbs from a given file containing attempts data.

    Parameters:
    attempts_filepath (str | os.PathLike): The file path to the CSV file containing the attempts data.

    Returns:
    pd.DataFrame: A DataFrame containing the calculated statistics for all climbs.

    Raises:
    TypeError: If attempts_filepath is not a string or os.PathLike

    Note:
    The function reads the attempts data from the CSV file, groups it by climb_id, and calculates various statistics
    such as first attempt date, latest attempt date, sent status, total number of attempts, first send date, and attempts to send.
    """

    if not isinstance(attempts_filepath, (str, os.PathLike)):
        raise TypeError(f'Expected str or os.PathLike for attempts_filepath, got {type(attempts_filepath)}')
    
    # read in updated attempts file
    attempts_df= pd.read_csv(attempts_filepath, header=0, index_col=None, dtype=None, engine=None,
                                        converters=None, skipinitialspace=True, skiprows=None, skipfooter=0,
                                        nrows=None, na_values=None, keep_default_na=True, na_filter=True,
                                        parse_dates=['attempt_date'], date_format='%Y-%m-%d', dayfirst=False, comment='#')

    # group attempt dates by climb_id in groupby object
    attempts_grouped_climbid = attempts_df.groupby(['climb_id']) # this groups attempt dates by climb_id in groupby object

    # aggregate data:
    first_attempts = attempts_grouped_climbid['attempt_date'].apply(lambda x: x.min()) # finds first attempt date for each climb_id group
    latest_attempts = attempts_grouped_climbid['attempt_date'].apply(lambda x: x.max()) # finds latest attempt date for each climb_id group
    sent_statuses = attempts_grouped_climbid['success'].apply(lambda x: x.any()) # checks if success column has any trues for each climb_id group
    total_number_attempts = attempts_grouped_climbid.size()
    first_sends = attempts_grouped_climbid.apply(lambda x: x[x["success"]==True]['attempt_date'].min() if x["success"].any() else None, include_groups=False)
    attempts_to_send = attempts_grouped_climbid.apply(lambda x: x[x['attempt_date'] <= x[x['success']==True]['attempt_date'].min()].shape[0] if x['success'].any() else None, include_groups=False)
    # what happens if there are null rows?

    aggregate_data = {
        'first_attempt_date': first_attempts,
        'latest_attempt_date': latest_attempts,
        'sent_status': sent_statuses,
        'total_number_attempts': total_number_attempts,
        'first_send_date': first_sends,
        'attempts_to_send': attempts_to_send,
    }

    agg_df = pd.DataFrame.from_dict(aggregate_data, orient = 'columns') # pd.DataFrame.from_dict() is slightly faster
    # pandas seems to automatically take the climb_id index from the Series objects first_attempts etc and assign
    # this as the index of agg_df. Not sure I like that...
    # agg_df.set_index(list(attempts_grouped_climbid.groups.keys()), inplace = True)
    # agg_df.index.name  = 'climb_id'
    return agg_df
