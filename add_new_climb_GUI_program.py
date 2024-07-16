"""
@author: jbrown888
10/7/24
Creates GUI that allows user to input a new climb
"""

from tkinter import ttk
import os
import tkinter as tk
import broomcupboard as bc
import datetime as dt
import re

# define file to add attempts to 
dirpath = os.path.join(os.getcwd(), 'real_data')
fname = 'climbs_data.csv'
fpath = os.path.join(dirpath, fname)

# define file for importing tcl theme
tcl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme", "forest-light.tcl")

root = tk.Tk() # create GUI window, initialize instance of Tk class
root.title("Add Climb")
root.option_add("*tearOff", False) # This is always a good idea

# set theme, import the tcl file
style = ttk.Style(root) 
root.tk.call("source", tcl_path)
style.theme_use("forest-light")

# initialize global variables
sport = False
climb_data = {}

# Set relative weights of columns, determines how extra space distributed when window resized. 
# if weight = 1 for all, even distribution.
root.columnconfigure(index=0, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)

# Panedwindow
paned = ttk.PanedWindow(root)
paned.grid(row=0, column=0, pady=(25, 5), sticky="nsew", rowspan=3)
# pady adds padding to top and bottom of widget: (top, bottom), in pixels
# nsew makes it expand in n s e w directions
# rowspan specifies paned widget should open 3 rows in root window

# Add top pane
top_pane = ttk.Frame(paned)
paned.add(top_pane, weight=1)

# Add bottom pane
bottom_pane = ttk.Frame(paned)
paned.add(bottom_pane, weight=1)

# Notebook
top_notebook = ttk.Notebook(top_pane)

#######
# top tab : basic categories
def sport_switch():
    global sport
    if sport:
        sport = False
    else:
        sport = True

#### Indoor Bouldering Tab
tab_1 = ttk.Frame(top_notebook)
tab_1.columnconfigure(index=0, weight=2)
tab_1.columnconfigure(index=1, weight=2)
for j in range(5):
    tab_1.rowconfigure(index = j, weight =1)
top_notebook.add(tab_1, text="Indoor")

# Grade entry
grade_var = tk.StringVar(value = 'V3')
gradeentry_widget = ttk.Entry(tab_1, textvariable=grade_var) # location entry box
gradeentry_widget.grid(row=0, column =1)
gew_label = ttk.Label(tab_1, text="Grade :", justify="left")
gew_label.grid(row=0, column=0, pady=10, columnspan=1)

# Location entry
location_var = tk.StringVar(value = 'Rockover')
locationentry_widget = ttk.Entry(tab_1, textvariable=location_var) # location entry box
locationentry_widget.grid(row=1, column =1)
lew_label = ttk.Label(tab_1, text="Location :", justify="left")
lew_label.grid(row=1, column=0, pady=10, columnspan=1)

# Sport switch
sportswitch = ttk.Checkbutton(tab_1, style="Switch", command = sport_switch)
sportswitch.grid(row=2, column=1)#, padx=5, pady=10, sticky="w")
sport_label = ttk.Label(tab_1, text= 'Sport?', justify = 'left')
sport_label.grid(row=2, column=0, pady=10, columnspan = 1)
# Rope option for sport
ropevar = tk.StringVar()
ropebox = ttk.Combobox(tab_1, textvariable=ropevar, values=bc.ropes)
ropebox.current(1) # sets intial/default selection to 0 index of values list
ropebox.grid(row=3, column=1, padx=5, pady=10,  sticky="ew")
rope_label = ttk.Label(tab_1, text="Rope style :", justify="left")
rope_label.grid(row=3, column=0, pady=10, columnspan=1)

# Enter information button
def get_info_indoor():
    global sport
    g = grade_var.get()
    try:
        if not re.match(bc.Vgrades_regex_pattern, g) and not re.match(bc.Vgrades_range_regex_pattern, g) and not re.match(bc.font_grades_regex_pattern, g):
            raise Exception("Invalid regex pattern")
        else:
            climb_data['grade'] = grade_var.get()
    except Exception as e:
        print(e)
        print(f'{g} is not a valid font, V or V range grade')
    climb_data['location'] = location_var.get()
    climb_data['climb_name'] = 'NaN'
    climb_data['door'] = bc.doors[0]  # 'indoor'
    climb_data['angle'] = 'NaN'
    climb_data['mbyear'] = 'NaN'
    climb_data['rock_type'] = 'NaN'

    if not sport:
        climb_data['climb_style'] = bc.climb_styles[0] # 'bouldering'
        climb_data['rope'] = 'NaN'
    else:
        climb_data['climb_style'] = bc.climb_styles[1] # 'sport'
        climb_data['rope'] = ropevar.get()
    print(climb_data)

