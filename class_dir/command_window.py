#############################
#     command window      #
#      Class name       #
#        Date//         #
#############################
# NOTES :
"""

"""
# IMPORTS
import utility
import tkinter as tk
import ttkbootstrap as ttk
from typing import Union

# SETTINGS
# logger = Settings.setup_logging("debugging")


class CommandWindow:

    def __init__(self, master, names_functions):
        self.master = master
        self.buttons = {key: ttk.Button(master, text=key, command=names_functions[key]) for key in names_functions}

        for i, key in enumerate(self.buttons.values()):
            key.grid(column=i%2, row=i//2, padx=10, pady=10)



if __name__ == '__main__':
    # tests
    
    functions = {
        "button1": lambda: print("button1 clicked"),
        "button2": lambda: print("button2 clicked"),
        "button3": lambda: print("button3 clicked"),
        "button4": lambda: print("button4 clicked")
    }

    root = ttk.Window()
    app = CommandWindow(root, functions)
    root.mainloop()