
import tkinter as tk
from tkinter import ttk

import Utilities as utilities

from DailyTab import DailyTab
from RestaurantTab import RestaurantTab
from ItemTab import ItemTab

class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.refresh_saved_info()
        
        # Cosmetic Setup
        themePath = utilities.projectDir + "\SunValleyTheme\sun-valley.tcl"
        self.tk.call("source", themePath)
        self.tk.call("set_theme", "dark")

        self.title("Meal Tracker")
        self.attributes('-fullscreen', True)

        # Data Setup
        self.dailyEntries = utilities.get_daily_entries()
        if (self.settings == {}):
            self.settings = utilities.read_json("defaultSettings.json", {}, directoryPath = utilities.projectDir + "\\src\\")
            self.settings['startDate'] = utilities.dt.date.today().strftime(r"%d/%m/%Y")
            utilities.save_settings(self.settings)
        
        self.bind("<KeyPress-Escape>", self.kill)

        # Widget Setup
        self.setup_notebook()

    def refresh_saved_info(self):
        self.dailyEntries = utilities.get_daily_entries()
        self.itemInfo = utilities.get_item_info()
        self.restaurantInfo = utilities.get_restaurant_info()
        self.settings = utilities.get_settings()
    
    def setup_notebook(self):

        self.notebook_main = ttk.Notebook(self, width = self.winfo_screenwidth(), height = self.winfo_screenheight()-85)
        self.notebook_main.grid(row = 0, column = 0)

        self.frame_dailyTab = DailyTab()
        self.notebook_main.add(self.frame_dailyTab, text = "Daily")

        self.frame_itemTab = ItemTab()
        self.notebook_main.add(self.frame_itemTab, text = "Items")

        self.frame_restaurantTab = RestaurantTab()
        self.notebook_main.add(self.frame_restaurantTab, text = "Restaurants")

        self.button_quit = ttk.Button(self, width = 5, text = "Quit", command = self.kill)
        self.button_quit.grid(row = 1, column = 0, sticky = "se", **self.settings['padding'])
    
    def kill(self, event = None):
        self.destroy()
        quit()

app = Application()
app.mainloop()