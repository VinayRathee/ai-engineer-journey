import json
import os

FILE_PATH = "todos.json"

def loadData():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        try:
            d = json.load(f)
            return d
        except:
            return []

def saveData(lst):
    dataToSave = []
    for item in lst:
        dataToSave.append(item.toDict())
    with open(FILE_PATH, "w") as f:
        json.dump(dataToSave, f)
