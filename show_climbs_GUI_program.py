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
import copy
#%%
# define file to add attempts to 
dirpath = os.path.join(os.getcwd(), 'sample_data')
fname = 'sample_climbs.csv'
fpath = os.path.join(dirpath, fname)

root = tk.Tk() # create GUI window, initialize instance of Tk class
root.title("Show Selected Climbs")
root.option_add("*tearOff", False) # This is always a good idea

# define file for importing tcl theme
tcl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme", "forest-light.tcl")
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
topfrm = ttk.Frame(top_pane)
for j in range(3):
    topfrm.columnconfigure(index=j, weight=1)
for j in range(3):
    topfrm.rowconfigure(index = j, weight =1)

#######
# top tab : basic categories
def sport_switch():
    global sport
    if sport:
        sport = False
    else:
        sport = True


basicsfrm = ttk.LabelFrame(topfrm, text="Basic", padding=(20, 10))
basicsfrm.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="nsew")
for j in range(3):
    basicsfrm.columnconfigure(index=j, weight=1)
for j in range(3):
    basicsfrm.rowconfigure(index = j, weight =1)

sportsfrm = ttk.LabelFrame(topfrm, text="Sport", padding=(20, 10))
sportsfrm.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")
for j in range(3):
    sportsfrm.columnconfigure(index=j, weight=1)
for j in range(3):
    sportsfrm.rowconfigure(index = j, weight =1)

outfrm = ttk.LabelFrame(topfrm, text="Outdoor", padding=(20, 10))
outfrm.grid(row=0, column=1, padx=(20, 10), pady=10, sticky="nsew")
for j in range(3):
    outfrm.columnconfigure(index=j, weight=1)
for j in range(3):
    outfrm.rowconfigure(index = j, weight =1)

mbfrm = ttk.LabelFrame(topfrm, text="Moonboard", padding=(20, 10))
mbfrm.grid(row=1, column=1, padx=(20, 10), pady=10, sticky="nsew")
for j in range(3):
    mbfrm.columnconfigure(index=j, weight=1)
for j in range(4):
    mbfrm.rowconfigure(index = j, weight =1)

selection_dict = {}
def select_category(x, y, z):
    if y.get() == 0: # check if button already selected or not
        try:
            del selection_dict[z]
        except KeyError:
            pass
    else:
        selection_dict[z] =x.get()
    print(selection_dict)

display_dict = {('grade', 'labeltext'): 'Grade :',
                ('grade', 'frame'): basicsfrm,
                ('grade', 'row'): 0,
                ('location', 'labeltext'): 'Location :',
                ('location', 'frame'): basicsfrm,
                ('location', 'row'): 1,
                ('name_outdoor', 'labeltext'): 'Name :',
                ('name_outdoor', 'frame'): outfrm,
                ('name_outdoor', 'row'): 1,
                ('name_mb', 'labeltext'): 'Name :',
                ('name_mb', 'frame'): mbfrm,
                ('name_mb', 'row'): 2,
                ('rope', 'labeltext'): 'Rope :',
                ('rope', 'frame'): sportsfrm,
                ('rope', 'row'): 1,
                ('rock_type', 'labeltext'): 'Rock Type :',
                ('rock_type', 'frame'): outfrm,
                ('rock_type', 'row'): 0,
                ('angle', 'labeltext'): 'Angle :',
                ('angle', 'frame'): mbfrm,
                ('angle', 'row'):1,
                ('mbyear', 'labeltext'): 'Year :',
                ('mbyear', 'frame'): mbfrm,
                ('mbyear', 'row'):0,
            }
values_dict = {('grade', 'var'): tk.StringVar(),
               ('grade', 'onoff'): tk.IntVar(value = 0),
               ('grade', 'keyname'): 'grade',
               ('location', 'var'): tk.StringVar(),
               ('location', 'onoff'): tk.IntVar(value = 0),
               ('location', 'keyname'): 'location',
               ('name_outdoor', 'var'): tk.StringVar(),
               ('name_outdoor', 'onoff'): tk.IntVar(value = 0),
               ('name_outdoor', 'keyname'): 'climb_name',
               ('name_mb', 'var'): tk.StringVar(),
               ('name_mb', 'onoff'): tk.IntVar(value = 0),
               ('name_mb', 'keyname'): 'climb_name',
               ('rope', 'var'): tk.StringVar(),
               ('rope', 'onoff'): tk.IntVar(value = 0),
               ('rope', 'keyname'): 'rope',
               ('rope', 'dropdownvalues'): bc.ropes,
               ('rock_type', 'var') : tk.StringVar(),
               ('rock_type', 'onoff'): tk.IntVar(value = 0),
               ('rock_type', 'keyname'): 'rock_type',
               ('rock_type', 'dropdownvalues'): bc.rock_types,
               ('angle', 'var'): tk.StringVar(),
               ('angle', 'onoff'): tk.IntVar(value = 0),
               ('angle', 'keyname'): 'angle',
               ('angle', 'dropdownvalues'): bc.angles,
               ('mbyear', 'var'): tk.StringVar(),
               ('mbyear', 'onoff'): tk.IntVar(value = 0),
               ('mbyear', 'keyname'):'mbyear',
               ('mbyear', 'dropdownvalues'): bc.mbyears,
            }

