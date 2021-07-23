#!/usr/bin/env python
# -- coding: utf-8 --


__author__      = "Adrien PARIS"
__email__       = "a.paris.cs@gmail.com"

import maya.cmds as cmds

title = u"Vérification de la symétrie des noms"
image = ""
explanation = u"""Regarde si un transform [LEFT] a bien son double en [RIGHT]
                   marque d'un X l'élément manquant
                   Si ce test ne passe pas, il y a de fortes chances que certain tests échoue
                   dû à une mauvaise nomination"""

def centerText(text, gap=30):
    l = len(text)
    sent = ""
    sent = " " * ((gap - l) / 2)
    sent += text
    sent = sent.ljust(gap)
    return sent

def test():
    errors = []
    passed = True
    errors.append(" " * 5 + centerText("Left") + centerText("Right"))
    errors.append("")
    names = cmds.ls()
    for n in names:
        oSide = n.replace("_L", "_R") if n.endswith("_L") else n.replace("_R", "_L") if n.endswith("_R") else None
        if oSide == None:
            continue
        if not oSide in names:
            passed = False
            sent = " " * 5
            sent += centerText(n) + centerText("X") if n.endswith("_L") else centerText("X") + centerText(n)
            errors.append(sent)
    if passed:
        errors = []

    return passed, errors
