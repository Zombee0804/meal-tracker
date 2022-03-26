
import tkinter as tk
from tkinter import ttk

import pathlib
from datetime import datetime

applicationFonts = {
    'default' : ("Courier New", 12),
    'defaultBold' : ("Segoe Ui bold", 14)
}

class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        
        # Application Setup
        themePath = str(pathlib.Path(__file__).parent.parent.absolute()) + "\SunValleyTheme\sun-valley.tcl"
        self.tk.call("source", themePath)
        self.tk.call("set_theme", "dark")

        self.title("Meal Tracker")
        self.attributes('-fullscreen', True)

        self.setup_notebook()
    
    def setup_notebook(self):
        self.notebook_main = ttk.Notebook(self, width = self.winfo_screenwidth(), height = self.winfo_screenheight()-100)
        self.notebook_main.grid(row = 0, column = 0)

        self.frame_dailyTab = DailyTab()
        self.notebook_main.add(self.frame_dailyTab, text = "Daily")

        self.frame_restaurantTab = RestaurantTab()
        self.notebook_main.add(self.frame_restaurantTab, text = "Restaurants")

        self.frame_itemTab = ItemTab()
        self.notebook_main.add(self.frame_itemTab, text = "Items")

        self.button_quit = ttk.Button(self, text = "Quit", command = quit, width = 5)
        self.button_quit.grid(row = 1, column = 0, sticky = "se", padx = 15, pady = 15)

class DailyTab(ttk.Frame):

    def __init__(self):
        super().__init__()

class RestaurantTab(ttk.Frame):

    def __init__(self):
        super().__init__()

class ItemTab(ttk.Frame):

    def __init__(self):
        super().__init__()

app = Application()
app.mainloop()