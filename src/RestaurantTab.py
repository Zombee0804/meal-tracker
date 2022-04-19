
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import Utilities as utilities

class RestaurantTab(ttk.Frame):

    def __init__(self):
        super().__init__()

        self.refresh_saved_info()

        gridSettings = self.settings['padding'] | {'sticky' : 'w'}

        #region New Restaurant Frame
        self.frame_newRestaurant = ttk.Frame(self)
        self.frame_newRestaurant.grid(row = 0, column = 0, **gridSettings)

        self.label_name = ttk.Label(self.frame_newRestaurant, text = "Restaurant Name:", font = self.settings['fonts']['bold'])
        self.label_name.grid(row = 0, column = 0, **gridSettings)

        self.entry_name = ttk.Entry(self.frame_newRestaurant, font = self.settings['fonts']['default'], width = 75)
        self.entry_name.grid(row = 1, column = 0, **gridSettings)

        self.label_rating = ttk.Label(self.frame_newRestaurant, text = "Rating:", font = self.settings['fonts']['bold'])
        self.label_rating.grid(row = 0, column = 1, **gridSettings)

        self.spinbox_rating = ttk.Spinbox(
            self.frame_newRestaurant, 
            state = "READONLY", 
            values = ["Very Bad", "Bad", "Okay", "Good", "Very Good", "Outstanding"], 
            wrap = True, 
            font = self.settings['fonts']['default']
        )
        self.spinbox_rating.set("Okay")
        self.spinbox_rating.grid(row = 1, column = 1, **gridSettings)

        self.label_startingCount = ttk.Label(self.frame_newRestaurant, text = "Starting Count:", font = self.settings['fonts']['bold'])
        self.label_startingCount.grid(row = 0, column = 2, **gridSettings)
    
        self.spinbox_startingCount = ttk.Spinbox(self.frame_newRestaurant, from_ = 0, to = 999, font = self.settings['fonts']['default'])
        self.spinbox_startingCount.set(0)
        self.spinbox_startingCount.grid(row = 1, column = 2, **gridSettings)

        self.button_submit = ttk.Button(self.frame_newRestaurant, text = "Submit", style = "Accent.TButton", command = self.submit_new_restaurant)
        self.button_submit.grid(row = 1, column = 3, **gridSettings)
        #endregion

        #region Restaurant Count Frame
        self.frame_restCount = ttk.Frame(self)
        self.frame_restCount.grid(row = 1, column = 0, **gridSettings)

        self.button_recount = ttk.Button(self.frame_restCount, text = "Recount Restaurants", command = self.force_recount)
        self.button_recount.grid(row = 0, column = 0, padx = gridSettings['padx'] * 3, pady = gridSettings['pady'], sticky = gridSettings['sticky'])

        self.frame_restTree = RestaurantTree(self.frame_restCount, gridSettings)
        self.frame_restTree.grid(row = 1, column = 0, **gridSettings)
        #endregion

    def refresh_saved_info(self):
        self.dailyEntries = utilities.get_daily_entries()
        self.itemInfo = utilities.get_item_info()
        self.restaurantInfo = utilities.get_restaurant_info()
        self.settings = utilities.get_settings()
    
    def get_new_restaurant_info(self):
        restName = self.entry_name.get()
        restInfo = {
            "rating" : self.spinbox_rating.get(),
            "count" : int(self.spinbox_startingCount.get()),
            "startingCount" : int(self.spinbox_startingCount.get())
        }
        return restName, restInfo
    
    def validate_new_restaurant(self):
        restName, restInfo = self.get_new_restaurant_info()
        
        if (restName == "" or restName.isspace() == True):
            return False
        
        return True
    
    def submit_new_restaurant(self):
        isNewRestValid = self.validate_new_restaurant()
        if (isNewRestValid == True):
            restName, restInfo = self.get_new_restaurant_info()
            self.restaurantInfo[restName] = restInfo
            utilities.save_restaurant_info(self.restaurantInfo)

            self.frame_restTree.add_restaurants_to_tree()

            self.clear_restaurant_input()
        else:
            messagebox.showerror("Invalid Info", "Restaurant Information Is Invalid")
    
    def clear_restaurant_input(self):
        self.entry_name.delete(0, tk.END)
        self.spinbox_rating.set("Okay")
        self.spinbox_startingCount.set(0)

    def force_recount(self, event = None):
        self.refresh_saved_info()

        newCount = {key:0 for (key, value) in self.restaurantInfo.items()}

        for restaurantName in newCount.keys():
            for date, entries in self.dailyEntries.items():
                for meal, entry in entries.items():
                    if ('establishment' in entry.keys()):
                        if (entry['establishment'].lower() == restaurantName.lower()):
                            newCount[restaurantName] += 1

        for restName, restInfo in self.restaurantInfo.items():
            self.restaurantInfo[restName]['count'] = newCount[restName] + restInfo['startingCount']
        
        utilities.save_restaurant_info(self.restaurantInfo)

        self.frame_restTree.add_restaurants_to_tree()

