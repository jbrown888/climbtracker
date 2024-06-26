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

# define date 
default_date = '2024-06-20' #dt.date.today().isoformat()
date_var = tk.StringVar(value = default_date)
dateentry_widget = ttk.Entry(frm, textvariable=date_var) # date entry box
dateentry_widget.grid(column =0, row = 0)
def get_date():
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

enterdate_button_widget = tk.Button(frm, text="Submit Date", command = get_date)
enterdate_button_widget.grid(row=0, column=1)

# define climb_id
climbid_var = tk.IntVar()
climbentry_widget = ttk.Entry(frm, textvariable=climbid_var) # climb id entry box
climbentry_widget.grid(column =0, row = 1)
def get_climbid():
    global climb_entered
    climbidstr = climbentry_widget.get()
    print(f"Climb id: {climbidstr}")
    try:
        climbid = int(climbidstr)
    except Exception as e:
        print(e)
    climb_entered = True
    attempts_data[f'{bc.attempt_file_columns[0]}'] = climbid

enterclimbid_button_widget = tk.Button(frm, text="Submit climb id", command = get_climbid)
enterclimbid_button_widget.grid(row=1, column=1)

# define send/success/True or fail/False
def send_climb():
    global send_status_entered, sent_status
    print(f"You sent the climb! Nice!")
    send_status_entered = True
    sent_status = True

def try_climb():
    global send_status_entered, sent_status
    print(f"You didn't send the climb. But good effort!")
    send_status_entered = True
    sent_status = False

sent_button_widget = ttk.Checkbutton(frm, text="Sent!", style="Switch", command = send_climb)
sent_button_widget.grid(row=2, column=0)
tried_button_widget = tk.Button(frm, text="Tried", command = try_climb)
tried_button_widget.grid(row=2, column=1)

# define number of attempts
try_counter = tk.IntVar(value = 1)
attempts_data['num_attempts'] = 1

def add_try():
    try_counter.set(try_counter.get() + 1)
    attempts_data['num_attempts'] = try_counter.get()

def remove_try():
    if try_counter.get() > 1:
        try_counter.set(try_counter.get() - 1)
        attempts_data['num_attempts'] = try_counter.get()
    else: 
        pass

tries_label = tk.Label(frm, text="Number of tries")
tries_label.grid(row = 3, column = 1)
add_try_button_widget = tk.Button(frm, text = '+', command = add_try)
add_try_button_widget.grid(row = 4, column = 2)
remove_try_button_widget = tk.Button(frm, text = '-', command = remove_try)
remove_try_button_widget.grid(row = 4, column = 0)
display_tries_widget = tk.Label(frm, textvariable=try_counter)
display_tries_widget.grid(row = 4, column = 1)


# submit data to file
def check_buttons():
    global date_entered, climb_entered, send_status_entered, sent_status
    if date_entered and climb_entered and send_status_entered:
        print(attempts_data)
        print(f'Sent? = {sent_status}')
        if sent_status:
            bc.add_N_attempts_send_final_try_on_one_climb_same_date(fpath, **attempts_data)
        else:
            bc.add_N_failed_attempts_on_one_climb_same_date(fpath, **attempts_data)
        root.destroy()

submit_button_widget = tk.Button(frm, text="Done", command = check_buttons)
submit_button_widget.grid(row=8, column=1)

# execute GUI
root.mainloop()

