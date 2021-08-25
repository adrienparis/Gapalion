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

def drill_to_dic(drill):
    dico = {}
    dico["name"] = drill.__name__.split(".")[-1]
    dico["author"] = None
    if hasattr(drill, '__author__'):
        if drill.__author__ != "prenom NOM":
            dico["author"] = unicode(drill.__author__)
    dico["email"] = unicode(drill.__email__) if hasattr(drill, '__email__') else None
    dico["title"] = unicode(drill.title) if hasattr(drill, 'title') else None
    dico["tags"] = []
    try:
        tags = eval(unicode(drill.tags) if hasattr(drill, 'tags') else [])
    except:
        tags = []
    if type(tags) == "str":
        dico["tags"].append(tags)
    else:
        dico["tags"].extend(tags)

    dico["explanation"] = unicode(drill.explanation) if hasattr(drill, 'explanation') else None
    dico["explanation"] = unicode(drill.__doc__) if hasattr(drill, '__doc__') else None
    dico["image"] = None
    if drill.image != "":
        if hasattr(drill, 'image'):
            dico["image"] = unicode(drill.image)
    return dico

def ls_drills(rsrcs_path):
    sys.path.append(rsrcs_path) if rsrcs_path not in sys.path else None
    modulename = "maya2020_invg"
    with open(os.devnull,"w") as devNull:
        original = sys.stdout
        sys.stdout = devNull
        invg_mod = importlib.import_module(modulename)
        invg_mod = __import__(modulename)
        sys.stdout = original 
        l = []
        for t in invg_mod.__all__:
            mod_t = importlib.import_module(modulename + "." + t)
            l.append(drill_to_dic(mod_t))
        return l
    return []

formulaQuadru = "(#rig*#chara-#props)*#cs"
formulaQuadru = "(#rig*#chara-#props)*#cs-cleanNamespace"

tags = {"rig" : ["rotateOrder", "worldScale", "ctrlSet", "rigPropsTest"],
        "chara": ["rotateOrder", "worldScale", "ctrlSet"],
        "props": ["worldScale", "ctrlSet", "rigPropsTest"],
        "cs": ["rotateOrder", "worldScale", "triangle", "ctrlSet", "rigPropsTest"],
        }

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
            self.tags = [tag]

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
            self.tags = list(filter((i).__ne__, self.tags))
        return self
    def __mul__(self, o):
        self.tags = [x for x in self.tags if x in o.tags]
        return self
    def __div__(self, o):
        self.tags = [x for x in self.tags if x not in o.tags]
        return self

def execute_drills(rsrcs_path, formula):
    drills = ls_drills(rsrcs_path)
    tags = {}
    for d in drills:
        ExoTag.all.append(d["name"]) if d["name"] not in ExoTag.all else None
        ts = d["tags"]
        for t in ts:
            if t in tags:
                tags[t].append(d["name"])
            else:
                tags[t] = [d["name"]]

    ExoTag.tag = []
    ExoTag.exos = tags
    f = ExoTag.convert(formula)
    try :
        p = eval(f)
        print(p.tags)
    except:
        print("Error - While evaluating command")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        exit()

    mayapy_path = sys.executable
    rsrcs_path = sys.argv[1] + "/drills"
    if not os.path.exists(rsrcs_path):
        exit()

    if len(sys.argv) == 3:
        if sys.argv[2] == "ls":
            for i in ls_drills(rsrcs_path):
                print(i)
    elif len(sys.argv) / 2 != 0:
        files_eval = [sys.argv[i:i+2] for i in range(2, len(sys.argv), 2)]
        for file, tags in files_eval:
            print("_" * 50)
            print("file : {}".format(file))
            print("tags : {}".format(tags))
            execute_drills(rsrcs_path, tags)
            print(" ")