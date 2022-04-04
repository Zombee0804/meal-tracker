
import datetime as dt
import os, pathlib, json

projectDir = str(pathlib.Path(__file__).parent.parent.absolute())
filesDir = projectDir + "\\files\\"

#region File Handling
# Lambdas
get_settings = lambda: read_json("settings.json", fillerContents = {})
save_settings = lambda settings: write_json("settings.json", settings)

get_daily_entries = lambda: read_json("dailyEntries.json", fillerContents = {})
save_daily_entries = lambda dailyEntries: write_json("dailyEntries.json", dailyEntries)

get_item_info = lambda: read_json(
    "itemInfo.json", 
    fillerContents = {
        "skipped_meal" : {
            "type" : "food",
            "rating" : "none",
            "count" : 0,
            "startingCount" : 0
        }
    }
)
save_item_info = lambda itemInfo: write_json("itemInfo.json", itemInfo)

get_restaurant_info = lambda: read_json("restaurantInfo.json", {"home" : {"count" : 0, "startingCount" : 0}})
save_restaurant_info = lambda restaurantInfo: write_json("restaurantInfo.json", restaurantInfo)

# Methods
def read_json(fileName, fillerContents = None, directoryPath = filesDir):
    filePath = directoryPath + fileName
    try:
        with open(filePath, 'r') as fileReader:
            fileContents = json.load(fileReader)
    except FileNotFoundError:
        fileContents = fillerContents
        write_json(fileName, fileContents, directoryPath)

    return fileContents

def write_json(fileName, fileContents, directoryPath = filesDir):
    filePath = directoryPath + fileName

    if (directoryPath != "" and directoryPath.isspace() == False):
        try:
            os.mkdir(directoryPath)
        except FileExistsError:
            pass

    with open(filePath, 'w+') as fileWriter:
        json.dump(fileContents, fileWriter)
#endregion

#region Daily Entires
def get_date_list():
    settings = get_settings()
    startDate = dt.datetime.strptime(settings['startDate'], r"%d/%m/%Y").date()
    endDate = dt.date.today() + dt.timedelta(days = 1)
    dateList = []
    for x in range(int((endDate - startDate).days)):
        xDate = startDate + dt.timedelta(x)
        dateList.append(xDate.strftime(r"%d/%m/%Y"))
    return dateList

def get_date_string(datetimeObject = None):
    if (datetimeObject == None):
        datetimeObject = date.today()
    return f'{datetimeObject.day:>02}/{datetimeObject.month:>02}/{datetimeObject.year:>04}'
#endregion

#region Other
# String Arrays
lower_string_array = lambda array: [element.lower() for element in array]
title_string_array = lambda array: [element.title() for element in array]
#endregion