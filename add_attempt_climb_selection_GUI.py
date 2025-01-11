"""
@author: jbrown888
19/7/24
Creates GUI that allows user to add attempt on climb, and finds climb id or allows creation of new climb
"""
from tkinter import ttk
import os
import tkinter as tk
import broomcupboard as bc
import datetime as dt
import pandas as pd
# import csv
import re
import copy
#%%
class MultiFrameRoot(tk.Tk):
    def __init__(self, *args, **kwargs):
        """
        Initialize the main application window.

        Parameters:
        *args: Variable length argument list. These arguments are passed to the parent class initializer.
        **kwargs: Arbitrary keyword arguments. These arguments are passed to the parent class initializer.

        Returns:
        None
        """        
        # Call the parent class initializer, Tk class
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Show Selected Climbs")
        self.option_add("*tearOff", False) # This is always a good idea

        # define file for importing tcl theme
        tcl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme", "forest-light.tcl")
        # set theme, import the tcl file
        style = ttk.Style(self) 
        self.tk.call("source", tcl_path)
        style.theme_use("forest-light")

        # container contains stacked frames - can raise one above others to be visible
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to hold each page. The keys are the page names, and the values are the corresponding frames.
        self.frames = {}
        for F in (AddAttemptPage,):#, DisplayPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            # F is the loop variable. 
            # The loop is iterating over a list of classes, so each time through the loop F will be representing a class. 
            # F(...) creates an instance of the class. 
            # These classes (SelectionPage, DisplayPage) all require two parameters: a widget that will be the parent of this class//
            # and an object that will server as a controller (a term borrowed from the UI patter model/view/controller).
            # The line of code creates an instance of the class (which itself is a subclass of a Frame widget)//
            # and temporarily assigns the frame to the local variable frame.
            # passing self as parameter means these new class instances can call methods in MultiFrameRoot class

            self.frames[page_name] = frame # can access page through dictionary self.frames
            frame.grid(row=0, column=0, sticky="nsew") # frames at same location - stacking order decides which is visible

        # self.findclimbsframes = {}
        # for F in (SelectionPage, DisplayPage):
        #     page_name = F.__name__
        #     frame = F(parent=container, controller=self)
        #     self.findclimbsframes[page_name] = frame # can access page through dictionary self.frames
        #     frame.grid(row=0, column=0, sticky="nsew") # frames at same location - stacking order decides which is visible

        self.selection_dict = {} # initialize dictionary for storing criteria, accessible by SelectionPage and DisplayPage through controller
        dirpath = os.path.join(os.getcwd(), 'real_data')
        climbsfname = 'climbs_data.csv'
        attemptsfname = 'attempts_data.csv'
        self.climbsfpath = os.path.join(dirpath, climbsfname) # filepath to climbs data file
        self.attemptsfpath = os.path.join(dirpath, attemptsfname) # filepath to attempts data file

        self.show_frame("AddAttemptPage") # sets initial visible frame
        self.update()

        # defining geometry of window
        self.minsize(self.winfo_width(), self.winfo_height())
        x_cordinate = int((self.winfo_screenwidth()/2) - (self.winfo_width()/2))
        y_cordinate = int((self.winfo_screenheight()/2) - (self.winfo_height()/2))
        self.geometry("+{}+{}".format(x_cordinate, y_cordinate))

    def show_frame(self, page_name):
        """
        Show a frame for the given page name.

        Parameters:
        page_name (str): The name of the page to show.

        Returns:
        None. This function raises the frame associated with page_name to the top of the stacking order.
        """
        # zorder
        frame = self.frames[page_name]
        frame.tkraise() # raises frame to the top of the stacking order
        # each page is subclass of tk.Frame (SelectionPage, DisplayPage, PageTwo)
        # so tk.Frame.__init__(self,parent) calls constructor of parent class

        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())
        x_cordinate = int((self.winfo_screenwidth()/2) - (self.winfo_width()/2))
        y_cordinate = int((self.winfo_screenheight()/2) - (self.winfo_height()/2))
        self.geometry("+{}+{}".format(x_cordinate, y_cordinate))

    def update_selection_dict(self, key_, v):
        """
        Update the self.selection_dict with key-value pair
    
        Parameters:
        key_ (str): key to add
        v (list): value to add
    
        Returns:
        None. The selection dictionary is updated in-place.
        """
        self.selection_dict[key_] = v
    
    def remove_kvpair_selection_dict(self, key_):
        """
        Removes a key-value pair from self.selection_dict based on the provided key.

        Parameters:
        key_ (str): The key of the key-value pair to be removed.

        Returns:
        None. The function modifies the selection_dict in-place.
        """        
        try:
            del self.selection_dict[key_]
        except KeyError:
            pass

    def recalculate_display_climbs(self):
        """
        Recalculates the dataframe of climbs to display based on the current selection criteria.

        Parameters:
        self 

        Returns:
        filtered_climbs_df (DataFrame): A dataframe containing the filtered climbs based on the selection criteria.
        display_columns (list): A list of str of column names to display
        """        
        self.climbs_df = pd.read_csv(self.climbsfpath, header=0,\
                 index_col =0, dtype=None, engine=None, converters={'climb_id':int},\
                 skipinitialspace=True, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True,\
                 na_filter=True, parse_dates=None, comment='#')
        # with open(self.controller.fpath, "r") as climbsfile:
        #     reader = csv.reader(climbsfile, delmitier = ',', )
        #     data = list(reader)

        # set empty rows to empty strings in these columns
        fill_na_values = {'hold':'', 'wall':'', 'skill':'', 'notes':''}
        self.climbs_df = self.climbs_df.fillna(value = fill_na_values)

        display_columns = self.calculate_columns_to_show() # returns list of columns to display
        filtered_climbs_df = bc.get_filtered_climbs(self.climbs_df, self.selection_dict) # returns dataframe filtered based on selection criteria

        return filtered_climbs_df, display_columns

    def calculate_columns_to_show(self):
        """
        Based on current self.selection_dict, calculates and returns the column names that should be displayed
        (excluding climb_id)

        Parameters:
        self

        Returns:
        list: A list of str of column names to be displayed.
        """
        dont_always_display_keys = ['climb_style', 'door', 'location', 'rope', 'climb_name', 'angle', 'mbyear', 'rock_type'] # columns not always displayed
        always_display_keys = ['climb_id', 'grade', 'hold', 'wall', 'skill', 'notes']
        display_columns = [k for k in bc.climb_file_columns[1:]] # bc.climb_file_columns names excluding climb_id

        # delete selection keys that appear in selection_dict from display_columns
        # ie if all selected climbs have rock type granite, no point displaying this column
        for k in self.selection_dict.keys():
            if k in dont_always_display_keys:
                try:
                    display_columns.remove(k)
                except ValueError:
                    pass
        
        # columns to delete from display_columns based on selection criteria
        # eg all moonboard climbs have rope=nan, no point displaying this column
        dict_try_to_delete_display_keys = {
            ('climb_style', 'bouldering') : ['rope'],
            ('climb_style', 'sport') : ['angle', 'mbyear'],
            ('door', 'indoor') : ['climb_name', 'angle', 'mbyear', 'rock_type'],
            ('door', 'outdoor') : ['angle', 'mbyear'],
            ('door', 'moonboard') : ['rock_type', 'rope'],
            ('rope') : ['angle', 'mbyear'],
            ('rock_type') : ['angle', 'mbyear', 'door'],
            ('angle') : ['rock_type', 'style', 'door', 'rope'],
            ('mbyear') : ['rock_type', 'style', 'door', 'rope'],
        }
        for k in ['climb_style', 'door', 'rope', 'rock_type', 'angle', 'mbyear']:
            if k in self.selection_dict.keys():
                if k in ['climb_style', 'door']:
                    kk = (k, self.selection_dict[k][0])
                else:
                    kk = (k)
                for j in dict_try_to_delete_display_keys[kk]:
                    try:
                        # column name may have already been deleted from display_columns
                        # we don't care if it has been, so catch and ignore ValueError
                        display_columns.remove(j)
                    except ValueError:
                        pass

        return(display_columns)
    
    def find_climbid(self):
        self.toplevels = {}
        self.toplevels['NewClimbWindow'] = NewClimbWindow(controller = self)

    def addnewclimb(self):
        self.toplevels['NewClimbWindow'].destroy()
        self.toplevels['AddNewClimbPage'] = AddNewClimbPage(controller = self)
        self.newclimbdata = {}

    def findclimb(self):
        self.toplevels['NewClimbWindow'].destroy()

        # container contains stacked frames - can raise one above others to be visible
        self.findclimbcontainer = tk.Toplevel()
        # self.findclimbcontainer.pack(side="top", fill="both", expand=True)
        self.findclimbcontainer.grid_rowconfigure(0, weight=1)
        self.findclimbcontainer.grid_columnconfigure(0, weight=1)

        self.findclimbsframes = {}
        for F in (SelectionPage, DisplayPage):
            page_name = F.__name__
            frame = F(parent=self.findclimbcontainer, controller=self)
            self.findclimbsframes[page_name] = frame # can access page through dictionary self.frames
            frame.grid(row=0, column=0, sticky="nsew") # frames at same location - stacking order decides which is visible

        self.show_findclimbframe("SelectionPage") # sets initial visible frame


    def show_findclimbframe(self, page_name):
        """
        Show a frame for the given page name.

        Parameters:
        page_name (str): The name of the page to show.

        Returns:
        None. This function raises the frame associated with page_name to the top of the stacking order.
        """
        # zorder
        frame = self.findclimbsframes[page_name]
        frame.tkraise() # raises frame to the top of the stacking order
        # each page is subclass of tk.Frame (SelectionPage, DisplayPage, PageTwo)
        # so tk.Frame.__init__(self,parent) calls constructor of parent class

        self.findclimbcontainer.update()
        # self.minsize(self.winfo_width(), self.winfo_height())
        # x_cordinate = int((self.winfo_screenwidth()/2) - (self.winfo_width()/2))
        # y_cordinate = int((self.winfo_screenheight()/2) - (self.winfo_height()/2))
        # self.geometry("+{}+{}".format(x_cordinate, y_cordinate))

    def return_to_attempts(self):
        self.findclimbcontainer.destroy()
        self.frames['AddAttemptPage'].climbid_var.set(self.selectedclimbid)
        print(self.selectedclimbid)

    def submit_new_climb(self):
        self.toplevels['AddNewClimbPage'].destroy()
        print(self.newclimbdata)
        self.selectedclimbid = bc.add_new_climb_to_file(self.climbsfpath, self.newclimbdata, returnclimbid = True)
        self.frames['AddAttemptPage'].climbid_var.set(self.selectedclimbid)


