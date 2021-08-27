# -- coding: utf-8 --
'''Indepedant interacting module that load drills in the resource folder
shell argument :
• must be the path to this file
• must be the path to the resource folder
            ╔══════════╩═════════════════╗
  • ╒ path to maya file                 • ls
    ╘ tag formula
  • ╒ path to maya file
    ╘ tag formula
  • ...

tag formula:
    #tag or drillName
    ex:
        (#rig*#chara-#props)*#cs-cleanNamespace
'''
__author__ = "Adrien PARIS"
__email__ = "a.paris.cs@gmail.com"

import os
import sys
import importlib
import maya.cmds as cmds

def importmaya(mayapy_path):

    MAYA_LOCATION = os.path.dirname(os.path.dirname(mayapy_path))
    PYTHON_LOCATION = os.path.join(MAYA_LOCATION, "/Python/Lib/site-packages")

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
    with open(os.devnull,"w") as devNull:
        original = sys.stdout
        sys.stdout = devNull
        import maya.standalone
        maya.standalone.initialize(name='python')
        sys.stdout = original 

def splitnonalpha(s):
   pos = 1
   while pos < len(s) and s[pos].isalpha():
      pos+=1
   return (s[:pos], s[pos:])

class ExoTag():
    exos = {}
    tag = []
    all = []

    def __init__(self, tag):
        self.name = tag
        if tag.startswith('#'):
            if tag[1:] in ExoTag.exos:
                self.tags = ExoTag.exos[tag[1:]]
            elif tag[1:] == "all":
                self.tags = ExoTag.all[:]
            else:
                self.tags = []
        else:
            self.tags = [x for x in ExoTag.all if x.name == tag]

    @staticmethod
    def convert(f):
        new_formula = ""
        i = 0
        n = 0
        allowed_char = "#ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        s = 0
        limit = 200
        while s != -1:
            limit -= 1
            if limit <= 0:
                break
            lac = [f[i:].find(a) for a in allowed_char if f[i:].find(a) != -1]
            s = min(lac) if len(lac) != 0 else -1
            if s == -1:
                break
            s += i
            tag, _ = splitnonalpha(f[s + 1:])
            tag = f[s] + tag
            ExoTag.tag.append(ExoTag(tag))
            new_formula += f[i:s] + "ExoTag.tag[{}]".format(n)
            n += 1
            i = s + len(tag)
        return new_formula
    
    def __add__(self, o):
        self.tags + o.tags
        return self
    def __sub__(self, o):
        for i in o.tags:
            self.tags = [x for x in self.tags if x not in o.tags]
        return self
    def __mul__(self, o):
        self.tags = [x for x in self.tags if x in o.tags]
        return self
    def __div__(self, o):
        self.tags = [x for x in self.tags if x not in o.tags] + [x for x in o.tags if x not in self.tags]
        return self

