"""
@author: jbrown888
25/6/24
Creates GUI that allows user to input multiple attempts on same climb, same date, with final send or not
"""

from tkinter import ttk
import os
import tkinter as tk
import broomcupboard as bc
import datetime as dt

# define file to add attempts to 
dirpath = os.path.join(os.getcwd(), 'real_data')
fname = 'attempts_data.csv'
fpath = os.path.join(dirpath, fname)

# define file for importing tcl theme
tcl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme", "forest-light.tcl")

# initialize global variables
date_entered = False
climb_entered = False
send_status_entered = False
sent_status = False
attempts_data = {}

root = tk.Tk() # create GUI window, initialize instance of Tk class

# set theme
style = ttk.Style(root) 
root.tk.call("source", tcl_path)
style.theme_use("forest-light")

root.title("Input attempt data") # set title
frm = ttk.Frame(root, padding=40) # creates frame widget
frm.grid()

# Create text entry widget for defining date 
default_date = '2024-12-21' #dt.date.today().isoformat()
date_var = tk.StringVar(value = default_date) # store str variable of date
dateentry_widget = ttk.Entry(frm, textvariable=date_var) # date entry box
dateentry_widget.grid(column =0, row = 0) # set position
def get_date():
    """
    This function retrieves the date input from the GUI and validates it.
    It then updates the global variable 'date_entered' and the 'attempts_data' dictionary.

    Parameters:
    None

    Returns:
    None

    Notes:
    Will not add date_entered to attempts_data if it is either the wrong datetime format ,or in the future
    These exceptions are caught and printed.

    """    
    global date_entered
    datestr = dateentry_widget.get()
    print(f"You entered: {datestr}")
    try:
        attemptdate = dt.datetime.strptime(datestr, '%Y-%m-%d').date()
    except Exception as e:
        print(f'Wrong datetime format, must be YYYY-MM-DD and received {datestr}')
        print(e)
    else:
        if attemptdate > dt.date.today():
            print('Attempt date cannot be in the future.')
        else:
            print(f'Attempt Date: {attemptdate}')
            date_entered = True
            attempts_data[f'{bc.attempt_file_columns[1]}'] = attemptdate
# Create widget for button to submit date
enterdate_button_widget = tk.Button(frm, text="Submit Date", command = get_date)
enterdate_button_widget.grid(row=0, column=1)

# Create widget for text entry box to define climb_id
climbid_var = tk.IntVar() # int var to store climb_id
climbentry_widget = ttk.Entry(frm, textvariable=climbid_var) # climb id entry box
climbentry_widget.grid(column =0, row = 1)
def get_climbid():
    """
    This function retrieves the climb id input from the GUI, validates it, and updates the global variables.
    It also populates the 'attempts_data' dictionary with the climb id.

    Parameters:
    None

    Returns:
    None

    Raises:
    ValueError: If the input string cannot be converted to an integer.
    """    
    global climb_entered
    climbidstr = climbentry_widget.get()
    print(f"Climb id: {climbidstr}")
    try:
        climbid = int(climbidstr)
    except Exception as e:
        print(e)
    climb_entered = True
    attempts_data[f'{bc.attempt_file_columns[0]}'] = climbid
# Create widget for button to submit climb_id
enterclimbid_button_widget = tk.Button(frm, text="Submit climb id", command = get_climbid)
enterclimbid_button_widget.grid(row=1, column=1)

# define send/success/True or fail/False
def send_climb():
    """
    This function updates the global variables 'send_status_entered' and 'sent_status' to indicate that the climb was sent.
    It also prints a message to the console.

    Parameters:
    None

    Returns:
    None

    Global Variables:
    send_status_entered (bool): Indicates whether the send status has been entered.
    sent_status (bool): Indicates whether the climb was sent (True) or not (False).
    """
    global send_status_entered, sent_status
    print(f"You sent the climb! Nice!")
    send_status_entered = True
    sent_status = True

