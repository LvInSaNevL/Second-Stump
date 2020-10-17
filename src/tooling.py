import os
import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def prettyPrint(color, text):
    logfile = open(fullPath("data/logfile"),"a")
    logfile.write("[{}]: {}\n".format(datetime.datetime.now(), text))
    print(color + text + bcolors.ENDC)

def fullPath(path):
    cwd = os.path.dirname(os.path.abspath(__file__)) + "/"
    return (cwd + path)