#!/bin/env mayapy
# -- coding: utf-8 --
u"""Ce test vérifie que le transform [LEFT] a bien le même rotateOrder que le transform [RIGHT]
Les [does not exist] indique un problème dans la nomenclature des noms et donc qu'il ne peut tester la symétrie des rotateOrders"""


__author__      = "Adrien PARIS"
__email__       = "a.paris.cs@gmail.com"

import maya.cmds as cmds

title = u"Vérification de la symétrie des rotates orders"
image = ""
tags = "rig", "cs", "symetric"

def main():
    status = "SUCCESS"
    errors = []
    for s in cmds.ls(type="transform"):
        if s[-2:] == "_L":
            r = s[:-2] + "_R"
            if not cmds.objExists(r):
                errors.append("does not exists : " + r)
                continue
            if cmds.getAttr(s + ".rotateOrder") != cmds.getAttr(r + ".rotateOrder"):
                status = "ERROR"
                errors.append("not symetric : {0: <20} -> \t \t {1: <24}".format(s, r))
        if s[-2:] == "_R":
            r = s[:-2] + "_L"
            if not cmds.objExists(r):
                status = "WARNING"
                errors.append("does not exists : " + r)
                continue
    return status, errors