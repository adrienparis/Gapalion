#!/bin/env mayapy
# -- coding: utf-8 --

u"""Écrire ici une expliaction du test"""

__author__      = "prenom NOM"
__email__       = "p.nom.cs@gmail.com"

import maya.cmds as cmds

title = u"Nom du test"
image = u"questionMark"

def test():
    # Change this value to false if the test fails
    passed = True

    # This should be an array of strings
    # the message you want to send
    msg = []

    #################
    # DO SOME TESTS #
    #################

    return passed, msg

if __name__ == "__main__":
    p, m = test()
    if p:
        print("##########")
        print("# PASSED #")
        print("##########")
    else:
        print("##########")
        print("# FAILED #")
        print("##########")
    for l in m:
        print(l)