enterinfo_indoor_button_widget = tk.Button(tab_1, text="Submit Climb Details", command = get_info_indoor)
enterinfo_indoor_button_widget.grid(row=4, column=1)


#### Outdoor bouldering tab
tab_2 = ttk.Frame(top_notebook)
tab_2.columnconfigure(index=0, weight=2)
tab_2.columnconfigure(index=1, weight=2)
for j in range(8):
    tab_2.rowconfigure(index = j, weight =1)
top_notebook.add(tab_2, text="Outdoor")

# Name entry
name_var_2 = tk.StringVar()
nameentry_widget_2 = ttk.Entry(tab_2, textvariable=name_var_2) # location entry box
nameentry_widget_2.grid(row=0, column =1)
new_label_2 = ttk.Label(tab_2, text="Name :", justify="left")
new_label_2.grid(row=0, column=0, pady=10, columnspan=1)

# Grade entry
grade_var_2 = tk.StringVar(value = 'V3')
gradeentry_widget_2 = ttk.Entry(tab_2, textvariable=grade_var_2) # location entry box
gradeentry_widget_2.grid(row=1, column =1)
gew_label_2 = ttk.Label(tab_2, text="Grade :", justify="left")
gew_label_2.grid(row=1, column=0, pady=10, columnspan=1)

# Location entry
location_var_2 = tk.StringVar(value = 'Rockover')
locationentry_widget_2 = ttk.Entry(tab_2, textvariable=location_var_2) # location entry box
locationentry_widget_2.grid(row=2, column =1)
lew_label_2 = ttk.Label(tab_2, text="Location :", justify="left")
lew_label_2.grid(row=2, column=0, pady=10, columnspan=1)

# Rock type
rock_var_2 = tk.StringVar()
rockbox_2 = ttk.Combobox(tab_2, textvariable= rock_var_2, values=bc.rock_types)
rockbox_2.current(0) # sets intial/default selection to 0 index of values list
rockbox_2.grid(row=3, column=1, padx=5, pady=10,  sticky="ew")
rock_label_2 = ttk.Label(tab_2, text="Rock type :", justify="left")
rock_label_2.grid(row=3, column=0, pady=10, columnspan=1)

# Sport switch
sportswitch_2 = ttk.Checkbutton(tab_2, style="Switch", command = sport_switch)
sportswitch_2.grid(row=4, column=1)#, padx=5, pady=10, sticky="w")
sport_label_2 = ttk.Label(tab_2, text= 'Sport?', justify = 'left')
sport_label_2.grid(row=4, column=0, pady=10, columnspan = 1)
# Rope option for sport
ropevar_2 = tk.StringVar()
ropebox_2 = ttk.Combobox(tab_2, textvariable=ropevar_2, values=bc.ropes)
ropebox_2.current(1) # sets intial/default selection to 0 index of values list
ropebox_2.grid(row=5, column=1, padx=5, pady=10,  sticky="ew")
rope_label_2 = ttk.Label(tab_2, text="Rope style :", justify="left")
rope_label_2.grid(row=5, column=0, pady=10, columnspan=1)

def get_info_outdoor():
    global sport
    climb_data['grade'] = grade_var_2.get()
    climb_data['location'] = location_var_2.get()
    climb_data['climb_name'] = name_var_2.get()
    climb_data['door'] = bc.doors[1]  # 'outdoor'
    climb_data['angle'] = 'NaN'
    climb_data['mbyear'] = 'NaN'
    climb_data['rock_type'] = rock_var_2.get()

    if not sport:
        climb_data['climb_style'] = bc.climb_styles[0] # 'bouldering'
        climb_data['rope'] = 'NaN'
    else:
        climb_data['climb_style'] = bc.climb_styles[1] # 'sport'
        climb_data['rope'] = ropevar_2.get()
    print(climb_data)

enterinfo_outdoor_button_widget = tk.Button(tab_2, text="Submit Climb Details", command = get_info_outdoor)
enterinfo_outdoor_button_widget.grid(row=7, column=1)


#### Moonboard tab
tab_3 = ttk.Frame(top_notebook)
tab_3.columnconfigure(index=0, weight=2)
tab_3.columnconfigure(index=1, weight=1)
tab_3.columnconfigure(index=2, weight=2)
for j in range(6):
    tab_3.rowconfigure(index = j, weight =1)
