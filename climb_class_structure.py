# -*- coding: utf-8 -*-
"""
@author: jnb19
"""
import datetime as dt



class route:
    def __init__(self, climb_style, grade, door, location, attempts = 0, **kwargs):
        """
        Initialize a new route object.

        Parameters:
        ----------
        climb_style : str
        The style of the climb (e.g., bouldering, sport, trad, lead).
        grade : str
        The grade of the climb.
        door : str
        Indoor or outdoor climb.
        location : str
        The location of climb (gym or crag)
        attempts : int, optional
        Number of attempts on this route. Default 0
        kwargs : dict, optional
        Additional keyword arguments for future expansion.

        Returns:
        -------
        None.
        """
        self.climb_style = climb_style
        self.grade = grade
        self.door = door
        self.location = location
        self.attempts_counter = attempts
        self.attempts = {} # dictionary of attempt dates and results; {key = date, value = success}
        self.sent = False # whether or not the route has been sent, initialized to false

    def __str__(self):
        # write __str__ method using init values here
        return f"{self.door} {self.climb_style} at {self.location}, grade {self.grade}"

    def add_attempt(self, attempt_date, success, **kwargs):
        """
        Add attempt to the route object.

        Parameters:
        ----------
        attempt_date : dt.date
            The date of the attempt.
        success : bool
            The result of the attempt (i.e., true = success, false = failure).
        kwargs : dict, optional
            Additional keyword arguments for future expansion.

        Returns:
        -------
        None.
        """
        if attempt_date > dt.date.today():
            raise ValueError("Attempt date cannot be in the future.")
        self.attempts_counter += 1
        group = self.attempts.setdefault(attempt_date, []) # checks if attempt_date is already key in dict
        group.append(success)
        if success:
            if not self.sent:
                self.initial_send_date = attempt_date
            self.sent = success # placed within the if statement so that it is only updated for send, and doesn't get backdated as failure

    def remove_all_attempts_on_date(self, attempt_date):
        """
        Remove all attempts on a specific date from the route object, and update sent status accordingly

        Parameters:
        ----------
        attempt_date : dt.date
            The date of the attempts to be removed.

        Returns:
        -------
        None.

        Raises:
        ------
        ValueError
            If the attempt date is in the future.
        KeyError
            If there are no attempts on the specified date.

        """
        if attempt_date > dt.date.today():
            raise ValueError("Attempt date cannot be in the future.")
        
        if attempt_date in self.attempts.keys():
            attempts_on_date = self.attempts.pop(attempt_date)
            self.attempts_counter -= len(attempts_on_date)

            # check if any previous sends on this route
            if any(True in val for val in self.attempts.values()):
                self.sent = True
                self.initial_send_date = min([k for k, v in self.attempts.items() if any(v)])
            else:
                self.sent = False
                self.initial_send_date = None
        else:
            raise KeyError(f"There are no attempts on {attempt_date} for this {self.grade} route {self.climb_style} at {self.location}")

    def adjust_date(self, old_attempt_date, new_attempt_date):
        """
        Adjust the date of an existing attempt. If the new date already has attempts, 
        these attempts will be merged into the new date.

        Parameters:
        ----------
        old_attempt_date : dt.date
            The original date of the attempt.
        new_attempt_date : dt.date
            The new date for the attempt.

        Returns:
        -------
        None

        Raises:
        ------
        ValueError
            If either the old or new attempt date is in the future.
        KeyError
            If there are no attempts on the old attempt date.
        """
        if old_attempt_date > dt.date.today():
            raise ValueError("Date to be adjusted cannot be in the future.")
        if new_attempt_date > dt.date.today():
            raise ValueError("Adjusted date cannot be in the future.")
        if old_attempt_date not in self.attempts.keys():
            raise KeyError(f"There are no attempts on {old_attempt_date} for this {self.grade} route {self.climb_style} at {self.location}")
        if new_attempt_date in self.attempts.keys():
            print(f"There are already attempts on {new_attempt_date} for this route. Attempts on this date will be merged.")
            attempts_to_be_merged = self.attempts.pop(old_attempt_date)
            for x in attempts_to_be_merged:
                self.attempts[new_attempt_date].append(x)
        else:
            self.attempts[new_attempt_date] = self.attempts.pop(old_attempt_date)
        # shouldn't need to change status of self.sent, as we are not removing attempts, only changing the date
        if self.sent:
            self.initial_send_date = min([k for k, v in self.attempts.items() if any(v)])
            


    # def remove_last_x_attempts(self, x_attempts):
    #     # delete last x dictionary entries
    #     if x_attempts > self.attempts_counter:
    #         raise ValueError(f"Cannot remove {x_attempts} attempts. There are only {self.attempts_counter} attempts.")
    #     for keyentry in list(self.attempts.keys())[len(self.attempts)-x_attempts:]:
    #         del self.attempts[keyentry] 
    #     self.attempts_counter -= x_attempts
    #     if any(self.attempts.values()):
    #         self.sent = True
    #         self.initial_send_date = min([k for k, v in self.attempts.items() if v])
    #     else:
    #         self.sent = False
    #         self.initial_send_date = None
    # def remove_last_attempt(self):
    #     self.attempts_counter -= 1
    #     # delete last element of list from last dictionary value
    #     del self.attempts[list(self.attempts.keys())[-1]]
    #     if any(self.attempts.values()):
    #         self.sent = True
    #         self.initial_send_date = min([k for k, v in self.attempts.items() if v])
    #     else:
    #         self.sent = False
    #         self.initial_send_date = None

#%%
climb = route(climb_style = 'bouldering', grade = 'f5a', door = 'indoor', location = 'Rockover')
climb.add_attempt(attempt_date = dt.date(2024, 5, 16), success = False)
climb.add_attempt(attempt_date = dt.date(2024, 5, 17), success  = False)
climb.add_attempt(attempt_date = dt.date(2024, 5, 20), success = False)
climb.add_attempt(attempt_date = dt.date(2024, 5, 28), success  = True)
climb.add_attempt(attempt_date = dt.date(2024, 5, 20), success = True)
climb.add_attempt(attempt_date = dt.date(2024, 4, 28), success  = False)
climb.add_attempt(attempt_date = dt.date(2024, 6, 3), success  = True)

print(climb.initial_send_date)
climb.remove_all_attempts_on_date(attempt_date = dt.date(2024, 5, 28))

print(climb.attempts)


climb.remove_all_attempts_on_date(attempt_date = dt.date(2024, 5, 20))

print(climb.attempts)

print(climb.attempts_counter)

print(climb.sent, climb.initial_send_date)