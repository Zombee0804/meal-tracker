
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import Utilities as utilities

class DailyTab(ttk.Frame):

    def __init__(self):
        super().__init__()

        self.refresh_saved_info()

        gridSettings = self.settings['padding'] | {'sticky' : 'w'}

        #region Widget Setup
        # Settings Frame
        self.frame_dateSelection = ttk.Frame(self)
        self.frame_dateSelection.grid(row = 0, column = 0, columnspan = 2, **gridSettings)

        self.label_dates = ttk.Label(self.frame_dateSelection, text = "Date: ", font = self.settings['fonts']['bold'])
        self.label_dates.grid(row = 0, column = 0, **gridSettings)
        
        dates = utilities.get_date_list()
        self.spinbox_dates = ttk.Spinbox(
            self.frame_dateSelection, 
            font = self.settings['fonts']['default'], 
            values = dates, 
            state = "readonly", 
            command = self.update_daily
        )
        self.spinbox_dates.set(dates[-1])
        self.spinbox_dates.grid(row = 0, column = 1, **gridSettings)
        
        self.button_save = ttk.Button(
            self.frame_dateSelection, 
            text = "Save", 
            command = self.save_daily, 
            style = "Accent.TButton"
        )
        self.button_save.grid(row = 0, column = 2, **gridSettings)

        # Meal Frames
        self.frame_breakfast = MealFrame(self, "Breakfast", gridSettings)
        self.frame_breakfast.grid(row = 1, column = 0, **gridSettings)

        self.frame_lunch = MealFrame(self, "Lunch", gridSettings)
        self.frame_lunch.grid(row = 2, column = 0, **gridSettings)

        self.frame_dinner = MealFrame(self, "Dinner", gridSettings)
        self.frame_dinner.grid(row = 1, column = 1, **gridSettings)

        self.frame_snacks = MealFrame(self, "Snacks", gridSettings)
        self.frame_snacks.grid(row = 2, column = 1, **gridSettings)
        
        self.mealFrames = [self.frame_breakfast, self.frame_lunch, self.frame_dinner, self.frame_snacks]
        #endregion
    
        self.update_daily()
        self.bind("<Expose>", self.update_daily)

    def refresh_saved_info(self):
        self.dailyEntries = utilities.get_daily_entries()
        self.itemInfo = utilities.get_item_info()
        self.restaurantInfo = utilities.get_restaurant_info()
        self.settings = utilities.get_settings()

    def save_daily(self):
        dailyEntry = {}
        for mealFrame in self.mealFrames:
            if mealFrame.state == "INVALID" or mealFrame.state == "BLANK":
                messagebox.showerror("Error", "Invalid Entries")
                return

            mealData = mealFrame.get_meal_data()
            mealFrame.update_counts(mealData)
            dailyEntry[mealFrame.labelText] = mealData

        dailyEntries = utilities.get_daily_entries()
        dailyEntries[self.spinbox_dates.get()] = dailyEntry
        utilities.save_daily_entries(dailyEntries)

        for mealFrame in self.mealFrames:
            mealFrame.validate_items()

        messagebox.showinfo("Saved", "Daily Entry Saved")
    
    def update_daily(self, event = None):
        dailyEntries = utilities.get_daily_entries()
        dateKey = self.spinbox_dates.get()

        if (dateKey not in dailyEntries.keys()):
            dailyEntries[dateKey] = {
                "Breakfast" : {'items' : [], 'establishment' : "None"},
                "Lunch" : {'items' : [], 'establishment' : "None"},
                "Dinner" : {'items' : [], 'establishment' : "None"},
                "Snacks" : {'items' : []}
            }
            utilities.save_daily_entries(dailyEntries)

        dailyEntry = dailyEntries[dateKey]

        for mealFrame in self.mealFrames:
            meal = mealFrame.labelText
            mealFrame.text_itemBox.delete(0.0, tk.END)
            mealFrame.text_itemBox.insert(0.0, '\n'.join(dailyEntry[meal]['items']))

            if (meal != "Snacks"):
                mealFrame.combo_restaurant.set(dailyEntry[meal]['establishment'])

            mealFrame.validate_items()
    
    def set_spinbox_state(self, event = None):
        for mealFrame in self.mealFrames:
            if mealFrame.state == "INVALID" or mealFrame.state == "MODIFIED":
                self.spinbox_dates.configure(state = tk.DISABLED)
                return
        
        self.spinbox_dates.configure(state = tk.NORMAL)

