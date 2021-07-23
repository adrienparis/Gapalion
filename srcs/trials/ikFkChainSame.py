#!/usr/bin/env python
# -- coding: utf-8 --


__author__      = "Adrien PARIS"
__email__       = "a.paris.cs@gmail.com"

from os import error
import maya.cmds as cmds

title = u"Vérification du décalage entre les chaînes IK et FK"
image = "joinSym"
explanation = ""

def test():
    errors = []
    passed = True
    for ik in cmds.ls(type="joint"):
        if not ik.startswith("ik_"):
            continue
        sk = ik.replace("ik_", "sk_")
        if not cmds.objExists(sk):
            continue
        skMatrice = cmds.xform(sk ,q=1,ws=1,rp=1)
        ikMatrice = cmds.xform(ik ,q=1,ws=1,rp=1)
        error = False
        for i, s in zip(skMatrice, ikMatrice):
            if abs(s - i) >= 0.00001:
                error = True
        if error:
            passed = False
            errors.append(ik + "" + str(ikMatrice))
            errors.append(sk + "" + str(skMatrice))
            errors.append("")
    return passed, errors