for k in ['grade', 'location', 'name_outdoor', 'name_mb']:
    display_dict[(k, 'entrywidget')] = ttk.Entry(display_dict[(k, 'frame')], textvariable=values_dict[(k, 'var')]) # location entry box
    display_dict[(k, 'entrywidget')].grid(row=display_dict[(k, 'row')], column = 1)
    display_dict[(k, 'entrywidgetlabel')] = ttk.Label(display_dict[(k, 'frame')], text=display_dict[(k, 'labeltext')], justify="left")
    display_dict[(k, 'entrywidgetlabel')].grid(row=display_dict[(k, 'row')], column=0, pady=10, columnspan=1)
    display_dict[(k, 'checkbuttonwidget')] = ttk.Checkbutton(display_dict[(k, 'frame')], variable = values_dict[(k, 'onoff')], offvalue =0, onvalue = 1, command=lambda x=values_dict[(k, 'var')], y=values_dict[(k, 'onoff')], z = values_dict[(k, 'keyname')]: select_category(x, y, z))
    display_dict[(k, 'checkbuttonwidget')].grid(row=display_dict[(k, 'row')], column=2, padx=5, pady=10, sticky="nsew")

for k in ['rope', 'rock_type', 'angle', 'mbyear']:
    display_dict[(k, 'entrywidget')] = ttk.Combobox(display_dict[(k, 'frame')], textvariable=values_dict[(k, 'var')], values = values_dict[(k, 'dropdownvalues')])
    display_dict[(k, 'entrywidget')].current(1) # sets intial/default selection to 0 index of values list
    display_dict[(k, 'entrywidget')].grid(row=display_dict[(k, 'row')], column=1, padx=5, pady=10,  sticky="ew")
    display_dict[(k, 'entrywidgetlabel')] = ttk.Label(display_dict[(k, 'frame')], text=display_dict[(k, 'labeltext')], justify="left")
    display_dict[(k, 'entrywidgetlabel')].grid(row=display_dict[(k, 'row')], column=0, pady=10, columnspan=1)
    display_dict[(k, 'checkbuttonwidget')] = ttk.Checkbutton(display_dict[(k, 'frame')], variable = values_dict[(k, 'onoff')], offvalue =0, onvalue = 1, command=lambda x=values_dict[(k, 'var')], y=values_dict[(k, 'onoff')], z = values_dict[(k, 'keyname')]: select_category(x, y,z))
    display_dict[(k, 'checkbuttonwidget')].grid(row=display_dict[(k, 'row')], column=2, padx=5, pady=10, sticky="nsew")


#Indoor Outdoor Moonboard
in_onoff = tk.IntVar(value = 0)
in_filter = ttk.Checkbutton(basicsfrm, text = 'Indoor', variable = in_onoff, offvalue =0, onvalue = 1)#ommand=lambda x=wall_, y=wall_onoff: select_wallstyle(x, y)))
in_filter.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
out_onoff = tk.IntVar(value = 0)
out_filter = ttk.Checkbutton(basicsfrm, text = 'Outdoor',variable = out_onoff, offvalue =0, onvalue = 1)#ommand=lambda x=wall_, y=wall_onoff: select_wallstyle(x, y)))
out_filter.grid(row=2, column=1, padx=5, pady=10, sticky="nsew")
mb_onoff = tk.IntVar(value = 0)
mb_filter = ttk.Checkbutton(basicsfrm, text = 'Moonboard', variable = mb_onoff, offvalue =0, onvalue = 1)#ommand=lambda x=wall_, y=wall_onoff: select_wallstyle(x, y)))
mb_filter.grid(row=2, column=2, padx=5, pady=10, sticky="nsew")

# Sport switch
sportswitch = ttk.Checkbutton(sportsfrm, style="Switch", command = sport_switch)
sportswitch.grid(row=0, column=1)#, padx=5, pady=10, sticky="w")
sport_label = ttk.Label(sportsfrm, text= 'Sport?', justify = 'left')
sport_label.grid(row=0, column=0, pady=10, columnspan = 1)
sport_onoff = tk.IntVar(value = 0)
sport_filter = ttk.Checkbutton(sportsfrm, variable = sport_onoff, offvalue =0, onvalue = 1,)#ommand=lambda x=wall_, y=wall_onoff: select_wallstyle(x, y)))
sport_filter.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")

