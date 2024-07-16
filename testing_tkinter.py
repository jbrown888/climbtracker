"""
@author: jbrown888
19/06/24
"""
from tkinter import ttk
import os
import csv
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
import broomcupboard as bc
import datetime as dt
tcl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme", "forest-light.tcl")

#%%
# basic hello world message
root = tk.Tk() # creates instance of Tk class, initialises Tk and creates associated Tcl interpreter.
# also creates root window (toplevel)
frm = ttk.Frame(root, padding=10) # creates frame widget
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0) # label widget with static text string. grid method specifies relative position of label within frame 
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0) #creates button
root.mainloop() # puts everything on display


# widgets arranged in hierarchy. if creating child, parent widget passed as first argument to constructor
# i.e. above example: root -> frame -> label, button
# grid manages position
# event loop: reacts to user input

#%%

def create_csv_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask the user to select a directory
    directory = filedialog.askdirectory()

    if not directory:
        messagebox.showerror("Error", "No directory selected.")
        return

    # Ask the user to enter a filename
    filename = filedialog.asksaveasfilename(
        initialdir=directory,
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
    )

    if not filename:
        messagebox.showerror("Error", "No filename provided.")
        return

    # Create the CSV file
    try:
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([])  # Write an empty row

        messagebox.showinfo("Success", f"CSV file '{os.path.basename(filename)}' created.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create CSV file: {str(e)}")

# Call the function to create the CSV file
create_csv_file()

