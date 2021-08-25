# -- coding: utf-8 --
'''Interact with the config file to recover data
Must be data than change  very infrequently
'''

__author__      = "Adrien PARIS"
__email__       = "a.paris.cs@gmail.com"

import os
import keyring
from cryptography.fernet import Fernet

# PATH = os.path.expanduser('~/') + "maya/2020/prefs/cs"
PATH = "./"
NAME = "config"
SERVICE = "gapalion"
secret_key = None

def write(name, value, secret=False):
    global secret_key
    prefVars = {} 
    fPath = os.path.join(PATH, NAME)

    if not os.path.isdir(PATH):
        os.makedirs(PATH)
    if os.path.isfile(fPath):   
        with open(fPath, "r") as f:
            l = f.readline()
            while l:
                varName = l.split(":")[0].replace(" ", "")
                varValue = l[l.index(":") + 1:].lstrip().rstrip("\n")
                prefVars[varName] = varValue
                l = f.readline()
    # if the value must be secret, crypt it, and store the crypting key in the OS vault
    if secret:
        if secret_key == None:
            secret_key = keyring.get_password(SERVICE, "secret_key")
        if secret_key == None:
            secret_key = Fernet.generate_key()
            keyring.set_password(SERVICE, "secret_key", secret_key.decode())
        fernet = Fernet(secret_key)
        value = fernet.encrypt(value.encode()).decode()

    prefVars[name] = value
    with open(fPath, "w+") as f:
        for key in prefVars:
            f.writelines(str(key) + ":" + str(prefVars[key]) + "\n")

def read(name, secret=False):
    global secret_key
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
                if secret:
                    if secret_key == None:
                        secret_key = keyring.get_password(SERVICE, "secret_key")
                    fernet = Fernet(secret_key)
                    varValue = fernet.decrypt(varValue.encode()).decode()

                return(varValue)
            l = f.readline()
    return None
