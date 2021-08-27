#!/bin/env mayapy
# -- coding: utf-8 --
u"""Sur une propal de Yann GENTY le boss ♥
l'ordre des deformer doit être cluster, puis skinCluster, pour finir sur les blendShape
Si vous mettez des lattices, le test peut se perdre, et donc une vérification manuelle est nécessaire"""


__author__      = "Adrien PARIS"
__email__       = "a.paris.cs@gmail.com"

import maya.cmds as cmds

title = u"Vérification de l'ordre des deformer"
image = ""
tags = "asset", "rig", "cs"

def matchnmatch(a, b):
    if len(a) == 0:
        return False
    if len(b) == 0:
        return True
    if a[0] == b[0]:
        return matchnmatch(a, b[1:])
    if a[0] != b[0]:
        return matchnmatch(a[1:], b)

def main():
    temp = ["cluster", "skinCluster", "blendShape"]
    # temp = ["cluster", "skinCluster", "tweak", "blendShape"]
    status = "SUCCESS"

    msg = ["the order should be : ".ljust(30) + "-> " + str(temp), ""]

    for s in cmds.ls(type="transform"):
        cnt = cmds.listHistory(s)
        if cnt is None:
            continue
        cnt = [cmds.nodeType(x) for x in cnt]
        cnt = [x for x in cnt if x in temp]
        v = matchnmatch(temp, cnt)
        if not v:
            status = "ERROR"
            msg.append(s.ljust(30) + "-> " + str(cnt))
    if status == "SUCCESS":
        msg = []

    return status, msg