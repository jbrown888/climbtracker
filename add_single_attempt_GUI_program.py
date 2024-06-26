"""
@author: jbrown888
24/6/24
"""
from tkinter import *
from tkinter import ttk
import os
# import csv
# from tkinter import filedialog
# from tkinter import messagebox
import tkinter as tk
import broomcupboard as bc
import datetime as dt


dirpath = os.path.join(os.getcwd(), 'sample_data')
fname = 'attempts_data.csv'
fpath = os.path.join(dirpath, fname)

# input attempt data
date_entered = False
climb_entered = False
send_status_entered = False

attempt_data = {}

root = tk.Tk() 
root.title("Input attempt data")
frm = ttk.Frame(root, padding=60) # creates frame widget
frm.grid()

# define date 
date_var = tk.StringVar()
dateentry_widget = ttk.Entry(frm, textvariable=date_var)
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
            attempt_data.update({f'{bc.attempt_file_columns[1]}':attemptdate})

enterdate_button_widget = Button(frm, text="Submit Date", command = get_date)
enterdate_button_widget.grid(row=0, column=1)

# define climb_id
climbid_var = tk.IntVar()
climbentry_widget = ttk.Entry(frm, textvariable=climbid_var)
climbentry_widget.grid(column =0, row = 1)
def get_climbid():
    global climb_entered
    climbidstr = climbentry_widget.get()
    print(f"Climb id: {climbidstr}")
    climb_entered = True
    attempt_data.update({f'{bc.attempt_file_columns[0]}': climbidstr})

enterclimbid_button_widget = Button(frm, text="Submit climb id", command = get_climbid)
enterclimbid_button_widget.grid(row=1, column=1)

# define send/success/True or fail/False
def send_climb():
    global send_status_entered
    print(f"You sent the climb! Nice!")
    send_status_entered = True
    attempt_data.update({f'{bc.attempt_file_columns[2]}': True})

def try_climb():
    global send_status_entered
    print(f"You didn't send the climb. Good effort!")
    send_status_entered = True
    attempt_data.update({f'{bc.attempt_file_columns[2]}': False})

sent_button_widget = Button(frm, text="Send", command = send_climb)
sent_button_widget.grid(row=2, column=0)
try_button_widget = Button(frm, text="Try", command = try_climb)
try_button_widget.grid(row=2, column=1)

# enter data
def check_buttons():
    global date_entered, climb_entered, send_status_entered
    if date_entered and climb_entered and send_status_entered:
        print(attempt_data)
        bc.add_new_attempt_to_file(fpath, attempt_data)
        root.destroy()

submit_button_widget = Button(frm, text="Done", command = check_buttons)
submit_button_widget.grid(row=3, column=1)


root.mainloop()
