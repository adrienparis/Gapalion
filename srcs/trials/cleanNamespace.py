#!/usr/bin/env python
# -- coding: utf-8 --

u"""liste les namespace en trop"""

__author__      = "Adrien PARIS"
__email__       = "a.paris.cs@gmail.com"

import maya.cmds as cmds

title = u"Vérification de la proprete des namespaces"
image = ""

def test():
    passed = False
    errors = []
    namespaces = cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)
    namespaces.remove("UI")
    namespaces.remove("shared")
    if len(namespaces):
        errors = namespaces
        passed = False
    else:
        passed = True
    return passed, errors