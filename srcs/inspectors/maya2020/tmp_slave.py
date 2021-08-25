# -- coding: utf-8 --

from subprocess import STDOUT, STD_ERROR_HANDLE
import maya
import sys

import importlib

import sys
import os
'''
The first arguments must always be the resources path folder
'''

def printModule(module):
    dico = {}
    dico["name"] = module.__name__.split(".")[-1]
    dico["author"] = None
    if hasattr(module, '__author__'):
        if module.__author__ != "prenom NOM":
            dico["author"] = unicode(module.__author__)
    dico["email"] = unicode(module.__email__) if hasattr(module, '__email__') else None
    dico["title"] = unicode(module.title) if hasattr(module, 'title') else None
    dico["tags"] = unicode(module.tags) if hasattr(module, 'tags') else None
    dico["explanation"] = unicode(module.explanation) if hasattr(module, 'explanation') else None
    dico["explanation"] = unicode(module.__doc__) if hasattr(module, '__doc__') else None
    dico["image"] = None
    if module.image != "":
        if hasattr(module, 'image'):
            dico["image"] = unicode(module.image)
    print(dico)




def loadAllTrial(rsrcs_path):
    sys.path.append(rsrcs_path) if rsrcs_path not in sys.path else None
    modulename = "maya2020_invg"
    with open(os.devnull,"w") as devNull:
        original = sys.stdout
        sys.stdout = devNull
        invg_mod = importlib.import_module(modulename)
        invg_mod = __import__(modulename)
        sys.stdout = original 
        for t in invg_mod.__all__:
            if t == "template":
                continue
            mod_t = importlib.import_module(modulename + "." + t)
            printModule(mod_t)
            # loadTrial(invg_mod + "." + t)

# def loadTrial(name):
#         moduleName = "trials." + name
#         print(moduleName)
        # sys.path.append(resource_path)
        # try:
        #     module = importlib.import_module(moduleName)
        #     tload = trial.Trial(module.title, module.trial)
        #     tload.loadTrial(module)
        #     if hasattr(module, 'image'):
        #         if module.image != "":
        #             self.images.add(module.image)
        #     self.trials.append(tload)
        # except Exception as e:
        #     e = str(e)
        #     print("{} : can not be loaded \n {}".format(name, e))



if __name__ == "__main__":
    if len(sys.argv) == 3:
        if sys.argv[2] == "ls":
            ag = sys.argv[1:]
            rsrcs_path = ag.pop(0) + "/trials"
            loadAllTrial(rsrcs_path)
    elif len(sys.argv) / 2 != 0 and len(sys.argv):
        ag = sys.argv[1:]
        rsrcs_path = ag.pop(0) + "/trials"
        files_eval = [sys.argv[i:i+2] for i in range(2, len(sys.argv), 2)]
        for file, tags in files_eval:
            print(file)
            print(tags)