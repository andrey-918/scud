import tkinter as tk
from tkinter import ttk

def create_time_combobox(parent, default_value, range_max, width=3):
    frame = tk.Frame(parent)
    frame.pack(fill='x', padx=3, pady=3)
    var = tk.StringVar(value=str(default_value).zfill(2))
    combobox = ttk.Combobox(frame, textvariable=var, values=[str(i).zfill(2) for i in range(range_max)],
                           font=('Arial', 18), state='readonly', width=width)
    combobox.pack(side='left', padx=3)
    return var