top_notebook.add(tab_3, text="Moonboard")

# Name entry
name_var_3 = tk.StringVar()
nameentry_widget_3 = ttk.Entry(tab_3, textvariable=name_var_3) # location entry box
nameentry_widget_3.grid(row=0, column =1)
new_label_3 = ttk.Label(tab_3, text="Name :", justify="left")
new_label_3.grid(row=0, column=0, pady=10, columnspan=1)

# Grade entry
grade_var_3 = tk.StringVar(value = 'V3')
gradeentry_widget_3 = ttk.Entry(tab_3, textvariable=grade_var_3) # location entry box
gradeentry_widget_3.grid(row=1, column =1)
gew_label_3 = ttk.Label(tab_3, text="Grade :", justify="left")
gew_label_3.grid(row=1, column=0, pady=10, columnspan=1)

# Location entry
location_var_3 = tk.StringVar(value = 'Rockover')
locationentry_widget_3 = ttk.Entry(tab_3, textvariable=location_var_3) # location entry box
locationentry_widget_3.grid(row=2, column =1)
lew_label_3 = ttk.Label(tab_3, text="Location :", justify="left")
lew_label_3.grid(row=2, column=0, pady=10, columnspan=1)

# Year option
year_var_3 = tk.StringVar()
yearbox_3 = ttk.Combobox(tab_3, textvariable=year_var_3, values= bc.mbyears)
yearbox_3.current(1) # sets intial/default selection to 0 index of values list
yearbox_3.grid(row=3, column=1, padx=5, pady=10,  sticky="ew")
year_label_3 = ttk.Label(tab_3, text="Year :", justify="left")
year_label_3.grid(row=3, column=0, pady=10, columnspan=1)

# Year option
angle_var_3 = tk.StringVar()
anglebox_3 = ttk.Combobox(tab_3, textvariable=angle_var_3, values= bc.angles)
anglebox_3.current(1) # sets intial/default selection to 0 index of values list
anglebox_3.grid(row=4, column=1, padx=5, pady=10,  sticky="ew")
angle_label_3 = ttk.Label(tab_3, text="Angle :", justify="left")
angle_label_3.grid(row=4, column=0, pady=10, columnspan=1)

def get_info_moonboard():
    global sport
    climb_data['grade'] = grade_var_3.get()
    climb_data['location'] = location_var_3.get()
    climb_data['climb_name'] = name_var_3.get()
    climb_data['door'] = bc.doors[2]  # 'moonboard'
    climb_data['angle'] = angle_var_3.get()
    climb_data['mbyear'] = year_var_3.get()
    climb_data['rock_type'] = 'NaN'
    climb_data['climb_style'] = bc.climb_styles[0] # 'bouldering'
    climb_data['rope'] = 'NaN'

    print(climb_data)

enterinfo_mb_button_widget = tk.Button(tab_3, text="Submit Climb Details", command = get_info_moonboard)
enterinfo_mb_button_widget.grid(row=5, column=1)

top_notebook.pack(expand=True, fill="both", padx=5, pady=5)


########
# bottom pane - styles and notes

frm = ttk.Frame(bottom_pane)
frm.columnconfigure(index=0, weight=1)
frm.columnconfigure(index=1, weight=1)
frm.columnconfigure(index=2, weight=1)
for j in range(5):
    frm.rowconfigure(index = j, weight =1)
# frm.rowconfigure(index=5, weight=1)
# frm.rowconfigure(index=6, weight=1)
# bottom_pane.add(frm, text="Notes and styles")

# Holds entry
# Create a Frame for the hold types
holds_frame = ttk.LabelFrame(frm, text="Hold Types", padding=(20, 10))
holds_frame.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="nsew")
holds_frame.columnconfigure(index=0, weight=1)
holds_frame.columnconfigure(index=1, weight=1)
for j in range(3):
    holds_frame.rowconfigure(index = j, weight =1)

holdbuttons = []
nrows = 5
holdstyles = []

def select_holdstyle(x, y):
    if y.get()==0:
        try:
            holdstyles.remove(x)
        except KeyError:
            pass
    else:
        holdstyles.append(x)
    print(holdstyles)

