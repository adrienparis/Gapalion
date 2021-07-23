#!/usr/bin/env python
# -- coding: utf-8 --


__author__      = "Adrien PARIS"
__email__       = "a.paris.cs@gmail.com"

import maya.cmds as cmds

title = u"Vérification de la visibilite de l'attribut [visibilitty] des controlleurs"
image = "eye"
explanation = ""

def test():
    passed = True
    errors = []
    unhides = []
    unlocks = []
    both = []
    for s in cmds.ls(type="transform"):
        if s.startswith("c_"):
            if cmds.getAttr(s + ".v", k=True) or not cmds.getAttr(s + ".v", l=True):
                passed = False
            if cmds.getAttr(s + ".v", k=True) and not cmds.getAttr(s + ".v", l=True):
                both.append(s)
            elif cmds.getAttr(s + ".v", k=True):
                unhides.append(s)
            elif not cmds.getAttr(s + ".v", l=True):
                unlocks.append(s)
    if len(both) != 0:
        errors.append("The folowing controller has theire visibility attribute unhided and unlocked :")
        for v in both:
            errors.append("\t" + v)
    if len(unhides) != 0:
        errors.append("The folowing controller has theire visibility attribute unhided :")
        for v in unhides:
            errors.append("\t" + v)
    if len(unlocks) != 0:
        errors.append("The folowing controller has theire visibility attribute unlocked :")
        for v in unlocks:
            errors.append("\t" + v)
    return passed, errors