topfrm.pack(expand=True, fill="both", padx=5, pady=5)

###########
# bottom pane - styles and notes
frm = ttk.Frame(bottom_pane)
frm.columnconfigure(index=0, weight=1)
frm.columnconfigure(index=1, weight=1)
frm.columnconfigure(index=2, weight=1)
for j in range(5):
    frm.rowconfigure(index = j, weight =1)
# bottom_pane.add(frm, text="Notes and styles")

# Create a Frame for the hold, wall and skill types
holdsfrm = ttk.LabelFrame(frm, text="Hold Types", padding=(20, 10))
holdsfrm.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="nsew")
for j in range(2):
    holdsfrm.columnconfigure(index = j, weight =1)
for j in range(3):
    holdsfrm.rowconfigure(index = j, weight =1)

wallsfrm = ttk.LabelFrame(frm, text="Wall Types", padding=(20, 10))
wallsfrm.grid(row=0, column=1, padx=(20, 10), pady=10, sticky="nsew")
for j in range(2):
    wallsfrm.columnconfigure(index = j, weight =1)
for j in range(3):
    wallsfrm.rowconfigure(index = j, weight =1)

skillsfrm = ttk.LabelFrame(frm, text="Skill Types", padding=(20, 10))
skillsfrm.grid(row=0, column=2, padx=(20, 10), pady=10, sticky="nsew")
for j in range(2):
    skillsfrm.columnconfigure(index = j, weight =1)
for j in range(3):
    skillsfrm.rowconfigure(index = j, weight =1)

display_dict.update({('hold', 'frame'): holdsfrm,
                ('wall', 'frame'): wallsfrm,
                ('skill', 'frame'): skillsfrm,
                })
values_dict.update({('hold', 'dropdownvalues'): bc.holds,
                    ('hold', 'keyname'): 'hold',
                    ('wall', 'dropdownvalues'): bc.walls,
                    ('wall', 'keyname'): 'wall',
                    ('skill', 'dropdownvalues'): bc.skills,
                    ('skill', 'keyname'): 'skill',
                    })

def select_style(x, y, z):
    if y.get()==0:
        try:
            values_dict[(z, 'checkedstyles')].remove(x.get())
        except KeyError:
            pass
    else:
        values_dict[(z, 'checkedstyles')].append(x.get())
    print(values_dict[(z, 'checkedstyles')])

for k in ['hold', 'wall', 'skill']:
    display_dict[(k, 'buttons')] = []
    nrows = 5
    values_dict[(k, 'checkedstyles')] = []
    for i, ddv in enumerate(values_dict[((k, 'dropdownvalues'))]):
        values_dict[(k, 'var')] = tk.StringVar(value=ddv)
        values_dict[(k, 'onoff')] = tk.IntVar(value = 0)
        display_dict[(k, 'buttons')].append(ttk.Checkbutton(display_dict[(k, 'frame')], text = ddv, variable = values_dict[(k, 'onoff')], offvalue =0, onvalue = 1, state = 'selected disabled', command=lambda x=values_dict[(k, 'var')], y=values_dict[(k, 'onoff')], z = values_dict[(k, 'keyname')]: select_style(x, y, z)))
        display_dict[(k, 'buttons')][i].grid(row=i%nrows, column=i//nrows, padx=5, pady=10, sticky="nsew")


# Enter information button
def get_info():
    global sport
    g = values_dict[('grade', 'var')].get()
    try:
        if not re.match(bc.Vgrades_regex_pattern, g) and not re.match(bc.Vgrades_range_regex_pattern, g) and not re.match(bc.font_grades_regex_pattern, g):
            raise Exception("Invalid regex pattern")
        else:
            climb_data['grade'] = values_dict[('grade', 'var')].get()
    except Exception as e:
        print(e)
        print(f'{g} is not a valid font, V or V range grade')
    climb_data['location'] = values_dict[('location', 'var')].get()
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
        climb_data['rope'] = values_dict[('rope', 'var')].get()
    
    for k in ['hold', 'wall', 'skill']:
        climb_data[k] = ', '.join(values_dict[(k, 'checkedstyles')])
    print(climb_data)
    root.destroy()

enterinfo_button_widget = tk.Button(frm, text="Search corresponding climbs", command = get_info)
enterinfo_button_widget.grid(row=4, column=1)


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

# execute GUI
root.mainloop()




#%%

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

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
        label = tk.Label(self, text="This is the start page")
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
        label = tk.Label(self, text="This is page 1")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()