for i, hold_ in enumerate(bc.holds):
    hold_var = tk.StringVar(value=hold_)
    hold_onoff = tk.IntVar(value = 0)
    holdbuttons.append(ttk.Checkbutton(holds_frame, text = hold_, variable = hold_onoff, offvalue =0, onvalue = 1, state = 'selected disabled', command=lambda x=hold_, y=hold_onoff: select_holdstyle(x, y)))
    holdbuttons[i].grid(row=i%nrows, column=i//nrows, padx=5, pady=10, sticky="nsew")

# Walls entry
# Create a Frame for the wall types
walls_frame = ttk.LabelFrame(frm, text="Wall Types", padding=(20, 10))
walls_frame.grid(row=0, column=1, padx=(20, 10), pady=10, sticky="nsew")
walls_frame.columnconfigure(index=0, weight=1)
walls_frame.columnconfigure(index=1, weight=1)
for j in range(3):
    walls_frame.rowconfigure(index = j, weight =1)
wallbuttons = []
nrows = 5
wallstyles = []

def select_wallstyle(x, y):
    if y.get()==0:
        try:
            wallstyles.remove(x)
        except KeyError:
            pass
    else:
        wallstyles.append(x)
    print(wallstyles)

for i, wall_ in enumerate(bc.walls):
    wall_var = tk.StringVar(value=wall_)
    wall_onoff = tk.IntVar(value = 0)
    wallbuttons.append(ttk.Checkbutton(walls_frame, text = wall_, variable = wall_onoff, offvalue =0, onvalue = 1, state = 'selected disabled', command=lambda x=wall_, y=wall_onoff: select_wallstyle(x, y)))
    wallbuttons[i].grid(row=i%nrows, column=i//nrows, padx=5, pady=10, sticky="nsew")

# Skills entry
# Create a Frame for the skill types
skills_frame = ttk.LabelFrame(frm, text="Skill Types", padding=(20, 10))
skills_frame.grid(row=0, column=2, padx=(20, 10), pady=10, sticky="nsew")
skills_frame.columnconfigure(index=0, weight=1)
skills_frame.columnconfigure(index=1, weight=1)
for j in range(3):
    skills_frame.rowconfigure(index = j, weight =1)

skillbuttons = []
nrows = 4
skillstyles = []

def select_skillstyle(x, y):
    if y.get()==0:
        try:
            skillstyles.remove(x)
        except KeyError:
            pass
    else:
        skillstyles.append(x)
    # print(skillstyles)

for i, skill_ in enumerate(bc.skills):
    skill_var = tk.StringVar(value=skill_)
    skill_onoff = tk.IntVar(value = 0)
    skillbuttons.append(ttk.Checkbutton(skills_frame, text = skill_, variable = skill_onoff, offvalue =0, onvalue = 1, state = 'selected disabled', command=lambda x=skill_, y=skill_onoff: select_skillstyle(x, y)))
    skillbuttons[i].grid(row=i%nrows, column=i//nrows, padx=5, pady=10, sticky="nsew")


# Notes entry
notes_var = tk.StringVar()
notes_entry_widget = ttk.Entry(frm, textvariable=notes_var) # location entry box
notes_entry_widget.grid(row=1, column =1)
new_label = ttk.Label(frm, text="Notes :", justify="left")
new_label.grid(row=1, column=0, pady=10, columnspan=1)


# Enter all details
def get_info_holdwallskillnotes():
    climb_data['hold'] = ', '.join(holdstyles)
    climb_data['wall'] = ', '.join(wallstyles)
    climb_data['skill'] = ', '.join(skillstyles)
    climb_data['notes'] = notes_var.get()
    print(climb_data)

enter_extra_info_button_widget = tk.Button(frm, text="Submit Climb Details", command = get_info_holdwallskillnotes)
enter_extra_info_button_widget.grid(row=3, column=1)

frm.pack(expand=True, fill="both", padx=5, pady=5)

# Sizegrip
sizegrip = ttk.Sizegrip(root)
sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))

# Center the window, and set minsize
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
x_cordinate = int((root.winfo_screenwidth()/2) - (root.winfo_width()/2))
y_cordinate = int((root.winfo_screenheight()/2) - (root.winfo_height()/2))
root.geometry("+{}+{}".format(x_cordinate, y_cordinate))


# submit data to file
def check_buttons():
    print(climb_data)
    bc.add_new_climb_to_file(fpath, climb_data)
    root.destroy()

submit_button_widget = tk.Button(frm, text="Done", command = check_buttons)
submit_button_widget.grid(row=4, column=1)

# execute GUI
root.mainloop()

