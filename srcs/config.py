import os

# PATH = os.path.expanduser('~/') + "maya/2020/prefs/cs"
PATH = "./"
NAME = "config"

def write(name, value):
    prefVars = {} 
    fPath = os.path.join(PATH, NAME)
    if not os.path.isdir(PATH):
        os.makedirs(PATH)
    if os.path.isfile(fPath):   
        with open(fPath, "r") as f:
            l = f.readline()
            while l:
                res = eval(l)
                prefVars[res[0]] = res[1]
                l = f.readline()
    prefVars[name] = value
    with open(fPath, "w+") as f:
        for key in prefVars:
            f.writelines(str(key) + ":" + str(prefVars[key]) + "\n")

def read(name):
    fPath = os.path.join(PATH, NAME)
    if not os.path.isdir(PATH):
        return None
    if not os.path.isfile(fPath):
        return None
    prefVars = {}    
    with open(fPath, "r") as f:
        l = f.readline()
        while l:
            varName = l.split(":")[0].replace(" ", "")
            varValue = l[l.index(":") + 1:].lstrip().rstrip("\n")
            prefVars[varName] = varValue
            if varName == name:
                return(varValue)
            l = f.readline()
    return None
