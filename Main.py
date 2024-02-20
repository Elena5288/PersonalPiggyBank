import tkinter as tk
from tkinter import ttk
import csv
import numpy as np
from LoginPage import LoginPage
from NewProfile import NewProfile

if __name__=="__main__":
    root=tk.Tk()
    app_login=LoginPage(root)
    root.mainloop()