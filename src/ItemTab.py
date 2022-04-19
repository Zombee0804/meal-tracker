
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import Utilities as utilities

class ItemTab(ttk.Frame):

    def __init__(self):
        super().__init__()

        self.refresh_saved_info()

        gridSettings = self.settings['padding'] | {'sticky' : 'w'}

        style_labelFrame = ttk.Style(self)
        style_labelFrame.configure("TLabelframe.Label", font = self.settings['fonts']['header'], background = "#1c1c1c")

        #region New Item Frame
        self.frame_newItem = ttk.LabelFrame(self, text = " New Item ")
        self.frame_newItem.grid(row = 0, column = 0, **gridSettings)

        self.label_name = ttk.Label(self.frame_newItem, text = "Item Name:", font = self.settings['fonts']['bold'])
        self.label_name.grid(row = 0, column = 0, **gridSettings)

        self.entry_name = ttk.Entry(self.frame_newItem, font = self.settings['fonts']['default'], width = 75)
        self.entry_name.grid(row = 1, column = 0, **gridSettings)

        self.label_type = ttk.Label(self.frame_newItem, text = "Type:", font = self.settings['fonts']['bold'])
        self.label_type.grid(row = 0, column = 1, **gridSettings)

        #region Item Type
        self.frame_itemType = ttk.Frame(self.frame_newItem)
        self.frame_itemType.grid(row = 1, column = 1, **gridSettings)

        self.var_itemType = tk.StringVar()
        self.var_itemType.set("food")
        self.radio_food = ttk.Radiobutton(self.frame_itemType, text = "Food", variable = self.var_itemType, value = "food")
        self.radio_food.grid(row = 0, column = 0, **gridSettings)

        self.radio_drink = ttk.Radiobutton(self.frame_itemType, text = "Drink", variable = self.var_itemType, value = "drink")
        self.radio_drink.grid(row = 0, column = 1, **gridSettings)
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

        self.button_itemSubmit = ttk.Button(self.frame_newItem, text = "Submit", style = "Accent.TButton", command = self.submit_new_item)
        self.button_itemSubmit.grid(row = 1, column = 5, **gridSettings)
        #endregion

        #region Editing Item Frame
        self.frame_edit = ttk.LabelFrame(self, text = " Edit Item ")
        self.frame_edit.grid(row = 1, column = 0, **gridSettings)

        self.label_currentName = ttk.Label(self.frame_edit, text = "Current Name:", font = self.settings['fonts']['bold'])
        self.label_currentName.grid(row = 0, column = 0, **gridSettings)

        self.entry_currentName = ttk.Entry(self.frame_edit, font = self.settings['fonts']['default'], width = 50)
        self.entry_currentName.grid(row = 1, column = 0, **gridSettings)

        self.label_arrow = ttk.Label(self.frame_edit, text = "-->", font = self.settings['fonts']['default'])
        self.label_arrow.grid(row = 1, column = 1, **gridSettings)

        self.label_newName = ttk.Label(self.frame_edit, text = "New Name:", font = self.settings['fonts']['bold'])
        self.label_newName.grid(row = 0, column = 2, **gridSettings)

        self.entry_newName = ttk.Entry(self.frame_edit, font = self.settings['fonts']['default'], width = 50)
        self.entry_newName.grid(row = 1, column = 2, **gridSettings)

        self.button_editSubmit = ttk.Button(self.frame_edit, text = "Submit", style = "Accent.TButton", command = self.submit_item_edit)
        self.button_editSubmit.grid(row = 1, column = 3, **gridSettings)
        #endregion

        #region Item Count Frame
        self.frame_itemCount = ttk.LabelFrame(self, text = " Item Counts ")
        self.frame_itemCount.grid(row = 2, column = 0, **gridSettings)

        self.button_recount = ttk.Button(self.frame_itemCount, text = "Recount Items", command = self.force_recount)
        self.button_recount.grid(row = 0, column = 0, padx = gridSettings['padx'] * 3, pady = gridSettings['pady'], sticky = gridSettings['sticky'])

        self.frame_foodTree = ItemTree(self.frame_itemCount, self, "food", gridSettings)
        self.frame_foodTree.grid(row = 1, column = 0, **gridSettings)

        self.frame_drinkTree = ItemTree(self.frame_itemCount, self, "drink", gridSettings)
        self.frame_drinkTree.grid(row = 1, column = 1, **gridSettings)
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
        self.refresh_saved_info()
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

    def update_edit_box(self, treeFrame):
        focusItem = treeFrame.treeview_itemCount.focus()
        if (focusItem != "skipped_meal"):
            self.entry_currentName.delete(0, tk.END)
            self.entry_currentName.insert(0, utilities.find_dict_key(self.itemInfo, treeFrame.treeview_itemCount.focus()))
   
    def submit_item_edit(self):
        currentName = self.entry_currentName.get()
        newName = self.entry_newName.get()
        if (currentName == "" or currentName.isspace() == True or newName == "" or newName.isspace() == True):
            messagebox.showerror("Item Edit Error", "Edit Information Empty")
            return
        
        self.refresh_saved_info()

        if (utilities.is_element_in_list(self.itemInfo.keys(), currentName) == False):
            messagebox.showerror("Item Edit Error", "Item Not Found")
            return
        
        currentName = utilities.find_dict_key(self.itemInfo, currentName)
        itemInformation = self.itemInfo[currentName]
        self.itemInfo.pop(currentName)
        self.itemInfo[newName] = itemInformation

        for date, entries in self.dailyEntries.items():
            for meal, entry in entries.items():
                if (utilities.is_element_in_list(entry['items'], currentName)):
                    entry['items'] = utilities.list_replace(entry['items'], currentName, newName)
        
        utilities.save_item_info(self.itemInfo)
        utilities.save_daily_entries(self.dailyEntries)

        messagebox.showinfo("Edit Complete", "Edit Complete!")

        self.entry_currentName.delete(0, tk.END)
        self.entry_newName.delete(0, tk.END)

        itemType = self.itemInfo[newName]['type']
        if (itemType == "food"):
            self.frame_foodTree.add_items_to_tree()
        elif (itemType == "drink"):
            self.frame_drinkTree.add_items_to_tree()
    
    def force_recount(self, event = None):
        self.refresh_saved_info()

        newCount = {key:0 for (key, value) in self.itemInfo.items()}

        for itemName in newCount.keys():
            for date, entries in self.dailyEntries.items():
                for meal, entry in entries.items():
                    newCount[itemName] += utilities.element_count_in_list(entry['items'], itemName)
        
        for item, itemData in self.itemInfo.items():
            self.itemInfo[item]['count'] = newCount[item] + self.itemInfo[item]['startingCount']
        
        utilities.save_item_info(self.itemInfo)

        self.frame_foodTree.add_items_to_tree()
        self.frame_drinkTree.add_items_to_tree()