class AddAttemptPage(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialize the AddAttemptPage with parent widget and controller object.

        Parameters:
        parent (tk.Widget): The parent widget for the AddAttemptPage.
        controller (MultiFrameRoot): The controller object that manages the application's frames.

        Returns:
        None
        """        
        # Call parent class constructor, tk.Frame
        tk.Frame.__init__(self, parent) # parent is parent widget
        self.controller = controller # MultiFrameRoot object

        # set rows and columns of base frame of page. weight = 1 : even distribution
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)


        # initialize global variables
        date_entered = False
        climb_entered = False
        send_status_entered = False
        sent_status = False
        attempts_data = {}


        self.controller.title("Input attempt data") # set title
        
        # Panedwindow
        paned = ttk.PanedWindow(self)
        paned.grid(row=0, column=0, pady=(10,20), sticky="nsew", rowspan=2)
        # pady adds padding (top, bottom) to widget in pixels
        # nsew makes it expand in n s e w directions
        # rowspan specifies paned widget should open 2 rows in root window

        # Add top pane
        top_pane = ttk.Frame(paned)
        paned.add(top_pane, weight=1)
        
        frm = ttk.Frame(top_pane, padding=40) # creates frame widget
        for j in range(11):
            frm.rowconfigure(index=1, weight=1)
        for j in range(3):
            frm.columnconfigure(index=1, weight=1)
        frm.grid()

        # Create text entry widget for defining date
        default_date = '2024-12-14' #dt.date.today().isoformat()
        self.date_var = tk.StringVar(value = default_date) # store str variable of date
        dateentry_widget = ttk.Entry(frm, textvariable=self.date_var) # date entry box
        dateentry_widget.grid(column =0, row = 0) # set position
        self.date_var.set(default_date)
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
        self.climbid_var = tk.IntVar() # int var to store climb_id
        climbentry_widget = ttk.Entry(frm, textvariable=self.climbid_var) # climb id entry box
        climbentry_widget.grid(row =1, column =0)
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


        dontknowclimbid_button_widget = tk.Button(frm, text="Don't know climb id?", command = lambda: self.controller.find_climbid())
        dontknowclimbid_button_widget.grid(row=2, column=1)


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
        sent_button_widget.grid(row=3, column=0)
        tried_button_widget = tk.Button(frm, text="Tried", command = try_climb)
        tried_button_widget.grid(row=3, column=1)

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
        tries_label.grid(row = 4, column = 1)
        add_try_button_widget = tk.Button(frm, text = '+', command = add_try) # add try button
        add_try_button_widget.grid(row = 5, column = 2)
        remove_try_button_widget = tk.Button(frm, text = '-', command = remove_try) # remove try button
        remove_try_button_widget.grid(row = 5, column = 0)
        display_tries_widget = tk.Label(frm, textvariable=try_counter)
        display_tries_widget.grid(row = 5, column = 1)


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
                    bc.add_N_attempts_send_final_try_on_one_climb_same_date(self.controller.attemptsfpath, **attempts_data)
                    pass
                else:
                    # if climb not sent
                    bc.add_N_failed_attempts_on_one_climb_same_date(self.controller.attemptsfpath, **attempts_data)
                    pass
                self.controller.destroy()

        submit_button_widget = tk.Button(frm, text="Done", command = check_buttons)
        submit_button_widget.grid(row=8, column=1)

        frm.pack(expand=True, fill="both", padx=5, pady=5) # pack and display bottom frame and all children

        # Sizegrip
        sizegrip = ttk.Sizegrip(self)
        sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))

class SelectionPage(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialize the SelectionPage with parent widget and controller object.

        Parameters:
        parent (tk.Widget): The parent widget for the SelectionPage.
        controller (MultiFrameRoot): The controller object that manages the application's frames.

        Returns:
        None
        """        # Call parent class constructor, tk.Frame
        tk.Frame.__init__(self, parent) # parent is parent widget
        self.controller = controller # MultiFrameRoot object

        # set rows and columns of base frame of page. weight = 1 : even distribution
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)

        # Panedwindow
        paned = ttk.PanedWindow(self)
        paned.grid(row=0, column=0, pady=(10,20), sticky="nsew", rowspan=2)
        # pady adds padding (top, bottom) to widget in pixels
        # nsew makes it expand in n s e w directions
        # rowspan specifies paned widget should open 2 rows in root window

        # Add top pane
        top_pane = ttk.Frame(paned)
        paned.add(top_pane, weight=1)
        # Add middle pane
        middle_pane = ttk.Frame(paned)
        paned.add(middle_pane, weight=1)
        # Add bottom pane
        bottom_pane = ttk.Frame(paned)
        paned.add(bottom_pane, weight = 1)

        # Configure columns in topfrm
        topfrm = ttk.Frame(top_pane)
        for j in range(2):
            topfrm.columnconfigure(index=j, weight=1)
        for j in range(2):
            topfrm.rowconfigure(index = j, weight =1)

        # Add four label frames to topfrm
        topfrmspadx = 20
        topfrmspady = 10

        basicsfrm = ttk.LabelFrame(topfrm, text="Basic", padding=(topfrmspadx, topfrmspady))
        basicsfrm.grid(row=0, column=0, padx=(20, 5), pady=5, sticky="nsew")
        for j in range(3):
            basicsfrm.columnconfigure(index=j, weight=1)
        for j in range(4):
            basicsfrm.rowconfigure(index = j, weight =1)

        sportsfrm = ttk.LabelFrame(topfrm, text="Sport", padding=(topfrmspadx, topfrmspady))
        sportsfrm.grid(row=1, column=0, padx=(20,5), pady=5, sticky="nsew")
        for j in range(3):
            sportsfrm.columnconfigure(index=j, weight=1)
        for j in range(1):
            sportsfrm.rowconfigure(index = j, weight =1)

        outfrm = ttk.LabelFrame(topfrm, text="Outdoor", padding=(topfrmspadx, topfrmspady))
        outfrm.grid(row=0, column=1, padx=(5, 20), pady=5, sticky="nsew")
        for j in range(3):
            outfrm.columnconfigure(index=j, weight=1)
        for j in range(3):
            outfrm.rowconfigure(index = j, weight =1)

        mbfrm = ttk.LabelFrame(topfrm, text="Moonboard", padding=(topfrmspadx, topfrmspady))
        mbfrm.grid(row=1, column=1, padx=(5, 20), pady=5, sticky="nsew")
        for j in range(3):
            mbfrm.columnconfigure(index=j, weight=1)
        for j in range(4):
            mbfrm.rowconfigure(index = j, weight =1)

        def select_category(x_var, y_onoff, z_keyname):
            """
            This function handles the selection of categories in the application. It adds or removes
            categories from the selection_dict depending on if checkbutton is selected or not

            Parameters:
            x_var (tk.StringVar): The variable containing the value to add to selection_dict.
            y_onoff (tk.IntVar): The variable indicating whether the button is selected (1) or not (0).
            z_keyname (str): The key name (one of bc.climb_file_columns) associated with the selected category.

            Returns:
            None
            """
            # if button being turned off, i.e. onoff==0, set to off
            if y_onoff.get() == 0: 
                self.controller.remove_kvpair_selection_dict(z_keyname) # delete key-value pair from selection_dict

            else:
                # button being turned on, onoff==1
                if z_keyname == 'grade':
                    try:
                        g = x_var.get()
                        # check grade input is valid
                        if not re.match(bc.Vgrades_regex_pattern, g) and not re.match(bc.Vgrades_range_regex_pattern, g) and not re.match(bc.font_grades_regex_pattern, g):
                            raise Exception("Invalid regex pattern")
                    except Exception as e:
                        print(e)
                        print(f'{g} is not a valid font, V or V range grade')
                    else:
                        self.controller.update_selection_dict(z_keyname, [x_var.get()]) # add key-value pair to selection_dict
                elif z_keyname == 'notes':
                    notes_as_list = [v.strip(' ') for v in x_var.get().split(',')]# split up str by commas and make list
                    self.controller.update_selection_dict(z_keyname, notes_as_list) # add key-value pair to selection_dict
                else:
                    self.controller.update_selection_dict(z_keyname, [x_var.get()]) # add key-value pair to selection_dict

            # print(self.controller.selection_dict)

        # dictionary of information for display
        self.display_dict = {('grade', 'labeltext'): 'Grade :',
                        ('grade', 'row'): 0,
                        ('location', 'labeltext'): 'Location :',
                        ('location', 'row'): 1,
                        ('name_outdoor', 'labeltext'): 'Name :',
                        ('name_outdoor', 'row'): 1,
                        ('name_mb', 'labeltext'): 'Name :',
                        ('name_mb', 'row'): 2,
                        ('rope', 'labeltext'): 'Rope :',
                        ('rope', 'row'): 0,
                        ('rock_type', 'labeltext'): 'Rock Type :',
                        ('rock_type', 'row'): 0,
                        ('angle', 'labeltext'): 'Angle :',
                        ('angle', 'row'):1,
                        ('mbyear', 'labeltext'): 'Year :',
                        ('mbyear', 'row'):0,
                        ('door', 'row'):2,
                        ('climb_style', 'labeltext'): 'Climb Type :', 
                        ('door', 'labeltext'): 'In/Out/MB :',
                        ('hold', 'labeltext'): 'Hold :',
                        ('wall', 'labeltext'): 'Wall :',
                        ('skill', 'labeltext'): 'Skill :',
                        ('notes', 'labeltext'): 'Notes :',
                    }

        # Set parent frames for the different categories
        for k in ['grade', 'location', 'door', 'climb_style']:
            self.display_dict[(k, 'frame')] = basicsfrm
        for k in ['name_outdoor', 'rock_type']:
            self.display_dict[(k, 'frame')] = outfrm
        for k in ['name_mb', 'angle', 'mbyear']:
            self.display_dict[(k, 'frame')] = mbfrm
        for k in ['rope']:
            self.display_dict[(k, 'frame')] = sportsfrm

        # Dictionary of information for adding to selection_dict
        values_dict = {('grade', 'keyname'): 'grade',
                    ('location', 'keyname'): 'location',
                    ('name_outdoor', 'keyname'): 'climb_name',
                    ('name_mb', 'keyname'): 'climb_name',
                    ('rope', 'keyname'): 'rope',
                    ('rope', 'dropdownvalues'): bc.ropes,
                    ('rock_type', 'keyname'): 'rock_type',
                    ('rock_type', 'dropdownvalues'): bc.rock_types,
                    ('angle', 'keyname'): 'angle',
                    ('angle', 'dropdownvalues'): bc.angles,
                    ('mbyear', 'keyname'):'mbyear',
                    ('mbyear', 'dropdownvalues'): bc.mbyears,
                    ('door', 'keyname'): 'door',
                    ('climb_style', 'keyname'): 'climb_style',
                    }
        for k in ['grade', 'location', 'name_outdoor', 'name_mb', 'rope', 'rock_type', 'angle', 'mbyear', 'door', 'climb_style']:
            values_dict[(k, 'var')] = tk.StringVar() # variable containing str to add as value to selection_dict
            values_dict[(k, 'onoff')] = tk.IntVar(value=0) # variable storing whethere associated checkbutton is selected (1) or not (0)

        # Create text entry widgets
        for k in ['grade', 'location', 'name_outdoor', 'name_mb']:
            self.display_dict[(k, 'entrywidget')] = ttk.Entry(self.display_dict[(k, 'frame')], textvariable=values_dict[(k, 'var')]) # text entry box
            self.display_dict[(k, 'entrywidget')].grid(row=self.display_dict[(k, 'row')], column = 1) # set position
            self.display_dict[(k, 'entrywidgetlabel')] = ttk.Label(self.display_dict[(k, 'frame')], text=self.display_dict[(k, 'labeltext')], justify="left") # label of text entry box
            self.display_dict[(k, 'entrywidgetlabel')].grid(row=self.display_dict[(k, 'row')], column=0, pady=5, columnspan=1) # set position
            self.display_dict[(k, 'checkbuttonwidget')] = ttk.Checkbutton(self.display_dict[(k, 'frame')], variable = values_dict[(k, 'onoff')], offvalue =0, onvalue = 1, command=lambda x=values_dict[(k, 'var')], y=values_dict[(k, 'onoff')], z = values_dict[(k, 'keyname')]: select_category(x, y, z)) # checkbutton widget
            self.display_dict[(k, 'checkbuttonwidget')].grid(row=self.display_dict[(k, 'row')], column=2, padx=5, pady=5, sticky="nsew") # set position

        # Create dropdown menu widgets
        for k in ['rope', 'rock_type', 'angle', 'mbyear']:
            self.display_dict[(k, 'entrywidget')] = ttk.Combobox(self.display_dict[(k, 'frame')], textvariable=values_dict[(k, 'var')], values = values_dict[(k, 'dropdownvalues')]) # dropdown selection widget
            self.display_dict[(k, 'entrywidget')].current(0) # sets intial/default selection to 0 index of values list
            self.display_dict[(k, 'entrywidget')].grid(row=self.display_dict[(k, 'row')], column=1, padx=5, pady=5,  sticky="ew") # set position
            self.display_dict[(k, 'entrywidgetlabel')] = ttk.Label(self.display_dict[(k, 'frame')], text=self.display_dict[(k, 'labeltext')], justify="left") # label of dropdown widget
            self.display_dict[(k, 'entrywidgetlabel')].grid(row=self.display_dict[(k, 'row')], column=0, pady=5, columnspan=1) # set position
            self.display_dict[(k, 'checkbuttonwidget')] = ttk.Checkbutton(self.display_dict[(k, 'frame')], variable = values_dict[(k, 'onoff')], offvalue =0, onvalue = 1, command=lambda x=values_dict[(k, 'var')], y=values_dict[(k, 'onoff')], z = values_dict[(k, 'keyname')]: select_category(x, y,z)) # checkbutton widget
            self.display_dict[(k, 'checkbuttonwidget')].grid(row=self.display_dict[(k, 'row')], column=2, padx=5, pady=5, sticky="nsew") # set position

        # Create Indoor/Outdoor/Moonboard selection buttons
        radiopadx = 5
        radiopady = 5
        in_radio = ttk.Radiobutton(self.display_dict[('door', 'frame')], text = 'Indoor', variable = values_dict[('door', 'var')], value = 'indoor') # indoor radio button
        in_radio.grid(row=2, column=0, padx=radiopadx, pady=radiopady, sticky="nsew")
        out_radio = ttk.Radiobutton(self.display_dict[('door', 'frame')], text = 'Outdoor',variable = values_dict[('door', 'var')], value = 'outdoor') # outdoor radio button
        out_radio.grid(row=2, column=1, padx=radiopadx, pady=radiopady, sticky="nsew")
        mb_radio = ttk.Radiobutton(self.display_dict[('door', 'frame')], text = 'Moonboard', variable = values_dict[('door', 'var')], value = 'moonboard') # moonboard radio button
        mb_radio.grid(row=2, column=2, padx=radiopadx, pady=radiopady, sticky="nsew")
        self.display_dict[('door', 'checkbuttonwidget')] = ttk.Checkbutton(self.display_dict[('door', 'frame')], variable = values_dict[('door', 'onoff')], offvalue =0, onvalue = 1, command=lambda x=values_dict[('door', 'var')], y=values_dict[('door', 'onoff')], z = values_dict[('door', 'keyname')]: select_category(x, y,z)) # create checkbutton widget
        self.display_dict[('door', 'checkbuttonwidget')].grid(row=self.display_dict[('door', 'row')], column=3, padx=radiopadx, pady=radiopady, sticky="nsew")

        # Create climb style sport or bouldering selection buttons
        bouldering_radio = ttk.Radiobutton(self.display_dict[('climb_style', 'frame')], text = 'Bouldering', variable = values_dict[('climb_style', 'var')], value = 'bouldering') # bouldering radio button
        bouldering_radio.grid(row=3, column=0, padx=radiopadx, pady=radiopady, sticky="nsew")
        sport_radio = ttk.Radiobutton(self.display_dict[('climb_style', 'frame')], text = 'Sport', variable = values_dict[('climb_style', 'var')], value = 'sport') # sport radio button
        sport_radio.grid(row=3, column=1, padx=radiopadx, pady=radiopady, sticky="nsew")
        self.display_dict[('climb_style', 'checkbuttonwidget')] = ttk.Checkbutton(self.display_dict[('climb_style', 'frame')], variable = values_dict[('climb_style', 'onoff')], offvalue = 0, onvalue = 1, command=lambda x=values_dict[('climb_style', 'var')], y=values_dict[('climb_style', 'onoff')], z = values_dict[('climb_style', 'keyname')]: select_category(x, y,z)) # create check button widget
        self.display_dict[('climb_style', 'checkbuttonwidget')].grid(row=3, column=3, padx=radiopadx, pady=radiopady, sticky="nsew")

        topfrm.pack(expand=True, fill="both", padx=5, pady=5) # pack and show topfrm and all children

        ###########
        # middle pane - styles and notes
        # configure columns and rows in middle pane frame
        frm = ttk.Frame(middle_pane)
        for j in range(3):
            frm.columnconfigure(index = j, weight =1)
        for j in range(5):
            frm.rowconfigure(index = j, weight =1)

        # Create Labelframes for the hold, wall and skill types
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
        for j in range(3):
            skillsfrm.columnconfigure(index = j, weight =1)
        for j in range(3):
            skillsfrm.rowconfigure(index = j, weight =1)

        # update display_dict and values_dict with info for hold, wall, skill categories
        self.display_dict.update({('hold', 'frame'): holdsfrm,
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

        def select_style(x_var, y_onoff, z_keyname):
            """
            This function handles the selection of hold/wall/skill styles in the application. 
            values_dict[(z_keyname, 'checkedstyles')] is a list of str of hold/wall/skill styles whose buttons have been checked
            - ie list of hold/wall/skill styles to pass to selection_dict
            
            This function adds or removes styles from values_dict[(z_keyname, 'checkedstyles')] depending on if associated checkbutton is selected or not

            Parameters:
            x_var (tk.StringVar): The variable containing the value to add to values_dict[(z_keyname, 'checkedstyles')]
            y_onoff (tk.IntVar): The variable indicating whether the button is selected (1) or not (0).
            z_keyname (str): The key name (hold/wall/skill)

            Returns:
            None
            """
            # if button being turned off, i.e. onoff==0, set to off
            if y_onoff.get()==0:
                try:
                    values_dict[(z_keyname, 'checkedstyles')].remove(x_var.get()) # delete key-value pair from checkedstyles list for z_keyname(hold/wall/skill)
                except KeyError:
                    pass
            else:
                # button being turned on, onoff==1
                values_dict[(z_keyname, 'checkedstyles')].append(x_var.get()) # add key-value pair to checkedstyles list for z_keyname(hold/wall/skill)
            # print(values_dict[(z_keyname, 'checkedstyles')])

        # Create checkboxes for hold, wall and skill categories
        for k in ['hold', 'wall', 'skill']:
            self.display_dict[(k, 'buttons')] = [] # initialise empty list to store checkbutton widgets in
            nrows = 6 # number of rows to display - increase to reduce width of pane
            values_dict[(k, 'checkedstyles')] = [] # initialise empty list to store str values of styles to select
            values_dict[(k, 'buttons_onoff')] = [] # initialise empty list to store int values of button status selected (1) or not (0)
            values_dict[(k, 'dropdown_stringvars')] = [] # initialise empty list to store str values of style - eg hold = jug, crimp, volume etc.

            # iterate over all possible values of style
            for i, ddv in enumerate(values_dict[((k, 'dropdownvalues'))]):
                values_dict[(k, 'dropdown_stringvars')].append(tk.StringVar(value=ddv))
                values_dict[(k, 'buttons_onoff')].append(tk.IntVar(value = 0))
                self.display_dict[(k, 'buttons')].append(ttk.Checkbutton(self.display_dict[(k, 'frame')], text = ddv, variable = values_dict[(k, 'buttons_onoff')][i], offvalue =0, onvalue = 1, state = 'selected disabled', command=lambda x=values_dict[(k, 'dropdown_stringvars')][i], y=values_dict[(k, 'buttons_onoff')][i], z = values_dict[(k, 'keyname')]: select_style(x, y, z))) # create checkbutton
                self.display_dict[(k, 'buttons')][i].grid(row=i%nrows, column=i//nrows, padx=2, pady=2, sticky="nsew")

        frm.pack(expand=True, fill="both", padx=5, pady=5) # pack and display middle frame and all children

        ###########
        # bottom pane - notes and proceed buttom
        # configure columns and rows in bottom pane frame
        bottomfrm = ttk.Frame(bottom_pane)
        for j in range(3):
            bottomfrm.columnconfigure(index = j, weight =1)
        for j in range(2):
            bottomfrm.rowconfigure(index = j, weight =1)

        # Create Labelframes for the notes box
        notesfrm = ttk.LabelFrame(bottomfrm, text="Notes", padding=(20, 10))
        notesfrm.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="nsew")
        for j in range(2):
            notesfrm.columnconfigure(index = j, weight =1)
        notesfrm.rowconfigure(index = 0, weight =1)

        # Notes entry
        values_dict[('notes', 'keyname')] = 'notes'
        values_dict[('notes', 'var')] = tk.StringVar() # variable containing str to add as value to selection_dict
        values_dict[('notes', 'onoff')] = tk.IntVar(value=0) # variable storing whethere associated checkbutton is selected (1) or not (0)
        self.display_dict[('notes', 'entrywidget')] = ttk.Entry(notesfrm, textvariable=values_dict[('notes', 'var')]) # notes entry box
        self.display_dict[('notes', 'entrywidget')].grid(row=0, column = 0)
        self.display_dict[('notes', 'checkbuttonwidget')] = ttk.Checkbutton(notesfrm, variable = values_dict[('notes', 'onoff')], offvalue =0, onvalue = 1, command=lambda x=values_dict[('notes', 'var')], y=values_dict[('notes', 'onoff')], z = values_dict[('notes', 'keyname')]: select_category(x, y, z)) # checkbutton widget
        self.display_dict[('notes', 'checkbuttonwidget')].grid(row=0, column=1, padx=5, pady=5, sticky="nsew") # set position



        # Search Climbs button - get information from selection_dict
        def get_info():

            # Update selection_dict with selected styles for hold/wall/skill categories
            for k in ['hold', 'wall', 'skill']:
                if len(values_dict[(k, 'checkedstyles')]) != 0:
                    self.controller.update_selection_dict(k, values_dict[(k, 'checkedstyles')]) # add key-value pair to selection_dict if any styles have been selected
                    # selection_dict[k] = ', '.join(values_dict[(k, 'checkedstyles')])
            print(self.controller.selection_dict) # print final selection_dict
            self.controller.show_findclimbframe("DisplayPage") # move to DisplayPage

        # Create button for finalising selection_dict and moving to next page
        enterinfo_button_widget = tk.Button(bottomfrm, text="Search corresponding climbs", command = get_info)
        enterinfo_button_widget.grid(row=0, column=2)

        bottomfrm.pack(expand=True, fill="both", padx=5, pady=5) # pack and display bottom frame and all children

        # Sizegrip
        sizegrip = ttk.Sizegrip(self)
        sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))

