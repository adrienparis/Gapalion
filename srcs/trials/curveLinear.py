#!/bin/env mayapy
# -- coding: utf-8 --

"""curveLinear.py: Check if the curves are set to linear."""

__author__      = "Adrien PARIS"
__email__       = "a.paris.cs@gmail.com"

import maya.cmds as cmds

title = u"Vérification de la linéarite des courbe d'animation"
image = "curveLinear"
explanation = ""

def test():
    passed = True
    errors = []
    for s in cmds.ls(type="animCurve"):
    #    log(s)
        lenght = cmds.keyframe(s, q=True, kc=True)
        values = []
        tangents = []
        times = []
        for i in range(0, lenght):
            values += cmds.keyframe(s, q=True, ev=True, index=(i,i))
            tangents += cmds.keyTangent(s, q=True, itt=True, index=(i,i))
            tangents += cmds.keyTangent(s, q=True, ott=True, index=(i,i))
        if len(tangents) == 0:
            passed = False
            errors.append(str(s) + " is an anim curve, but has no key")
            continue
        if not (tangents.count(tangents[0]) == len(tangents) and tangents[0] == "linear"):
            passed = False
            errors.append(str(s) + " " + str(tangents))
    return passed, errors

