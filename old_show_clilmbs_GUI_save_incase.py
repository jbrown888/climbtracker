# Grade entry
grade_var = tk.StringVar()
grade_onoff = tk.IntVar(value = 0)
grade_var = tk.StringVar()
gradeentry_widget = ttk.Entry(basicsfrm, textvariable=grade_var) # location entry box
gradeentry_widget.grid(row=0, column =1)
gew_label = ttk.Label(basicsfrm, text="Grade :", justify="left")
gew_label.grid(row=0, column=0, pady=10, columnspan=1)
grade_onoff = tk.IntVar(value = 0)
grade_filter = ttk.Checkbutton(basicsfrm, text=grade_var, variable = grade_onoff, offvalue =0, onvalue = 1, command=lambda x=grade_var, y=grade_onoff: select_category(x, y))
grade_filter.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")
# Location entry
location_var = tk.StringVar()
locationentry_widget = ttk.Entry(basicsfrm, textvariable=location_var) # location entry box
locationentry_widget.grid(row=1, column =1)
lew_label = ttk.Label(basicsfrm, text="Location :", justify="left")
lew_label.grid(row=1, column=0, pady=10, columnspan=1)
loc_onoff = tk.IntVar(value = 0)
loc_filter = ttk.Checkbutton(basicsfrm, variable = loc_onoff, offvalue =0, onvalue = 1,)#ommand=lambda x=wall_, y=wall_onoff: select_wallstyle(x, y)))
loc_filter.grid(row=1, column=2, padx=5, pady=10, sticky="nsew")

# Rope option for sport
ropevar = tk.StringVar()
ropebox = ttk.Combobox(sportsfrm, textvariable=ropevar, values=bc.ropes)
ropebox.current(1) # sets intial/default selection to 0 index of values list
ropebox.grid(row=1, column=1, padx=5, pady=10,  sticky="ew")
rope_label = ttk.Label(sportsfrm, text="Rope style :", justify="left")
rope_label.grid(row=1, column=0, pady=10, columnspan=1)
rope_onoff = tk.IntVar(value = 0)
rope_filter = ttk.Checkbutton(sportsfrm, variable = rope_onoff, offvalue =0, onvalue = 1,)#ommand=lambda x=wall_, y=wall_onoff: select_wallstyle(x, y)))
rope_filter.grid(row=1, column=2, padx=5, pady=10, sticky="nsew")



# Name entry
name_var_2 = tk.StringVar()
nameentry_widget_2 = ttk.Entry(outfrm, textvariable=name_var_2) # location entry box
nameentry_widget_2.grid(row=1, column =1)
new_label_2 = ttk.Label(outfrm, text="Name :", justify="left")
new_label_2.grid(row=1, column=0, pady=10, columnspan=1)
name_out__onoff = tk.IntVar(value = 0)
name_out__filter = ttk.Checkbutton(outfrm, variable = name_out__onoff, offvalue =0, onvalue = 1,)#ommand=lambda x=wall_, y=wall_onoff: select_wallstyle(x, y)))
name_out__filter.grid(row=1, column=2, padx=5, pady=10, sticky="nsew")

# Name entry
name_var_2 = tk.StringVar()
nameentry_widget_2 = ttk.Entry(mbfrm, textvariable=name_var_2) # location entry box
nameentry_widget_2.grid(row=2, column =1)
new_label_2 = ttk.Label(mbfrm, text="Name :", justify="left")
new_label_2.grid(row=2, column=0, pady=10, columnspan=1)
name_mb_onoff = tk.IntVar(value = 0)
name_mb_filter = ttk.Checkbutton(mbfrm, variable = name_mb_onoff, offvalue =0, onvalue = 1,)#ommand=lambda x=wall_, y=wall_onoff: select_wallstyle(x, y)))
name_mb_filter.grid(row=2, column=2, padx=5, pady=10, sticky="nsew")

# Rock type
rock_var_2 = tk.StringVar()
rockbox_2 = ttk.Combobox(outfrm, textvariable= rock_var_2, values=bc.rock_types)
rockbox_2.current(0) # sets intial/default selection to 0 index of values list
rockbox_2.grid(row=0, column=1, padx=5, pady=10,  sticky="ew")
rock_label_2 = ttk.Label(outfrm, text="Rock type :", justify="left")
rock_label_2.grid(row=0, column=0, pady=10, columnspan=1)
rock_onoff = tk.IntVar(value = 0)
rock_filter = ttk.Checkbutton(outfrm, variable = rock_onoff, offvalue =0, onvalue = 1,)#ommand=lambda x=wall_, y=wall_onoff: select_wallstyle(x, y)))
rock_filter.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")


# Year option
year_var_3 = tk.StringVar()
yearbox_3 = ttk.Combobox(mbfrm, textvariable=year_var_3, values= bc.mbyears)
yearbox_3.current(1) # sets intial/default selection to 0 index of values list
yearbox_3.grid(row=0, column=1, padx=5, pady=10,  sticky="ew")
year_label_3 = ttk.Label(mbfrm, text="Year :", justify="left")
year_label_3.grid(row=0, column=0, pady=10, columnspan=1)
year_onoff = tk.IntVar(value = 0)
year_filter = ttk.Checkbutton(mbfrm, variable = year_onoff, offvalue =0, onvalue = 1,)#ommand=lambda x=wall_, y=wall_onoff: select_wallstyle(x, y)))
year_filter.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")
# Angle option
angle_var_3 = tk.StringVar()
anglebox_3 = ttk.Combobox(mbfrm, textvariable=angle_var_3, values= bc.angles)
anglebox_3.current(1) # sets intial/default selection to 0 index of values list
anglebox_3.grid(row=1, column=1, padx=5, pady=10,  sticky="ew")
angle_label_3 = ttk.Label(mbfrm, text="Angle :", justify="left")
angle_label_3.grid(row=1, column=0, pady=10, columnspan=1)
angle_onoff = tk.IntVar(value = 0)
angle_filter = ttk.Checkbutton(mbfrm, variable = angle_onoff, offvalue =0, onvalue = 1,)#ommand=lambda x=wall_, y=wall_onoff: select_wallstyle(x, y)))
angle_filter.grid(row=1, column=2, padx=5, pady=10, sticky="nsew")


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
    # print(holdstyles)

for i, hold_ in enumerate(bc.holds):
    hold_var = tk.StringVar(value=hold_)
    hold_onoff = tk.IntVar(value = 0)
    holdbuttons.append(ttk.Checkbutton(holds_frame, text = hold_, variable = hold_onoff, offvalue =0, onvalue = 1, state = 'selected disabled', command=lambda x=hold_, y=hold_onoff: select_holdstyle(x, y)))
    holdbuttons[i].grid(row=i%nrows, column=i//nrows, padx=5, pady=10, sticky="nsew")

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