class DisplayPage(tk.Frame):
    def __init__(self, parent, controller):
        """
        Initialize the DisplayPage with parent widget and controller object.

        Parameters:
        parent (tk.Widget): The parent widget for the DisplayPage.
        controller (MultiFrameRoot): The controller object that manages the application's frames.

        Returns:
        None
        """
        # Call parent class constructor, tk.Frame
        tk.Frame.__init__(self, parent) # parent is parent widget
        self.controller = controller # MultiFrameRoot object

        # set rows and columns of base frame of page. weight = 1 : even distribution
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)

        # Panedwindow
        paned = ttk.PanedWindow(self)
        paned.grid(row=0, column=0, padx = (15,15), pady=(25, 5), sticky="nsew")

        # Create a frame for some more selection buttons
        pane1 = ttk.Frame(paned)
        paned.add(pane1, weight=1)
        pane1.pack(padx=20, pady=10)

        # Create switch for including equivalent font/V grades
        # equivgrades_label = ttk.Label(pane1, text="Include font/V equivalent grades", justify="left")
        equiv_grades_widget = ttk.Checkbutton(pane1, text="Include font/V equivalent grades", style="Switch", command = lambda: self.update_grades())
        equiv_grades_widget.grid(row=0, column=0)

        # Create label box for displaying selection criteria
        infofrm = ttk.LabelFrame(pane1, text="Criteria", padding=(20, 10)) # create label frame
        infofrm.grid(row=0, column=1, padx=(20, 10), pady=10, sticky="nsew")
        self.criteria = tk.StringVar() # text variable to put criteria in
        criteria_label = ttk.Label(infofrm, textvariable = self.criteria, justify="left") # create label 
        criteria_label.grid(row=0, column=0)

        # Create a Frame for the Treeview
        treeFrame = ttk.Frame(paned)
        paned.add(treeFrame, weight=1)
        treeFrame.pack(padx=20, pady=10)

        # Create a pane for extra buttons/filters to move between frames or recalculate
        pane2 = ttk.Frame(paned)
        paned.add(pane2, weight =1)
        goback_button = tk.Button(pane2, text="Go back",
                           command=lambda: self.controller.show_findclimbframe("SelectionPage")) # go back to SelectionPage button
        exit_button = tk.Button(pane2, text="Exit",
                           command=lambda: self.controller.destroy()) # destroy and exit button - exit everything
        showclimbs_button = tk.Button(pane2, text = "Show climbs", command= lambda: self.show_climbs()) # show and recalculate climbs button
        # close display window and return to attempts input window, save selected climbid
        return_to_attempts_window_button = tk.Button(pane2, text = "Use selected climb, return to attempts", command = lambda: self.controller.return_to_attempts())
        goback_button.pack(side="left")
        exit_button.pack(side="right")
        showclimbs_button.pack(side="bottom")
        return_to_attempts_window_button.pack(side = "top")
        pane2.pack() 

        ##### Treeview #####
        # Scrollbars
        scrollbary = ttk.Scrollbar(treeFrame, orient = tk.VERTICAL)
        scrollbary.pack(side="right", fill="y")
        scrollbarx = ttk.Scrollbar(treeFrame, orient = tk.HORIZONTAL)
        scrollbarx.pack(side="bottom", fill="x")

        # Treeview
        self.treeview = ttk.Treeview(treeFrame, selectmode="extended", xscrollcommand = scrollbarx.set, yscrollcommand=scrollbary.set, columns=tuple(bc.climb_file_columns), height=12)
        self.treeview.pack()#expand=True, fill="both")
        scrollbary.config(command=self.treeview.yview)
        scrollbarx.config(command=self.treeview.xview)

        # Treeview headings & columns
        self.treeview.column("#0", width = 0, minwidth = "0") # sets width of first icon column to 0 so not displayed
        self.treeview.heading("#1", text = 'climb_id', anchor = "w") # adds climb_id as first column
        self.treeview.column("#1", stretch=True, width = 120, anchor = "w")
        
        def selectclimbid(a):
            curItem = self.treeview.focus()
            self.controller.selectedclimbid = self.treeview.item(curItem)['values'][0]
            # print(self.treeview.item(curItem))
            # print(self.treeview.item(curItem)['values'][0])
            # print(self.selectedclimbid, type(self.selectedclimbid))
        self.treeview.bind('<ButtonRelease-1>', selectclimbid)        

    def show_climbs(self):
        """
        Clears the treeview, recalculates the filtered climbs dataframe and display columns based on the current input in SelectionPage,
        sets up column headings for the treeview, inserts the treeview data for display, and sets the criteria str var for display.

        Parameters:
        self (DisplayPage): The instance of DisplayPage class where this method is being called.

        Returns:
        None: The function does not return any value.
        """
        # Clear treeview before repopulating it with new data
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Recalculate filtered climbs dataframe and display columns based on the current input in SelectionPage
        filtered_climbs_df, display_columns = self.controller.recalculate_display_climbs()

        # Set up column headings for treeview
        for i,heading in enumerate(display_columns):
            self.treeview.heading(f"#{i+2}", text = heading, anchor = "w") # i+2 as icon column and climb_id column
            self.treeview.column(f"#{i+2}", stretch=False, minwidth = 50, anchor = "w")
        self.treeview['show'] = 'headings' # hides #0 icon column

        # dataframe to display
        to_display = filtered_climbs_df[display_columns]

        # Insert treeview data for display
        for row in to_display.itertuples(index =True, name = None):
            self.treeview.insert('', 'end', values = row)

        # Set criteria str var for display
        cc = ''
        for k,v in self.controller.selection_dict.items():
            cc += f'{self.controller.findclimbsframes["SelectionPage"].display_dict[(k, "labeltext")]} {", ".join(v)}\n'
        self.criteria.set(cc)

        return 0

    def update_grades(self):
        """
        Update equivalent grades in climb_file_columns and recalculate display climbs.

        Parameters:
        self (DisplayPage): The instance of DisplayPage class where this method is being called.

        Returns:
        None:        
        """
        # Update equivalent grades in climb_file_columns
        bc.append_equivalent_grades(self.controller.selection_dict['grade'])
        # recalculate display climbs
        self.show_climbs()
    

