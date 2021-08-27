# -- coding: utf-8 --

import subprocess
from subprocess import Popen
import sys

import shlex

import config

resources_path = config.read("resources_path")

def interact(soft, *command):
    soft_cmd = shlex.split(config.read(soft + "_cmd"), )

    with open("./jargon_tmp", "w") as jargon:

        original = sys.stdout
        sys.stdout = jargon
        p = Popen(soft_cmd + [resources_path] + 
                  list(command), #Action to interact with
                cwd="./srcs/inspectors/maya2020",
                stdout=subprocess.PIPE)
        sys.stdout = original 
    stdout, stderr = p.communicate()
    exos = []
    for l in stdout.splitlines():
        try:
            exos.append(eval(l))
        except Exception as e:
            print(l)
            print("↑ Error ↑\n{}\n".format(e))
    return exos


#Example


files = ["fichier maya", "#asset*#rig*#cs-#asset-rotateOrder",
            "autre fichier maya", "#rig * #cs + cleanNamespace",
            "error", "#rig  #cs + cleanNamespace",
            "all", "#all",
            "autre fichier maya quadru", "(#rig/#humanoid)*#cs",
            "autre fichier maya quadru", "(#rig-#humanoid)*#cs",
            r"D:\creative seed\Atelier\année02.2\semestre02\sosuke\3_work\maya\scenes\assets\chars\sosuke\rig\cs_sosuke_rig.ma",
            "(#rig/#humanoid)*#cs"]


dct = interact("maya2020", "ls") 
for d in dct:
    if isinstance(d, dict):
        print(d["name"])
        print("\tTags : {}".format(d["tags"]))

dct = interact("maya2020", *files) 
for d in dct:
    if isinstance(d, dict):
        print(d["name"])
        print("\tfile : {}".format(d["file"]))
        print("\tDrill executed properly : {}".format(d["passed"]))
        print("\tStatus : {}".format(d["status"]))
        print("\tmessage : ")
        for m in d["message"]:
            print("\t\t{}".format(m))
    else:
        print(d)