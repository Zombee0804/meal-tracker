# Plan
## Function
#### Daily Tabs
* One page for each day. Each page contains a box for: Breakfast, Lunch, Dinner, and Snacks
* Each meal has a dropdown box to specify the restaurant (or home). This will only accept resturants added in the restaurants tab
* The meal box will also have a '+' button to add an item
    * Items can be food or drink
    * Items consist of an entry field and an label widget
    * The label widget will either display:
        * **Error** - If the item has not been added in the items tab
        * **Modified** - If the item is new or been changed since the last save
        * **Save** - If there are no changes to the item
* On each day page, there is a save button. This will save each meal, removing the 'Modified' tag from each item
* Daily entries can be edited, but remember to make sure that removed items are deleted from storage once the save button is pressed

#### Items Tab
* The items tab contains two large treeview widgets, one for food and one for drink
* At the top of the page is a box to add a new item, specifying:
    * Name
    * Type (Food or Drink)
    * Rating (Very Bad, Bad, Okay, Good, Very Good, Outstanding)
    * Potentially a Food Group or Drink Group (although this gets complicated with certain items, will be finalised later)
    * An optional 'Starting Count', as I personally have been tracking food using a spreadsheet for almost a year and want to transfer the data over
* As additional functionality later down the line, items should be able to be edited or merged with other items
* Also as additional functionality, searching or filtering the treeviews

#### Restaurants Tab
* The restaurants tab will allow the user to add a restaurant or food establishment
* This can then be used in the daily tabs to specify which restaurant the meal was from (with the additional option of 'Home')
* The tab will also contain a treeview displaying the restaurants and the amount of meals that have been had there, also with a 'Most popular food'

## Storage
* The daily meals will be stored in a two-tier dictionary:
    ```
    {
        '00/00/0000' : {
            'breakfast' : [
                'item01',
                'item02',
                'item03'
            ]
        }
    }
    ```
* Item information will be stored seperately in a two-tier array:
    ```
    [
        [name, type, rating, count],
        ...
    ]
    ```
* Upon each save on the daily tabs, the total item counts will be calculate (remembering to subtract for removed items)