class NewClimbWindow(tk.Toplevel):

    def __init__(self, controller):
        """
        Initialize the NewClimbWindow with controller object.

        Parameters:
        controller (MultiFrameRoot): The controller object that manages the application's frames.

        Returns:
        None
        """        
        # Call parent class constructor, tk.Toplevel()
        tk.Toplevel.__init__(self)
        self.controller = controller # MultiFrameRoot object
        self.title("New Climb?")

        frm = ttk.Frame(self, padding=40) # creates frame widget
        for j in range(4):
            frm.rowconfigure(index=1, weight=1)
        for j in range(2):
            frm.columnconfigure(index=1, weight=1)
        frm.grid()

        qlabel_widget = ttk.Label(frm, text="Is this a new climb?", justify="center") # label of text entry box
        qlabel_widget.grid(row=0, column=0, pady=5, columnspan=2) # set position


        yesnewclimb_button_widget = tk.Button(frm, text="Yes", command = lambda: self.controller.addnewclimb())
        yesnewclimb_button_widget.grid(row=2, column=0)

        nonewclimb_button_widget = tk.Button(frm, text="No", command = lambda: self.controller.findclimb())
        nonewclimb_button_widget.grid(row=2, column=1)


        frm.pack(expand=True, fill="both", padx=5, pady=5) # pack and display bottom frame and all children


