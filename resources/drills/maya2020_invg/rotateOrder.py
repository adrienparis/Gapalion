#!/bin/env mayapy
# -- coding: utf-8 --
u"""Dans le cas très spécifoque des bipeds apris à creativeSeeds
Liste tout les transform qui n'ont pas leurs rotate order bien setter
"""

__author__      = "Adrien PARIS"
__email__       = "a.paris.cs@gmail.com"

import maya.cmds as cmds

title = u"Vérification des rotate Order pour biped classic"
image = ""
tags = "rig", "cs", "humanoid"

def main():
    errors = []
    status = "SUCCESS"
    elems = ["sk_wrist", "ik_wrist", "c_IK_wrist", "pose_IK_wrist", "inf_IK_wrist", "root_IK_wrist",
             "c_FK_wrist", "pose_FK_wrist", "inf_FK_wrist", "root_FK_wrist",
             "sk_wrist0", "sk_wristOri", "sk_foreArm", "reverseHand", "c_IK_hand", "c_FK_hand", "grp_fingers"]
    for e in elems:
        for s in ["L", "R"]:
            name = e + "_" + s
            if cmds.objExists(name):
                if cmds.getAttr(name + ".rotateOrder") != 3:
                    status = "ERROR"
                    errors.append(name)

    return status, errors

if __name__ == "__main__":
    p, m = main()
    if p:
        print("##########")
        print("# PASSED #")
        print("##########")
    else:
        print("##########")
        print("# FAILED #")
        print("##########")
    for l in m:
        print(l)
