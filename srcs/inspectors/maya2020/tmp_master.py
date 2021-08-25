# -- coding: utf-8 --

import subprocess
from subprocess import Popen
import sys

import shlex

sys.path.append(r"D:\creative seed\script\Gapalion\srcs") if r"D:\creative seed\script\Gapalion\srcs" not in sys.path else None

from comon import config

resources_path = config.read("resources_path")

def list_exercices(soft):
    soft_cmd = shlex.split(config.read(soft + "_cmd"), )
    with open("./jargon_tmp", "w") as jargon:
        
        original = sys.stdout
        sys.stdout = jargon
        p = Popen(soft_cmd + [resources_path, "ls"],
                stdout=subprocess.PIPE)
        sys.stdout = original 
    stdout, stderr = p.communicate()
    out = stdout.decode()
    exos = []
    for l in out.splitlines():
        exos.append(eval(l))
    return exos

def execute_exercices(soft):
    soft_cmd = shlex.split(config.read(soft + "_cmd"), )

    with open("./jargon_tmp", "w") as jargon:

        original = sys.stdout
        sys.stdout = jargon
        p = Popen(soft_cmd + [resources_path] + 
                  ["fichier maya", "#asset*#rig*#cs-#assets-rotateOrder",
                   "autre fichier maya", "#rig * #cs + cleanNamespace",
                   "error", "#rig  #cs + cleanNamespace",
                   "all", "#all",
                   "autre fichier maya quadru", "(#rig/#humanoid)*#cs",
                   "autre fichier maya quadru", "(#rig-#humanoid)*#cs",
                  ], #Action to interact with
                cwd="./srcs/inspectors/maya2020",
                stdout=subprocess.PIPE)
        sys.stdout = original 
    stdout, stderr = p.communicate()
    out = stdout.decode()
    exos = []
    for l in out.splitlines():
        print(l)
    return "Done!"

# print(list_exercices("maya2020"))
print(execute_exercices("maya2020"))