class AddNewClimbPage(tk.Toplevel):
    def __init__(self, controller):
        tk.Toplevel.__init__(self)
        self.controller = controller # MultiFrameRoot object
        self.title("Add Climb")

        # initialize global variables
        self.sport = False
        climb_data = {}

        # Set relative weights of columns, determines how extra space distributed when window resized. 
        # if weight = 1 for all, even distribution.
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)

        # Panedwindow
        paned = ttk.PanedWindow(self)
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

        display_dict = {}
        values_dict = {}

        #######
        # top tab : basic categories
        def sport_switch():
            if self.sport:
                self.sport = False
            else:
                self.sport = True

        #### Indoor Bouldering Tab
        tab_1 = ttk.Frame(top_notebook)
        tab_1.columnconfigure(index=0, weight=2)
        tab_1.columnconfigure(index=1, weight=2)
        for j in range(5):
            tab_1.rowconfigure(index = j, weight =1)
        top_notebook.add(tab_1, text="Indoor")

        # Grade entry
        grade_var = tk.StringVar(value = 'V4-6')
        gradeentry_widget = ttk.Entry(tab_1, textvariable=grade_var) # location entry box
        gradeentry_widget.grid(row=0, column =1)
        gew_label = ttk.Label(tab_1, text="Grade :", justify="left")
        gew_label.grid(row=0, column=0, pady=10, columnspan=1)

        # Location entry
        location_var = tk.StringVar(value = 'Font Borough')
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

            if not self.sport:
                climb_data['climb_style'] = bc.climb_styles[0] # 'bouldering'
                climb_data['rope'] = 'NaN'
            else:
                climb_data['climb_style'] = bc.climb_styles[1] # 'sport'
                climb_data['rope'] = ropevar.get()
            print(climb_data)
            self.controller.newclimbdata = climb_data

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
        location_var_2 = tk.StringVar(value = 'Devils Gorge')
        locationentry_widget_2 = ttk.Entry(tab_2, textvariable=location_var_2) # location entry box
        locationentry_widget_2.grid(row=2, column =1)
        lew_label_2 = ttk.Label(tab_2, text="Location :", justify="left")
        lew_label_2.grid(row=2, column=0, pady=10, columnspan=1)

        # Rock type
        rock_var_2 = tk.StringVar()
        rockbox_2 = ttk.Combobox(tab_2, textvariable= rock_var_2, values=bc.rock_types)
        rockbox_2.current(2) # sets intial/default selection to 0 index of values list
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
            climb_data['grade'] = grade_var_2.get()
            climb_data['location'] = location_var_2.get()
            climb_data['climb_name'] = name_var_2.get()
            climb_data['door'] = bc.doors[1]  # 'outdoor'
            climb_data['angle'] = 'NaN'
            climb_data['mbyear'] = 'NaN'
            climb_data['rock_type'] = rock_var_2.get()

            if not self.sport:
                climb_data['climb_style'] = bc.climb_styles[0] # 'bouldering'
                climb_data['rope'] = 'NaN'
            else:
                climb_data['climb_style'] = bc.climb_styles[1] # 'sport'
                climb_data['rope'] = ropevar_2.get()
            print(climb_data)
            self.controller.newclimbdata = climb_data

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
        location_var_3 = tk.StringVar(value = 'Font Borough')
        locationentry_widget_3 = ttk.Entry(tab_3, textvariable=location_var_3) # location entry box
        locationentry_widget_3.grid(row=2, column =1)
        lew_label_3 = ttk.Label(tab_3, text="Location :", justify="left")
        lew_label_3.grid(row=2, column=0, pady=10, columnspan=1)

        # Year option
        year_var_3 = tk.StringVar()
        yearbox_3 = ttk.Combobox(tab_3, textvariable=year_var_3, values= bc.mbyears)
        yearbox_3.current(3) # sets intial/default selection to 0 index of values list
        yearbox_3.grid(row=3, column=1, padx=5, pady=10,  sticky="ew")
        year_label_3 = ttk.Label(tab_3, text="Year :", justify="left")
        year_label_3.grid(row=3, column=0, pady=10, columnspan=1)

        # Angle option
        angle_var_3 = tk.StringVar()
        anglebox_3 = ttk.Combobox(tab_3, textvariable=angle_var_3, values= bc.angles)
        anglebox_3.current(3) # sets intial/default selection to 0 index of values list
        anglebox_3.grid(row=4, column=1, padx=5, pady=10,  sticky="ew")
        angle_label_3 = ttk.Label(tab_3, text="Angle :", justify="left")
        angle_label_3.grid(row=4, column=0, pady=10, columnspan=1)

        def get_info_moonboard():
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
            self.controller.newclimbdata = climb_data

        enterinfo_mb_button_widget = tk.Button(tab_3, text="Submit Climb Details", command = get_info_moonboard)
        enterinfo_mb_button_widget.grid(row=5, column=1)

        top_notebook.pack(expand=True, fill="both", padx=5, pady=5)


        ########
        # bottom pane - styles and notes
        frm = ttk.Frame(bottom_pane)
        for j in range(3):
            frm.columnconfigure(index = j, weight =1)
        for j in range(5):
            frm.rowconfigure(index = j, weight =1)
        # bottom_pane.add(frm, text="Notes and styles")

        # Create Labelframes for the hold, wall and skill types
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
        for j in range(3):
            skillsfrm.columnconfigure(index = j, weight =1)
        for j in range(3):
            skillsfrm.rowconfigure(index = j, weight =1)

        # update display_dict and values_dict with info for hold, wall, skill categories
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


        def select_style(x_var, y_onoff, z_keyname):
            """
            This function handles the selection of hold/wall/skill styles in the application. 
            values_dict[(z_keyname, 'checkedstyles')] is a list of str of hold/wall/skill styles whose buttons have been checked
            - ie list of hold/wall/skill styles to pass to selection_dict
            
            This function adds or removes styles from values_dict[(z_keyname, 'checkedstyles')] depending on if associated checkbutton is selected or not

            Parameters:
            x_var (tk.StringVar): The variable containing the value to add to values_dict[(z_keyname, 'checkedstyles')]
            y_onoff (tk.IntVar): The variable indicating whether the button is selected (1) or not (0).
            z_keyname (str): The key name (hold/wall/skill)

            Returns:
            None
            """
            # if button being turned off, i.e. onoff==0, set to off
            if y_onoff.get()==0:
                try:
                    values_dict[(z_keyname, 'checkedstyles')].remove(x_var.get()) # delete key-value pair from checkedstyles list for z_keyname(hold/wall/skill)
                except KeyError:
                    pass
            else:
                # button being turned on, onoff==1
                values_dict[(z_keyname, 'checkedstyles')].append(x_var.get()) # add key-value pair to checkedstyles list for z_keyname(hold/wall/skill)
            # print(values_dict[(z_keyname, 'checkedstyles')])


        # Create checkboxes for hold, wall and skill categories
        for k in ['hold', 'wall', 'skill']:
            display_dict[(k, 'buttons')] = [] # initialise empty list to store checkbutton widgets in
            nrows = 6 # number of rows to display - increase to reduce width of pane
            values_dict[(k, 'checkedstyles')] = [] # initialise empty list to store str values of styles to select
            values_dict[(k, 'buttons_onoff')] = [] # initialise empty list to store int values of button status selected (1) or not (0)
            values_dict[(k, 'dropdown_stringvars')] = [] # initialise empty list to store str values of style - eg hold = jug, crimp, volume etc.

            # iterate over all possible values of style
            for i, ddv in enumerate(values_dict[((k, 'dropdownvalues'))]):
                values_dict[(k, 'dropdown_stringvars')].append(tk.StringVar(value=ddv))
                values_dict[(k, 'buttons_onoff')].append(tk.IntVar(value = 0))
                display_dict[(k, 'buttons')].append(ttk.Checkbutton(display_dict[(k, 'frame')], text = ddv, variable = values_dict[(k, 'buttons_onoff')][i], offvalue =0, onvalue = 1, state = 'selected disabled', command=lambda x=values_dict[(k, 'dropdown_stringvars')][i], y=values_dict[(k, 'buttons_onoff')][i], z = values_dict[(k, 'keyname')]: select_style(x, y, z))) # create checkbutton
                display_dict[(k, 'buttons')][i].grid(row=i%nrows, column=i//nrows, padx=2, pady=2, sticky="nsew")


        # Notes entry
        notes_var = tk.StringVar()
        notes_entry_widget = ttk.Entry(frm, textvariable=notes_var) # location entry box
        notes_entry_widget.grid(row=1, column =1)
        new_label = ttk.Label(frm, text="Notes :", justify="left")
        new_label.grid(row=1, column=0, pady=10, columnspan=1)


        # Enter all details
        def get_info_holdwallskillnotes():
            for k in ['hold', 'wall', 'skill']:
                if len(values_dict[(k, 'checkedstyles')]) != 0:
                    # self.controller.update_selection_dict(k, values_dict[(k, 'checkedstyles')]) # add key-value pair to selection_dict if any styles have been selected
                    # selection_dict[k] = ', '.join(values_dict[(k, 'checkedstyles')])
                    climb_data[k] = ', '.join(values_dict[(k, 'checkedstyles')])
                else:
                    climb_data[k] = ''
            climb_data['notes'] = notes_var.get()
            print(climb_data)
            self.controller.newclimbdata = climb_data

        enter_extra_info_button_widget = tk.Button(frm, text="Submit Climb Details", command = get_info_holdwallskillnotes)
        enter_extra_info_button_widget.grid(row=3, column=1)

        frm.pack(expand=True, fill="both", padx=5, pady=5)

        # Sizegrip
        sizegrip = ttk.Sizegrip(self)
        sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))

        # Center the window, and set minsize
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())
        x_cordinate = int((self.winfo_screenwidth()/2) - (self.winfo_width()/2))
        y_cordinate = int((self.winfo_screenheight()/2) - (self.winfo_height()/2))
        self.geometry("+{}+{}".format(x_cordinate, y_cordinate))


        submit_button_widget = tk.Button(frm, text="Done", command = lambda: self.controller.submit_new_climb())
        submit_button_widget.grid(row=4, column=1)



if __name__ == "__main__":
    app = MultiFrameRoot()
    app.mainloop()