def try_climb():
    """
    This function updates the global variables 'send_status_entered' and 'sent_status' to indicate that the climb was not sent.
    It also prints a message to the console.

    Parameters:
    None

    Returns:
    None

    Global Variables:
    send_status_entered (bool): Indicates whether the send status has been entered.
    sent_status (bool): Indicates whether the climb was sent (True) or not (False).
    """
    global send_status_entered, sent_status
    print(f"You didn't send the climb. But good effort!")
    send_status_entered = True
    sent_status = False
#Create widgets for sending or trying climb
sent_button_widget = ttk.Checkbutton(frm, text="Sent!", style="Switch", command = send_climb)
sent_button_widget.grid(row=2, column=0)
tried_button_widget = tk.Button(frm, text="Tried", command = try_climb)
tried_button_widget.grid(row=2, column=1)

# define number of attempts
try_counter = tk.IntVar(value = 1) # int var for storing number of attempts. default is 1
attempts_data['num_attempts'] = 1

def add_try():
    """
    Increments the number of attempts by 1 and updates the 'attempts_data' dictionary.

    Parameters:
    None

    Returns:
    None

    Global Variables:
    try_counter (tk.IntVar): A tkinter IntVar object used to store the number of attempts.
    attempts_data (dict): A dictionary used to store the climb attempt data. The 'num_attempts' key is updated with the new value.
    """
    try_counter.set(try_counter.get() + 1)
    attempts_data['num_attempts'] = try_counter.get()

def remove_try():
    """
    Decreases the number of attempts by 1 and updates the 'attempts_data' dictionary.
    If number of attempts is already 1, it does nothing.

    Parameters:
    None

    Returns:
    None

    Global Variables:
    try_counter (tk.IntVar): A tkinter IntVar object used to store the number of attempts.
    attempts_data (dict): A dictionary used to store the climb attempt data. The 'num_attempts' key is updated with the new value.
    """    
    if try_counter.get() > 1:
        try_counter.set(try_counter.get() - 1)
        attempts_data['num_attempts'] = try_counter.get()
    else: 
        pass

# Create widgets for adding and removing tries, and label to display number of tries
tries_label = tk.Label(frm, text="Number of tries") # label
tries_label.grid(row = 3, column = 1)
add_try_button_widget = tk.Button(frm, text = '+', command = add_try) # add try button
add_try_button_widget.grid(row = 4, column = 2)
remove_try_button_widget = tk.Button(frm, text = '-', command = remove_try) # remove try button
remove_try_button_widget.grid(row = 4, column = 0)
display_tries_widget = tk.Label(frm, textvariable=try_counter)
display_tries_widget.grid(row = 4, column = 1)


# submit data to file
def check_buttons():
    """
    This function checks if all necessary data has been entered and then submits the climb attempt data to a file.

    Parameters:
    None

    Returns:
    None

    Global Variables:
    date_entered (bool): Indicates whether the date has been entered.
    climb_entered (bool): Indicates whether the climb id has been entered.
    send_status_entered (bool): Indicates whether the send status has been entered.
    sent_status (bool): Indicates whether the climb was sent (True) or not (False).
    attempts_data (dict): A dictionary used to store the climb attempt data.
    fpath (str): The file path where the data will be saved.

    Side Effects:
    Prints the attempts_data and the send status to the console.
    Calls the appropriate function from the 'broomcupboard' module to save the data to a file.
    Destroys the GUI window when the data is successfully submitted.
    """
    global date_entered, climb_entered, send_status_entered, sent_status
    if date_entered and climb_entered and send_status_entered: # check if all data entered
        print(attempts_data)
        print(f'Sent? = {sent_status}')
        if sent_status:
            # if climb sent
            bc.add_N_attempts_send_final_try_on_one_climb_same_date(fpath, **attempts_data)
        else:
            # if climb not sent
            bc.add_N_failed_attempts_on_one_climb_same_date(fpath, **attempts_data)
        root.destroy()

submit_button_widget = tk.Button(frm, text="Done", command = check_buttons)
submit_button_widget.grid(row=8, column=1)

# execute GUI
root.mainloop()

