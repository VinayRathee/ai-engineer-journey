from .storage import loadData, saveData
from .models import TaskItem

class TaskManager:
    def __init__(self):
        self.tasks = loadData()

    def addTask(self, t):
        newItem = TaskItem(t)
        self.tasks.append(newItem)
        saveData(self.tasks)
        print("added")

    def getItems(self):
        return self.tasks

    def completeTask(self, idx):
        self.tasks[idx].markDone()
        saveData(self.tasks)
