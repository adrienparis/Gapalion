#!/bin/env mayapy
# -- coding: utf-8 --

u"""Écrire ici une expliaction du test"""

__author__      = "prenom NOM"
__email__       = "p.nom.cs@gmail.com"

import maya.cmds as cmds

title = u"Nom du test"
image = u"questionMark"

def main():
    # Set this value to SUCCESS if it pass
    #                   ERROR if it failed
    #                   WARNING if it doesn't pass because of an imprecision
    passed = "SUCCESS"

    # This should be an array of strings
    # the message you want to send
    msg = []

    #################
    # DO SOME TESTS #
    #################

    return status, msg

if __name__ == "__main__":
    p, m = main()
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