class RestaurantTree(ttk.Frame):

    def __init__(self, parent, gridSettings):
        super().__init__(parent)
        self.parent = parent

        self.refresh_saved_info()
        self.searchQuery = None

        #region Search Bar
        self.frame_search = ttk.Frame(self)
        self.frame_search.grid(row = 0, column = 0, **gridSettings)

        self.label_search = ttk.Label(self.frame_search, text = "Search:", font = self.settings['fonts']['bold'])
        self.label_search.grid(row = 0, column = 0, **gridSettings)

        self.entry_query = ttk.Entry(self.frame_search, font = self.settings['fonts']['default'], width = 63)
        self.entry_query.bind("<Any-KeyRelease>", self.submit_search_query)
        self.entry_query.grid(row = 0, column = 1, **gridSettings)
        #endregion

        #region Treeview
        self.frame_tree = ttk.Frame(self)
        self.frame_tree.grid(row = 1, column = 0, **gridSettings)

        treeviewHeaders = {
            "Index" : 50,
            "Name" : 250,
            "Rating" : 200,
            "Count" : 100
        }

        self.treeview_restCount = ttk.Treeview(
            self.frame_tree,
            columns = list(treeviewHeaders.keys()),
            height = 10,
            show = "headings"
        )
        self.treeview_restCount.column("#0", width = 50)
        for header, columnWidth in treeviewHeaders.items():
            self.treeview_restCount.heading(header, text = header)
            self.treeview_restCount.column(header, width = columnWidth)
        self.treeview_restCount.bind("<Expose>", self.add_restaurants_to_tree)
        self.treeview_restCount.bind("<KeyRelease-Delete>", self.delete_selected_item)
        self.treeview_restCount.grid(row = 0, column = 0, **gridSettings)

        self.scrollbar = ttk.Scrollbar(self.frame_tree, orient = tk.VERTICAL, command = self.treeview_restCount.yview)
        self.scrollbar.grid(row = 0, column = 1, sticky = "NS")
        self.treeview_restCount.configure(yscrollcommand = self.scrollbar.set)

        self.button_delete = ttk.Button(self.frame_tree, text = "Delete", style = "Accent.TButton", command = self.delete_selected_item)
        self.button_delete.grid(row = 1, column = 0, columnspan = 2, sticky = "E", padx = gridSettings['padx'], pady = gridSettings['pady'])
    
        self.add_restaurants_to_tree()
        #endregion
    
    def refresh_saved_info(self):
        self.dailyEntries = utilities.get_daily_entries()
        self.itemInfo = utilities.get_item_info()
        self.restaurantInfo = utilities.get_restaurant_info()
        self.settings = utilities.get_settings()
    
    def add_restaurants_to_tree(self, event = None):
        self.refresh_saved_info()
    
        alphaSorted = sorted(self.restaurantInfo.items(), key = lambda x:x[0], reverse = False)
        sortedRest = sorted(alphaSorted, key = lambda x:x[1]['count'], reverse = True)

        for iid in self.treeview_restCount.get_children():
            self.treeview_restCount.delete(iid)
    
        for restName, restInfo in sortedRest:
            if (self.searchQuery == None or self.searchQuery.lower() in restName.lower()):
                restValues = [sortedRest.index((restName, restInfo)) + 1, restName, restInfo['rating'], restInfo['count']]
                self.treeview_restCount.insert(parent = "", index = "end", iid = restName.lower(), values = restValues)
    
    def submit_search_query(self, event = None):
        query = self.entry_query.get()
        if (query == "" or query.isspace() == True):
            self.searchQuery = None
        else:
            self.searchQuery = query
        self.add_restaurants_to_tree()

    def delete_selected_item(self, event = None):
        self.refresh_saved_info()

        deleteItem = self.treeview_restCount.focus()

        if (deleteItem == "none"):
            messagebox.showerror("Deletion Error!", "Cannot Delete This Restaurant")
            return

        if (deleteItem != "" and deleteItem.isspace() == False):
            for date, entry in self.dailyEntries.items():
                for mealName, mealInfo in entry.items():                    
                    if ('establishment' in mealInfo.keys()):
                        if (mealInfo['establishment'].lower() == deleteItem.lower()):
                            mealInfo['establishment'] = "None"
                            self.restaurantInfo['None']['count'] += 1
        
        self.restaurantInfo.pop(utilities.find_dict_key(self.restaurantInfo, deleteItem))

        utilities.save_daily_entries(self.dailyEntries)
        utilities.save_restaurant_info(self.restaurantInfo)

        self.add_restaurants_to_tree()