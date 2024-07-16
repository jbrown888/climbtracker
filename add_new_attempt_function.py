# -*- coding: utf-8 -*-
"""
@author: jnb19
8/6/24
#cwd = D:\\j_Documents\\cliimbing\\climbtracker
# working and tested functions for adding to attempts data file
# superseded by broomcupboard on 24/6/24
"""

# appending climb_df file
import datetime as dt
import os
import csv 
import pandas as pd


attempt_file_columns = ['climb_id', 'attempt_date','success']

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


def add_new_attempts_to_file(filepath, newattempts_data, num_attempts):
    """
    This function appends a new attempt date (climb_id, date, success) to a csv file.

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


# NOTE: this function should not be used - it is bad practice to store aggregate/calculated data.
# it should just be recalculated each time
def update_new_attempt_on_existing_climb(newattempt_data, attempts_filepath, agg_data_filepath):
    """
    This function updates the aggregate data AND attempts data files for a new attempt on an existing climb.
    It appends the new attempt to the attempts file, reads the updated attempts file,
    and then updates the aggregate data file with the new statistics.

    Parameters:
    newattempt_data (dict): A dictionary containing the data of the new attempt.
        Should have keys 'climb_id', 'attempt_date', and 'success'.
    attempts_filepath (str): The path to the csv file containing all attempts data.
    agg_data_filepath (str): The path to the csv file containing the aggregate data.

    Returns:
    int: 0 if the function executes successfully, otherwise an error code.

    Raises:
    TypeError: If the newattempt_data is not a dictionary.
    ValueError: If the newattempt_data dictionary does not contain all the required keys.
    """
    if type(newattempt_data) is not dict:
        raise TypeError(f'Expected dict of attempt data, got {type(newattempt_data)}')
    if not all([x in newattempt_data.keys() for x in attempt_file_columns]):
        raise KeyError(f'Expected dict of attempt data with keys {attempt_file_columns[1:]}, got {newattempt_data.keys()}')


    # first append new attempt to attempts datafile
    # -safer to append and then read in rather than read in, append and rewrite whole CSV
    add_new_attempt_to_file(attempts_filepath, newattempt_data)

    # read in updated attempts file
    attempts_df_updated = pd.read_csv(attempts_filepath, header=0, index_col=None, dtype=None, engine=None,
                                      converters=None, skipinitialspace=True, skiprows=None, skipfooter=0,
                                      nrows=None, na_values=None, keep_default_na=True, na_filter=True,
                                      parse_dates=['attempt_date'], date_format='%Y-%m-%d', dayfirst=False, comment='#')

    # selects all attempts on this climb_id
    attempts_on_this_climbid = attempts_df_updated.groupby('climb_id').get_group(newattempt_data['climb_id']) 

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
    # line_replace = ','.join(map(str, updated_aggregate_data.values()))

    # read in aggregate data file
    agg_df_read = pd.read_csv(agg_data_filepath, header=0, index_col=0, dtype=None, engine=None,
                              converters=None, skipinitialspace=True, skiprows=None, skipfooter=0,
                              nrows=None, na_values=None, keep_default_na=True, na_filter=True,
                              parse_dates=['first_attempt_date', 'latest_attempt_date', 'first_send_date'],
                              date_format='%Y-%m-%d', dayfirst=False, comment='#')
    # update row index = climb_id with updated aggregate data
    agg_df_read.loc[newattempt_data['climb_id']] = updated_aggregate_data.values()

    # rewrite aggregate data file
    agg_df_read.to_csv(agg_data_filepath, sep=',', na_rep='NaN', float_format=None, columns=None, header=True, index=True,\
                    index_label=None, mode='w', date_format='%Y-%m-%d', doublequote=True, escapechar=None,\
                    decimal='.')
    
    return 0