class Drill():
    def __init__(self, module):
        self.name = module.__name__.split(".")[-1]
        self.title = unicode(module.title) if hasattr(module, 'title') else None
        self.doc = unicode(module.__doc__) if hasattr(module, '__doc__') else None
                
        self.tags = []
        try:
            tags = eval(unicode(module.tags) if hasattr(module, 'tags') else [])
        except:
            tags = []
        if type(tags) == "unicode" or type(tags) == "str":
            self.tags.append(tags)
        else:
            self.tags.extend(tags)
        self.author = unicode(module.__author__) if hasattr(module, '__author__') else None
        self.email = unicode(module.__email__) if hasattr(module, '__email__') else None
        self.image = unicode(module.image) if hasattr(module, 'image') else None
        # self.func = module.main if hasattr(module, 'main') else None
        self.func = module.test if hasattr(module, 'test') else None
        self.file = None 
        self.status = "" #must be "SUCCESS" "ERROR" or "WARNING"
        self.passed = False
        self.message = None

    def to_dict(self):
        filter_keys = ["name", "title", "doc", "tags", "author", "email",
                      "image", "file", "passed", "status", "message"]
        return { k: self.__dict__[k] for k in filter_keys }
    
    def start(self):
        with open(os.devnull,"w") as devNull:
            original = sys.stdout
            sys.stdout = devNull
            try:
                self.check_return_value(*self.func())
            except Exception as e:
                if self.author == None:
                    self.message = [u"This drill has failed because it was badly written",
                                    u"It has been written by an Anonymous author",
                                    e,
                                    u"Please contact {} at {} to resolve this issue".format("Adrien PARIS", "a.paris.cs@gmail.com")]
                else:
                    self.message = [u"This trial has failed because it was badly written",
                                    e,
                                    u"Please contact {} at {} to resolve this issue".format(self.author, self.email)]
                self.passed = False
        sys.stdout = original 

    def check_return_value(self, *value):
        if len(value) != 2:
            self.message = ["Returned values should be to the count of 2,",
                            "a string containing ethier 'SUCCESS', 'WARNING', 'ERROR'",
                            "and a list of string, containing the error messages",
                            value]
            self.passed = False
            return
        if not isinstance(value[1], list):
            self.message = ["Returned message should be a list of str"]
            self.passed = False
            return
        if not value[0] in ["SUCCESS", "WARNING", "ERROR"]:
            self.message = ["Returned status is incorect", "Drill message:"] + value[1]
            self.passed = False
            return
        self.passed = True
        self.status = value[0]
        self.message = value[1]

    @staticmethod
    def load_drills(rsrcs_path):
        sys.path.append(rsrcs_path) if rsrcs_path not in sys.path else None
        modulename = "maya2020_invg"
        l = []
        with open(os.devnull,"w") as devNull:
            original = sys.stdout
            sys.stdout = devNull
            invg_mod = importlib.import_module(modulename)
            invg_mod = __import__(modulename)
            sys.stdout = original 
            for t in invg_mod.__all__:
                mod_t = importlib.import_module(modulename + "." + t)
                l.append(Drill(mod_t))
        return l

    @staticmethod
    def get_drills_from_tags(rsrcs_path, tags):
        drills = Drill.load_drills(rsrcs_path)
        tags_dict = {}
        for d in drills:
            ExoTag.all.append(d) if d not in ExoTag.all else None
            ts = d.tags
            for t in ts:
                if t in tags_dict:
                    tags_dict[t].append(d)
                else:
                    tags_dict[t] = [d]

        # reset list of tags
        ExoTag.tag = []
        ExoTag.exos = tags_dict
        f = ExoTag.convert(tags)
        try :
            p = eval(f)
            return p.tags
        except:
            print("'ERROR - While evaluating tag formula - [{}]'".format(tags.replace("'", "\\'")))
            return []


    @staticmethod
    def execute_drills(drills, file):
        if not os.path.exists(file):
            return False
        try:
            cmds.file(file, o=True)
        except RuntimeError as e:
            pass
        for d in drills:
            d.file = file
            d.start()
        return True


    def __repr__(self):
        return "Drills<{}>".format(self.name)


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 3:
        exit()
    
    mayapy_path = sys.executable
    rsrcs_path = argv[1] + "/drills"
    if not os.path.exists(rsrcs_path):
        exit()

    if len(argv) == 3:
        if argv[2] == "ls":
            for d in Drill.load_drills(rsrcs_path):
                print(d.to_dict())
    elif len(argv) / 2 != 0:
        files_eval = [argv[i:i+2] for i in range(2, len(argv), 2)]
        for file, tags in files_eval:
            importmaya(mayapy_path)
            drills_ls = Drill.get_drills_from_tags(rsrcs_path, tags)
            if Drill.execute_drills(drills_ls, file) == False:
                print("'ERROR - file does not exists - {}'".format(file))
                continue
            for d in drills_ls:
                print(str(d.to_dict()))