# -*- coding: utf-8 -*-
"""
@author: jbrown888
8/6/24
#cwd = D:\\j_Documents\\cliimbing\\climbtracker
# working and tested functions for calculating statistics
"""

# functions for calculating statistics and aggregating data
import datetime as dt
import os
import csv 
import pandas as pd
import re
import numpy as np
import copy



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
#%%

dirpath = os.path.join(os.getcwd(), 'real_data')

attempts_fpath = os.path.join(dirpath, 'attempts_data.csv')

climbid = 10

attempts_df= pd.read_csv(attempts_fpath, header=0, index_col=None, dtype=None, engine=None,
                                    converters=None, skipinitialspace=True, skiprows=None, skipfooter=0,
                                    nrows=None, na_values=None, keep_default_na=True, na_filter=True,
                                    parse_dates=['attempt_date'], date_format='%Y-%m-%d', dayfirst=False, comment='#')

# selects all attempts on this climb_id
attempts_grouped_climbid = attempts_df.groupby(['climb_id']) # this groups attempt dates by climb_id in groupby object

# aggregate data:
first_attempts = attempts_grouped_climbid['attempt_date'].apply(lambda x: x.min()) # finds first attempt date for each climb_id group
latest_attempts = attempts_grouped_climbid['attempt_date'].apply(lambda x: x.max()) # finds latest attempt date for each climb_id group
sent_statuses = attempts_grouped_climbid['success'].apply(lambda x: x.any()) # checks if success column has any trues for each climb_id group
total_number_attempts = attempts_grouped_climbid.size()
first_sends = attempts_grouped_climbid.apply(lambda x: x[x["success"]==True]['attempt_date'].min() if x["success"].any() else None, include_groups=False)
attempts_to_send = attempts_grouped_climbid.apply(lambda x: x[x['attempt_date'] <= x[x['success']==True]['attempt_date'].min()].shape[0] if x['success'].any() else None, include_groups=False)
number_of_sends = attempts_grouped_climbid['success'].apply(lambda x: x.sum(skipna=True)) # counts number of Trues in success column for each climb_id group
# what happens if there are null rows?

aggregate_data = {
    'first_attempt_date': first_attempts,
    'latest_attempt_date': latest_attempts,
    'sent_status': sent_statuses,
    'total_number_attempts': total_number_attempts,
    'first_send_date': first_sends,
    'attempts_to_send': attempts_to_send,
    'number_of_sends': number_of_sends,
}

agg_df = pd.DataFrame.from_dict(aggregate_data, orient = 'columns') # pd.DataFrame.from_dict() is slightly faster
