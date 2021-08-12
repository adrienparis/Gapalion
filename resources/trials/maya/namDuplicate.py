#!/bin/env mayapy
# -- coding: utf-8 --

u"""Listes les nodes qui ont des noms non-unique
les | représente l'arborescence des groupe dans lequel
le node/transform est rangé"""

__author__      = "Adrien PARIS"
__email__       = "a.paris.cs@gmail.com"

import maya.cmds as cmds

title = u"Vérification des doublons"
image = "doubleN"



passed = True
errors = []
def test():
    passed = True
    errors = []
    dupName = {}
    for c in cmds.ls():
        if "|" in c:
            passed = False
            name = c.split("|")[-1]
            if c.split("|")[-1] in dupName:
                dupName[name].append(c)
            else:
                dupName[name] = [c]
    for k, v in dupName.iteritems():
        errors.append(k)
        for n in v:
            errors.append(" " * 4 + n)
        errors.append("")

    return passed, errors