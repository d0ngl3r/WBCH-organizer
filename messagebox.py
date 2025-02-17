import tkinter as tk
from tkinter import messagebox

def ask_rename():
    root = tk.Tk()
    root.withdraw()

    response = messagebox.askyesno("Rename Files", "Do you want to rename the files?")

    return response  # True = Yes, False = No
