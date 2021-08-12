#!/bin/env mayapy
# -- coding: utf-8 --

__author__      = "Adrien PARIS"
__email__       = "a.paris.cs@gmail.com"

import maya.cmds as cmds

title = u"Vérification des drive and key des follows"
image = ""

def test():
    errors = []
    passed = True
    for s in cmds.ls(type="animCurveUU"):
        name = s.split("_")
        lenght = cmds.keyframe(s, q=True, kc=True)
        keys = []
        for i in range(0, lenght):
            keys += cmds.keyframe(s, q=True, ev=True, index=(i,i))
        if "reverseroot" in name and not "tgt" in name:
            if len(keys) < 2:
                errors.append(s + " has not enough keys")
                passed = False
                continue
            if len(keys) > 2:
                errors.append(s + " has too many keys")
                passed = False
                continue
        else:
            if len(keys) != 2:
                continue
        if "reverseroot" in name:
            if not (keys[0] == 0 and keys[1] == 1):
                errors.append(s + "has not its reversroot keys right")
                passed = False
        elif "tgt" in name:
            if not (keys[0] == 1 and keys[1] == 0):
                errors.append(s + "has not its tgt keys right")
                passed = False
        else :
            if (keys[0] != 1 and keys[0] != 0 and keys[0] != 0.001) or (keys[1] != 1 and keys[1] != 0 and keys[0] != 0.001) :
                errors.append(s + " has not a name that suits for follows, so it can't say if it's ok, but it has weird values {} {}".format(keys[0], keys[1]))
    return passed, errors