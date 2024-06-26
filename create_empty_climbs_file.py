"""
@author: jbrown888
25/06/24
Create climbs data file
"""
from tkinter import ttk
import os
import csv
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
import broomcupboard as bc


def create_climbs_file():
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
        with open(filename, "x", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(bc.climb_file_columns)  # Write attempts column names

        messagebox.showinfo("Success", f"CSV file '{os.path.basename(filename)}' created.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create CSV file: {str(e)}")

# Call the function to create the CSV file
create_climbs_file()
