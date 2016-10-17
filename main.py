#!/usr/bin/env python
"""
This is the main of the controller to test de digital OMT.
This is a develop made by Amermelao.

Install:


    sudo add-apt-repository ppa:kivy-team/kivy
    sudo apt-get update
    sudo apt-get install python-kivy

"""
import os, sys
sys.path.append(os.path.dirname(__file__))

from omt.gui.init import GUIStart

if __name__ == "__main__":
    GUIStart().run()
