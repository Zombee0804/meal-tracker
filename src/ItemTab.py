
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import Utilities as utilities

class ItemTab(ttk.Frame):

    def __init__(self):
        super().__init__()

        self.refresh_saved_info()

        gridSettings = self.settings['padding'] | {'sticky' : 'w'}

        #region Widget Setup
        # New Item Frame
        self.frame_newItem = ttk.Frame(self)
        self.frame_newItem.grid(row = 0, column = 0, **gridSettings)

        self.label_name = ttk.Label(self.frame_newItem, text = "Item Name:", font = self.settings['fonts']['bold'])
        self.label_name.grid(row = 0, column = 0, **gridSettings)

        self.entry_name = ttk.Entry(self.frame_newItem, font = self.settings['fonts']['default'], width = 75)
        self.entry_name.grid(row = 1, column = 0, **gridSettings)

        self.label_type = ttk.Label(self.frame_newItem, text = "Type:", font = self.settings['fonts']['bold'])
        self.label_type.grid(row = 0, column = 1, **gridSettings)

        #region Item Type Selection
        self.frame_itemType = ttk.Frame(self.frame_newItem)
        self.frame_itemType.grid(row = 1, column = 1, **gridSettings)

        self.var_itemType = tk.StringVar()
        self.var_itemType.set("food")
        self.radio_food = ttk.Radiobutton(self.frame_itemType, text = "Food", variable = self.var_itemType, value = "food")
        self.radio_food.grid(row = 0, column = 0, **gridSettings)

        self.radio_drink = ttk.Radiobutton(self.frame_itemType, text = "Drink", variable = self.var_itemType, value = "drink")
        self.radio_drink.grid(row = 1, column = 0, **gridSettings)
        #endregion

        self.label_rating = ttk.Label(self.frame_newItem, text = "Rating:", font = self.settings['fonts']['bold'])
        self.label_rating.grid(row = 0, column = 3, **gridSettings)

        self.spinbox_rating = ttk.Spinbox(
            self.frame_newItem, 
            state = "READONLY", 
            values = ["Very Bad", "Bad", "Okay", "Good", "Very Good", "Outstanding"], 
            wrap = True, 
            font = self.settings['fonts']['default']
        )
        self.spinbox_rating.set("Okay")
        self.spinbox_rating.grid(row = 1, column = 3, **gridSettings)

        self.label_startingCount = ttk.Label(self.frame_newItem, text = "Starting Count:", font = self.settings['fonts']['bold'])
        self.label_startingCount.grid(row = 0, column = 4, **gridSettings)

        self.spinbox_startingCount = ttk.Spinbox(self.frame_newItem, from_ = 0, to = 999, font = self.settings['fonts']['default'])
        self.spinbox_startingCount.set(0)
        self.spinbox_startingCount.grid(row = 1, column = 4, **gridSettings)

        self.button_submit = ttk.Button(self.frame_newItem, text = "Submit", style = "Accent.TButton", command = self.submit_new_item)
        self.button_submit.grid(row = 1, column = 5, **gridSettings)

        # Item Count Frame
        self.frame_itemCount = ttk.Frame(self)
        self.frame_itemCount.grid(row = 1, column = 0, **gridSettings)

        self.frame_foodTree = ItemTree(self.frame_itemCount, "food", gridSettings)
        self.frame_foodTree.grid(row = 0, column = 0, **gridSettings)

        self.frame_drinkTree = ItemTree(self.frame_itemCount, "drink", gridSettings)
        self.frame_drinkTree.grid(row = 0, column = 1, **gridSettings)
        #endregion

    def refresh_saved_info(self):
        self.dailyEntries = utilities.get_daily_entries()
        self.itemInfo = utilities.get_item_info()
        self.restaurantInfo = utilities.get_restaurant_info()
        self.settings = utilities.get_settings()

    def get_new_item_info(self):
        itemName = self.entry_name.get()
        itemType = self.var_itemType.get()
        itemCount = int(self.spinbox_startingCount.get())
        itemInfo = {
            "type" : itemType,
            "rating" : self.spinbox_rating.get(),
            "count" : itemCount,
            "startingCount" : itemCount
        }
        return itemName, itemInfo
    
    def validate_new_item(self):
        itemName, itemInfo = self.get_new_item_info()

        if (itemName == "" or itemName.isspace() == True):
            return False
        
        if (itemInfo['type'] == ""):
            return False
        
        return True
    
    def submit_new_item(self):
        isNewItemValid = self.validate_new_item()
        if (isNewItemValid == True):
            itemName, itemInfo = self.get_new_item_info()
            self.itemInfo[itemName] = itemInfo
            utilities.save_item_info(self.itemInfo)

            if (itemInfo['type'] == "food"):
                self.frame_foodTree.add_items_to_tree()
            elif (itemInfo['type'] == "drink"):
                self.frame_drinkTree.add_items_to_tree()
            
            self.clear_item_input()
        else:
            messagebox.showerror("Invalid Info", "Item Information Is Invalid")
    
    def clear_item_input(self):
        self.entry_name.delete(0, tk.END)
        self.spinbox_rating.set("Okay")
        self.spinbox_startingCount.set(0)

class ItemTree(ttk.Frame):

    def __init__(self, parent, itemType, gridSettings):
        super().__init__(parent)
        self.parent = parent
        self.itemType = itemType

        self.refresh_saved_info()

        treeviewHeaders = {
            "Index" : 50,
            "Name" : 300, 
            "Rating" : 200, 
            "Count" : 100
        }
        self.treeview_itemCount = ttk.Treeview(
            self, 
            columns = list(treeviewHeaders.keys()), 
            height = 20,
            show = "headings"
        )
        self.treeview_itemCount.column("#0", width = 50)
        for header, columnWidth in treeviewHeaders.items():
            self.treeview_itemCount.heading(header, text = header)
            self.treeview_itemCount.column(header, width = columnWidth)
        self.treeview_itemCount.bind("<Expose>", self.add_items_to_tree)
        self.treeview_itemCount.grid(row = 0, column = 0, **gridSettings)

        self.scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = self.treeview_itemCount.yview)
        self.scrollbar.grid(row = 0, column = 1, sticky = "NS")
        self.treeview_itemCount.configure(yscrollcommand = self.scrollbar.set)

        self.add_items_to_tree()

    def refresh_saved_info(self):
        self.dailyEntries = utilities.get_daily_entries()
        self.itemInfo = utilities.get_item_info()
        self.restaurantInfo = utilities.get_restaurant_info()
        self.settings = utilities.get_settings()
    
    def add_items_to_tree(self, event = None):
        self.refresh_saved_info()
        alphaSorted = sorted(self.itemInfo.items(), key = lambda x:x[0], reverse = False)
        sortedItems = sorted(alphaSorted, key = lambda x:x[1]['count'], reverse = True)

        for itemName, itemInfo in sortedItems:
            if (self.treeview_itemCount.exists(itemName.lower())):
                self.treeview_itemCount.delete(itemName.lower())
            if (itemInfo['type'] == self.itemType):
                itemValues = [sortedItems.index((itemName, itemInfo)) + 1, itemName, itemInfo['rating'].title(), itemInfo['count']]
                self.treeview_itemCount.insert(parent = "", index = "end", iid = itemName.lower(), values = itemValues)