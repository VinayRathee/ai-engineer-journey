import sys
from .manager import TaskManager
from .formatter import formatOutput

class AppCLI:
    def __init__(self):
        self.mgr = TaskManager()

    def runCli(self):
        args = sys.argv[1:]
        if not args:
            print("usage: python -m chapter-06b.messy-todo.main <cmd>")
            return
        cmd = args[0]
        if cmd == "add":
            title = " ".join(args[1:])
            self.mgr.addTask(title)
        elif cmd == "list":
            items = self.mgr.getItems()
            print(formatOutput(items))
        else:
            print("unknown command")

def runCli():
    cli = AppCLI()
    cli.runCli()
