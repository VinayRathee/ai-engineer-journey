class TaskItem:
    def __init__(self, title, status=False):
        self.title = title
        self.status = status

    def markDone(self):
        self.status = True

    def toDict(self):
        return {
            "title": self.title,
            "status": self.status
        }
