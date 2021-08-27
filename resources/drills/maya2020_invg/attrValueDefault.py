#!/bin/env mayapy
# -- coding: utf-8 --

u"""vérifie que les transform des controleur on bien leur valeurs par défaut
tx ty tz indiquent que le controlleur a des valeur sur ses translate
rx ry rz indiquent que le controlleur a des valeur sur ses rotate
sx sy sz indiquent que le controlleur a des valeur autre que 1 sur ses scale"""

__author__      = "Adrien PARIS"
__email__       = "a.paris.cs@gmail.com"

import maya.cmds as cmds

title = u"Vérification des valeurs par default des controleurs"
image = ""
tags = "asset", "rig", "cs"

def getDefaultAttr(c):
    array = []
    array.append(cmds.getAttr(c + ".tx"))
    array.append(cmds.getAttr(c + ".ty"))
    array.append(cmds.getAttr(c + ".tz"))
    array.append(cmds.getAttr(c + ".rx"))
    array.append(cmds.getAttr(c + ".ry"))
    array.append(cmds.getAttr(c + ".rz"))
    array.append(cmds.getAttr(c + ".sx"))
    array.append(cmds.getAttr(c + ".sy"))
    array.append(cmds.getAttr(c + ".sz"))
    return array

def main():
    passed = True
    status = ""
    errors = []
    transform = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    defaultValues = [0, 0, 0, 0, 0, 0, 1, 1, 1]
    errors.append(u"with 0.001 tolérance:")
    for c in cmds.ls(type="transform"):
        if c.startswith("c_"):
            array = getDefaultAttr(c)
            if array != defaultValues:
                passed = False
                status = "ERROR"
                errorsSentence = [transform[i] for i in range(0, len(transform)) 
                                  if array[i] > defaultValues[i] + 0.001 or
                                  array[i] < defaultValues[i] - 0.001 ]
                if errorsSentence == []:
                    continue
                errorsSentence = ", ".join(errorsSentence)
                errors.append("\t" + c + " -> " + errorsSentence)
    errors.append("")
    errors.append("micro-value:")
    for c in cmds.ls(type="transform"):
        if c.startswith("c_"):
            array = getDefaultAttr(c)
            if array != defaultValues:
                passed = False
                status = "ERROR"
                errorsSentence = [transform[i] for i in range(0, len(transform))
                                  if array[i] <= defaultValues[i] + 0.001 and
                                  array[i] >= defaultValues[i] - 0.001 and
                                  array[i] != defaultValues[i]]
                if errorsSentence == []:
                    continue
                errorsSentence = ", ".join(errorsSentence)
                errors.append("\t" + c + " -> " + errorsSentence)
    if passed:
        status = "SUCCESS"
        errors = []
    return status, errors