
# -- coding: utf-8 --

from datetime import datetime
import sys
import os
import importlib
import io

import trials
import trial
from scopeHtml import Scope

#====================================================================#

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
        moduleName = "trials." + name
        # print(moduleName)
        try:
            module = importlib.import_module(moduleName)
            tload = trial.Trial(module.title, module.trial)
            tload.loadTrial(module)
            if hasattr(module, 'image'):
                if module.image != "":
                    self.images.add(module.image)
            self.trials.append(tload)
        except Exception as e:
            e = str(e)
            print("{} : can not be loaded \n {}".format(name, e))


    def loadAllTrial(self):
        for t in trials.__all__:
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