class ItemTree(ttk.Frame):

    def __init__(self, parent, root, itemType, gridSettings):
        super().__init__(parent)
        self.parent = parent
        self.root = root
        self.itemType = itemType

        self.refresh_saved_info()
        self.searchQuery = None

        #region Search Bar
        self.frame_search = ttk.Frame(self)
        self.frame_search.grid(row = 0, column = 0, **gridSettings)

        self.label_search = ttk.Label(self.frame_search, text = "Search:", font = self.settings['fonts']['bold'])
        self.label_search.grid(row = 0, column = 0, **gridSettings)

        self.entry_query = ttk.Entry(self.frame_search, font = self.settings['fonts']['default'], width = 69)
        self.entry_query.bind("<Any-KeyRelease>", self.submit_search_query)
        self.entry_query.grid(row = 0, column = 1, **gridSettings)
        #endregion

        #region Treeview
        self.frame_tree = ttk.Frame(self)
        self.frame_tree.grid(row = 1, column = 0, **gridSettings)

        treeviewHeaders = {
            "Index" : 50,
            "Name" : 300, 
            "Rating" : 200, 
            "Count" : 100
        }
        self.treeview_itemCount = ttk.Treeview(
            self.frame_tree, 
            columns = list(treeviewHeaders.keys()), 
            height = 9,
            show = "headings"
        )
        self.treeview_itemCount.column("#0", width = 50)
        for header, columnWidth in treeviewHeaders.items():
            self.treeview_itemCount.heading(header, text = header)
            self.treeview_itemCount.column(header, width = columnWidth)
        self.treeview_itemCount.bind("<Expose>", self.add_items_to_tree)
        self.treeview_itemCount.bind("<KeyRelease-Delete>", self.delete_selected_item)
        self.treeview_itemCount.bind("<ButtonRelease>", lambda e: self.root.update_edit_box(self))
        self.treeview_itemCount.grid(row = 0, column = 0, **gridSettings)

        self.scrollbar = ttk.Scrollbar(self.frame_tree, orient = tk.VERTICAL, command = self.treeview_itemCount.yview)
        self.scrollbar.grid(row = 0, column = 1, sticky = "NS")
        self.treeview_itemCount.configure(yscrollcommand = self.scrollbar.set)

        self.button_delete = ttk.Button(self.frame_tree, text = "Delete", style = "Accent.TButton", command = self.delete_selected_item)
        self.button_delete.grid(row = 1, column = 0, columnspan = 2, sticky = "E", padx = gridSettings['padx'], pady = gridSettings['pady'])

        self.add_items_to_tree()
        #endregion

    def refresh_saved_info(self):
        self.dailyEntries = utilities.get_daily_entries()
        self.itemInfo = utilities.get_item_info()
        self.restaurantInfo = utilities.get_restaurant_info()
        self.settings = utilities.get_settings()
    
    def add_items_to_tree(self, event = None):
        self.refresh_saved_info()
        alphaSorted = sorted(self.itemInfo.items(), key = lambda x:x[0], reverse = False)
        sortedItems = sorted(alphaSorted, key = lambda x:x[1]['count'], reverse = True)
        filteredItems = [i for i in sortedItems if i[1]['type'] == self.itemType]

        for iid in self.treeview_itemCount.get_children():
            self.treeview_itemCount.delete(iid)

        for itemName, itemInfo in filteredItems:
            if (itemInfo['type'] == self.itemType):
                if (self.searchQuery == None or self.searchQuery.lower() in itemName.lower()):
                    itemValues = [filteredItems.index((itemName, itemInfo)) + 1, itemName, itemInfo['rating'].title(), itemInfo['count']]
                    self.treeview_itemCount.insert(parent = "", index = "end", iid = itemName.lower(), values = itemValues)

    def submit_search_query(self, event = None):
        query = self.entry_query.get()
        if (query == "" or query.isspace() == True):
            self.searchQuery = None
        else:
            self.searchQuery = query
        self.add_items_to_tree()
    
    def delete_selected_item(self, event = None):
        self.refresh_saved_info()

        deleteItem = self.treeview_itemCount.focus()

        if (deleteItem.lower() == "skipped_meal"):
            messagebox.showerror("Deletion Error!", "Cannot Delete This Item")
            return

        if (deleteItem != "" and deleteItem.isspace() == False):
            for date, entry in self.dailyEntries.items():
                for mealName, mealInfo in entry.items():
                    for index, mealItem in enumerate(mealInfo['items']):
                        if (mealItem.lower() == deleteItem.lower()):
                            mealInfo['items'].pop(index)
        
        self.itemInfo.pop(utilities.find_dict_key(self.itemInfo, deleteItem))
        
        utilities.save_daily_entries(self.dailyEntries)
        utilities.save_item_info(self.itemInfo)

        self.add_items_to_tree()