#%%
def create_attempts_file():
    fname = "attempts_data.csv"
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask the user to select a directory
    directory = filedialog.askdirectory() # returns string with / for file separator. os.path.join joins with \\
    directory = os.path.normpath(directory) 
    if not directory:
        messagebox.showerror("Error", "No directory selected.")
        return

    filename = os.path.join(directory, fname)
    print(filename)

    # Create the CSV file
    try:
        with open(filename, "x", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(bc.attempt_file_columns)  # Write attempts column names

        messagebox.showinfo("Success", f"CSV file '{os.path.basename(filename)}' created.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create CSV file: {str(e)}")

def create_climbs_file():
    fname = "climbs_data.csv"
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask the user to select a directory
    directory = filedialog.askdirectory() # returns string with / for file separator. os.path.join joins with \\
    directory = os.path.normpath(directory) 
    if not directory:
        messagebox.showerror("Error", "No directory selected.")
        return

    filename = os.path.join(directory, fname)
    print(filename)

    # Create the CSV file
    try:
        with open(filename, "x", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(bc.climb_file_columns)  # Write attempts column names

        messagebox.showinfo("Success", f"CSV file '{os.path.basename(filename)}' created.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create CSV file: {str(e)}")

#%%
# from tkcalendar import *
# def get_date():
#     def cal_done():
#         top.withdraw()
#         root.quit()

#     root = tk.Tk()
#     root.withdraw() # keep the root window from appearing

#     top = tk.Toplevel(root)

#     cal = Calendar(top,
#                    font="Arial 14", selectmode='day',
#                    cursor="hand1")
#     cal.pack(fill="both", expand=True)
#     ttk.Button(top, text="ok", command=cal_done).pack()

#     selected_date = None
#     root.mainloop()
#     return cal.selection_get()

# selection = get_date()
# print(selection)

#%%
# https://stackoverflow.com/questions/13242970/tkinter-entry-box-formatted-for-date
# class DateEntry(tk.Frame):
#     def __init__(self, master, frame_look={}, **look):
#         args = dict(relief=tk.SUNKEN, border=1)
#         args.update(frame_look)
#         tk.Frame.__init__(self, master, **args)

#         args = {'relief': tk.FLAT}
#         args.update(look)

#         self.entry_1 = tk.Entry(self, width=2, **args)
#         self.label_1 = tk.Label(self, text='/', **args)
#         self.entry_2 = tk.Entry(self, width=2, **args)
#         self.label_2 = tk.Label(self, text='/', **args)
#         self.entry_3 = tk.Entry(self, width=4, **args)

#         self.entry_1.pack(side=tk.LEFT)
#         self.label_1.pack(side=tk.LEFT)
#         self.entry_2.pack(side=tk.LEFT)
#         self.label_2.pack(side=tk.LEFT)
#         self.entry_3.pack(side=tk.LEFT)

#         self.entries = [self.entry_1, self.entry_2, self.entry_3]

#         self.entry_1.bind('<KeyRelease>', lambda e: self._check(0, 2))
#         self.entry_2.bind('<KeyRelease>', lambda e: self._check(1, 2))
#         self.entry_3.bind('<KeyRelease>', lambda e: self._check(2, 4))

#     def _backspace(self, entry):
#         cont = entry.get()
#         entry.delete(0, tk.END)
#         entry.insert(0, cont[:-1])

#     def _check(self, index, size):
#         entry = self.entries[index]
#         next_index = index + 1
#         next_entry = self.entries[next_index] if next_index < len(self.entries) else None
#         data = entry.get()

#         if len(data) > size or not data.isdigit():
#             self._backspace(entry)
#         if len(data) >= size and next_entry:
#             next_entry.focus()

#     def get(self):
#         return [e.get() for e in self.entries]


# if __name__ == '__main__':        
#     win = tk.Tk()
#     win.title('DateEntry demo')

#     dentry = DateEntry(win, font=('Helvetica', 40, tk.NORMAL), border=0)
#     dentry.pack()

#     win.bind('<Return>', lambda e: print(dentry.get()))
#     win.mainloop()

#%%

# input single attempt data
dirpath = os.path.join(os.getcwd(), 'sample_data')
fname = 'attempts_data.csv'
fpath = os.path.join(dirpath, fname)

tcl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme", "forest-light.tcl")

date_entered = False
climb_entered = False
send_status_entered = False

attempt_data = {}

root = tk.Tk() 
# Import the tcl file
style = ttk.Style(root)
root.tk.call("source", tcl_path)
style.theme_use("forest-light")

root.title("Input attempt data")
frm = ttk.Frame(root, padding=40) # creates frame widget
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

enterdate_button_widget = tk.Button(frm, text="Submit Date", command = get_date)
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

enterclimbid_button_widget = tk.Button(frm, text="Submit climb id", command = get_climbid)
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

sent_button_widget = tk.Button(frm, text="Send", command = send_climb)
sent_button_widget.grid(row=2, column=0)
try_button_widget = tk.Button(frm, text="Try", command = try_climb)
try_button_widget.grid(row=2, column=1)

def check_buttons():
    global date_entered, climb_entered, send_status_entered
    if date_entered and climb_entered and send_status_entered:
        print(attempt_data)
        bc.add_new_attempt_to_file(fpath, attempt_data)
        root.destroy()

submit_button_widget = tk.Button(frm, text="Done", command = check_buttons)
submit_button_widget.grid(row=3, column=1)

root.mainloop()
# print(string_var.get())

#%%
# Create switch toggle
# Create Object
root = tk.Tk()
 
# Add Title
root.title('On/Off Switch!')
 
# Add Geometry
root.geometry("500x300")
 
# Keep track of the button state on/off
#global is_on
is_on = True
 
# Create Label
my_label = tk.Label(root, 
    text = "The Switch Is On!", 
    fg = "green", 
    font = ("Helvetica", 32))
 
my_label.pack(pady = 20)
 
# Define our switch function
def switch():
    global is_on
     
    # Determine is on or off
    if is_on:
        on_button.config(image = off)
        my_label.config(text = "The Switch is Off", 
                        fg = "grey")
        is_on = False
    else:
       
        on_button.config(image = on)
        my_label.config(text = "The Switch is On", fg = "green")
        is_on = True
 
# Define Our Images
on = tk.PhotoImage(file = "D:\\j_Documents\\cliimbing\\climbtracker\\theme\\forest-light\\on-accent.png")
off = tk.PhotoImage(file = "D:\\j_Documents\\cliimbing\\climbtracker\\theme\\forest-light\\off-basic.png")
 
# Create A Button
on_button = tk.Button(root, image = on, bd = 0,
                   command = switch)
on_button.pack(pady = 50)
 
# Execute Tkinter
root.mainloop()
#%%
root = tk.Tk()
root.title("Forest")
root.option_add("*tearOff", False) # This is always a good idea
# Import the tcl file
style = ttk.Style(root)
root.tk.call("source", tcl_path)
style.theme_use("forest-light")

# Make the app responsive
root.columnconfigure(index=0, weight=1)
root.columnconfigure(index=1, weight=1)
root.columnconfigure(index=2, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=1)

# Create a Frame for input widgets
widgets_frame = ttk.Frame(root, padding=(0, 0, 0, 10))
widgets_frame.grid(row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
widgets_frame.columnconfigure(index=0, weight=1)

# Switch
switch = ttk.Checkbutton(widgets_frame, text="Switch", style="Switch")
switch.grid(row=9, column=0, padx=5, pady=10, sticky="nsew")

root.mainloop()
#%%
# input multiple attempts on one climb, one date

dirpath = os.path.join(os.getcwd(), 'sample_data')
fname = 'attempts_data.csv'
fpath = os.path.join(dirpath, fname)
tcl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme", "forest-light.tcl")

date_entered = False
climb_entered = False
send_status_entered = False
sent_status = False
attempts_data = {}

root = tk.Tk() 
# Import the tcl file
style = ttk.Style(root)
root.tk.call("source", tcl_path)
style.theme_use("forest-light")

root.title("Input attempt data")
frm = ttk.Frame(root, padding=40) # creates frame widget
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
            attempts_data[f'{bc.attempt_file_columns[1]}'] = attemptdate

enterdate_button_widget = tk.Button(frm, text="Submit Date", command = get_date)
enterdate_button_widget.grid(row=0, column=1)

# define climb_id
climbid_var = tk.IntVar()
climbentry_widget = ttk.Entry(frm, textvariable=climbid_var)
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
    # attempts_data['num_attempts'] = 1
    # turn button green
    # open num_attempts options

def try_climb():
    global send_status_entered, sent_status
    print(f"You didn't send the climb. But good effort!")
    send_status_entered = True
    sent_status = False
    # attempts_data['num_attempts'] = 1

    # turn button grey?
    # open num_attempts options

try_counter = tk.IntVar(value = 1)
attempts_data['num_attempts'] = 1

def add_try():
    try_counter.set(try_counter.get() + 1)
    attempts_data['num_attempts'] = try_counter.get()

def remove_try():
    if try_counter.get() > 0:
        try_counter.set(try_counter.get() - 1)
        attempts_data['num_attempts'] = try_counter.get()
    else: 
        pass
    # attempts_data['num_attempts'] -= 1 # but >0

sent_button_widget = ttk.Checkbutton(frm, text="Sent!", style="Switch", command = send_climb)
sent_button_widget.grid(row=2, column=0)
tried_button_widget = tk.Button(frm, text="Tried", command = try_climb)
tried_button_widget.grid(row=2, column=1)

tries_label = tk.Label(frm, text="Number of tries")
tries_label.grid(row = 3, column = 1)

add_try_button_widget = tk.Button(frm, text = '+', command = add_try)
add_try_button_widget.grid(row = 4, column = 2)
remove_try_button_widget = tk.Button(frm, text = '-', command = remove_try)
remove_try_button_widget.grid(row = 4, column = 0)
display_tries_widget = tk.Label(frm, textvariable=try_counter)
display_tries_widget.grid(row = 4, column = 1)


def check_buttons():
    global date_entered, climb_entered, send_status_entered, sent_status
    if date_entered and climb_entered and send_status_entered:
        print(attempts_data)
        if sent_status:
            bc.add_N_attempts_send_final_try_on_one_climb_same_date(fpath, **attempts_data)
        else:
            bc.add_N_failed_attempts_on_one_climb_same_date(fpath, **attempts_data)
        root.destroy()

submit_button_widget = tk.Button(frm, text="Done", command = check_buttons)
submit_button_widget.grid(row=8, column=1)

root.mainloop()

#%% Testing switching between frames
from tkinter import font as tkfont  # python 3

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            # F is the loop variable. 
            # The loop is iterating over a list of classes, so each time through the loop F will be representing a class. 
            # F(...) creates an instance of the class. 
            # These classes (StartPage, PageOne, PageTwo) all require two parameters: a widget that will be the parent of this class//
            # and an object that will server as a controller (a term borrowed from the UI patter model/view/controller).
            # The line of code creates an instance of the class (which itself is a subclass of a Frame widget)//
            # and temporarily assigns the frame to the local variable frame.
            # passing self as parameter means these new class instances can call methods in SampleApp class

            self.frames[page_name] = frame
            # can access page through dictionary self.frames

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        # zorder
        frame = self.frames[page_name]
        frame.tkraise() # raises frame to the top of the stacking order
        # each page is subclass of tk.Frame (StartPage, PageOne, PageTwo), so tk.Frame.__init__(self,parent) calls//
        # constructor of parent class


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()