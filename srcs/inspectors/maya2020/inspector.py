
from datetime import datetime
import sys
import os
import importlib
import io

#====================================================================#

#TODO Get maya location from config file
MAYA_LOCATION = "C:/Program Files/Autodesk/Maya2020"
PYTHON_LOCATION = MAYA_LOCATION + "/Python/Lib/site-packages"

os.environ["MAYA_LOCATION"] = MAYA_LOCATION
os.environ["PYTHONPATH"] = PYTHON_LOCATION

sys.path.append(MAYA_LOCATION)
sys.path.append(PYTHON_LOCATION)
sys.path.append(MAYA_LOCATION+"/bin")
sys.path.append(MAYA_LOCATION+"/lib")
sys.path.append(MAYA_LOCATION+"/Python")
sys.path.append(MAYA_LOCATION+"/Python/DLLs")
sys.path.append(MAYA_LOCATION+"/Python/Lib")
sys.path.append(MAYA_LOCATION+"/Python/Lib/plat-win")
sys.path.append(MAYA_LOCATION+"/Python/Lib/lib-tk")
# print('\n'.join(sys.path))
import maya.standalone
maya.standalone.initialize(name='python')
import maya.cmds as cmds

import investigations


class Drill():
    def __init__(self, title, func):
        self.title = title
        self.explanation = ""
        self.author = ""
        self.email = ""
        self.image = "gears"
        
        self.func = func
        self.passed = False
        self.errors = []
    
    def loadTrial(self, module):
        if hasattr(module, '__author__'):
            if module.__author__ != "prenom NOM":
                self.author = unicode(module.__author__)
        if hasattr(module, '__email__'):
            self.email = unicode(module.__email__)
        if hasattr(module, 'explanation'):
            self.explanation = unicode(module.explanation)
        if hasattr(module, '__doc__'):
            self.explanation = unicode(module.__doc__)
        if hasattr(module, 'image'):
            if module.image != "":
                self.image = unicode(module.image)

    def start(self):
        self.passed, self.errors = False, []
        try:
            value = self.func()
        except Exception as e:
            e = str(e)
            print("FAILED : " + self.title)
            print("\t" + e)
            if self.author == "":
                errorMessage = ["This trial has failed because it was badly written",
                                "It has been written by an Anonymous author",
                                e,
                                "Please contact {} at {} to resolve this issue".format("Adrien PARIS", "a.paris.cs@gmail.com")]
            else:
                errorMessage = ["This trial has failed because it was badly written",
                                e,
                                "Please contact {} at {} to resolve this issue".format(self.author, self.email)]
            self.passed, self.errors = True, errorMessage
            return
        if len(value) == 2:
            if not type(value[0]) == type(True):
                print("first return value should be a bool")
                return
            if not isinstance(value[1], list):
                print("no error list")
                return
            self.passed, self.errors = value[0], value[1]
        else:
            print("no enough return value : " + self.title)





class Report():
    def __init__(self, filepath):
        self.user = ""
        self.file = os.path.basename(os.path.normpath(filepath))
        self.filePath = filepath
        self.trials = []
        self.images = set()

    def runTrial(self):
        if self.file == "":
            return
        # Open your file
        try:
            cmds.file(unicode(self.filePath), o=True)
        except Exception as e:
            print(str(e))
            print("known maya import fails")
        for t in self.trials:
            t.start()

    def loadTrial(self, name):
        # sys.path.insert(1, '/path/to/application/app/folder')
        # new_module = __import__(modulename)


        moduleName = "trials." + name
        # print(moduleName)
        try:
            module = importlib.import_module(moduleName)
            tload = Drill(module.title, module.trial)
            tload.loadTrial(module)
            if hasattr(module, 'image'):
                if module.image != "":
                    self.images.add(module.image)
            self.trials.append(tload)
        except Exception as e:
            e = str(e)
            print("{} : can not be loaded \n {}".format(name, e))


    def loadAllTrial(self):
        for t in investigations.__all__:
            if t == "template":
                continue
            self.loadTrial(t)

    def toHtml(self):
        passedTrialCount = len([x for x in self.trials if x.passed])
        if passedTrialCount != 0:
            self.images.add(u"check")
        if passedTrialCount != len(self.trials):
            self.images.add(u"cross")
        for t in self.trials:
            self.images.add(t.image)

        context = { "DATE" : unicode(datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
                    "VERSION" : u"v1.0.1",
                    "PASSEDTRIAL" : unicode(passedTrialCount) + u" / " + unicode(len(self.trials)),
                    "NAME" : unicode(self.file),
                    "TRIALLIST" : self.trials
           }

        filePath = r".\templates\trialRigPres.html"
        with io.open(filePath, "r", encoding='utf8') as f:
            html = f.read()

            main = Scope.getScopesFromHtml(html)

            return main.runContext(context)



if __name__ == "__main__":
    sys.argv