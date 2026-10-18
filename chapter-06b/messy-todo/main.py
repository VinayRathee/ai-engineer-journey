import sys
from .cli import runCli

def startApp():
    try:
        runCli()
    except Exception as e:
        print("err:", e)

if __name__ == "__main__":
    startApp()