class MealFrame(ttk.Frame):

    def __init__(self, parent, labelText, gridSettings):
        super().__init__(parent)
        self.parent = parent
        self.labelText = labelText

        self.refresh_saved_info()

        self.label_title = ttk.Label(self, text = labelText, font = self.settings['fonts']['bold'])
        if (self.labelText != "Snacks"):
            self.label_title.grid(row = 0, column = 0, **gridSettings)
        else:
            self.label_title.grid(row = 0, column = 0, sticky = "w", padx = gridSettings['padx'], pady = gridSettings['pady'] + 8)

        if (labelText != "Snacks"):
            self.combo_restaurant = ttk.Combobox(
                self, 
                font = self.settings['fonts']['default'], 
                values = utilities.title_string_array(self.restaurantInfo.keys()),
                state= "readonly"
            )
            self.combo_restaurant.set("None")
            self.combo_restaurant.bind("<Expose>", self.update_restaurant_list)
            self.combo_restaurant.grid(row = 0, column = 1, **gridSettings)

        self.text_itemBox = tk.Text(self, height = 17, width = 105, foreground = "#DD5555")
        self.text_itemBox.bind("<Any-KeyRelease>", self.validate_items)
        self.text_itemBox.grid(row = 1, column = 0, columnspan = 3, **gridSettings)

        self.state = "INVALID"
    
    def refresh_saved_info(self):
        self.dailyEntries = utilities.get_daily_entries()
        self.itemInfo = utilities.get_item_info()
        self.restaurantInfo = utilities.get_restaurant_info()
        self.settings = utilities.get_settings()
    
    def get_meal_data(self):
        text = self.text_itemBox.get(0.0, tk.END)
        entry = {
            'items' : [item for item in text.splitlines() if item.isspace() == False and item != ""]
        }
        if (self.labelText != "Snacks"):
            entry['establishment'] = self.combo_restaurant.get()
        return entry

    def validate_items(self, event = None):
        self.refresh_saved_info()
        existingItems = utilities.lower_string_array(self.itemInfo.keys())

        self.state = "VALID"
        self.text_itemBox.tag_delete(self.text_itemBox.tag_names()) # Removes all existing colours
        text = self.text_itemBox.get(0.0, tk.END) # Gets all text from the text box

        textBoxTags = {}
        for i, line in enumerate(text.splitlines()): # Assigning Tags To Each Line
            i += 1
            tagName = f"line_{i:>02}"
            self.text_itemBox.tag_add(tagName, f"{i}.0", f"{i}.end")
            textBoxTags[tagName] = {"contents" : line.lower(), "state" : None}
        
        previousItemCount = self.get_item_count(self.dailyEntries[self.parent.spinbox_dates.get()][self.labelText])
        
        currentItemCount = {}
        for i, (key, value) in enumerate(textBoxTags.items()): # Checking Tag Validity
            contents = value['contents']     
            if (contents == "" or contents.isspace() == True):
                textBoxTags[key]['state'] = "blank"
                continue

            if (contents not in existingItems):
                textBoxTags[key]['state'] = "invalid"
            else:
                if (contents in currentItemCount.keys()):
                    currentItemCount[contents] += 1
                else:
                    currentItemCount[contents] = 1
                
                if (contents in previousItemCount.keys()):
                    if (currentItemCount[contents] > previousItemCount[contents]):
                        textBoxTags[key]['state'] = "modified"
                    else:
                        textBoxTags[key]['state'] = "valid"
                else:
                    textBoxTags[key]['state'] = "modified"

        validityCount = {"valid" : 0, "modified" : 0, "invalid" : 0}  
        for key, value in textBoxTags.items(): # Setting Tag Colours
            if (value['state'] == "valid"):
                self.text_itemBox.tag_config(key, foreground = "#55DD55")
                validityCount[value['state']] += 1
            elif (value['state'] == "modified"):
                self.text_itemBox.tag_config(key, foreground = "#FF9955")
                validityCount[value['state']] += 1
            elif (value['state'] == "invalid"):
                self.text_itemBox.tag_config(key, foreground = "#DD5555")
                validityCount[value['state']] += 1

        # State Settings
        if (validityCount['invalid'] == 0):
            if (validityCount['modified'] > 0):
                self.state = "MODIFIED"
            else:
                if (previousItemCount == currentItemCount):
                    self.state = "VALID"
                else:
                        self.state = "MODIFIED"
        else:
            self.state = "INVALID"
        
        self.parent.set_spinbox_state()
        
    def get_item_count(self, mealData):
        itemList = mealData['items']
        itemCounts = {}
        for item in itemList:
            item = item.lower()
            if (item in itemCounts.keys()):
                itemCounts[item] += 1
            else:
                itemCounts[item] = 1
        return itemCounts
    
    def update_counts(self, mealData):
        self.refresh_saved_info()

        # Removing Previous Count
        previousEntry = self.dailyEntries[self.parent.spinbox_dates.get()][self.labelText]
        previousItemCount = self.get_item_count(previousEntry)
        
        for key, value in previousItemCount.items():
                self.itemInfo[utilities.find_dict_key(self.itemInfo, key)]['count'] -= value
        
        if (self.labelText != "Snacks" and "skipped_meal" not in previousEntry['items'] and previousEntry['items'] != []):
            self.restaurantInfo[utilities.find_dict_key(self.restaurantInfo, previousEntry['establishment'])]['count'] -= 1
        
        # Adding Current Count
        currentEntry = self.get_meal_data()
        currentItemCount = self.get_item_count(currentEntry)

        for key, value in currentItemCount.items():
            self.itemInfo[utilities.find_dict_key(self.itemInfo, key)]['count'] += value
        
        if (self.labelText != "Snacks" and "skipped_meal" not in currentEntry['items'] and currentEntry['items'] != []):
            self.restaurantInfo[utilities.find_dict_key(self.restaurantInfo, self.combo_restaurant.get())]['count'] += 1
            
        utilities.save_item_info(self.itemInfo)
        utilities.save_restaurant_info(self.restaurantInfo)
    
    def update_restaurant_list(self, event = None):
        self.refresh_saved_info()
        self.combo_restaurant.configure(values = utilities.title_string_array(self.restaurantInfo.keys()))