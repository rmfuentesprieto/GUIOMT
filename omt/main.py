#!/usr/bin/env python
"""
This is the main of the controller to test de digital OMT.
This is a develop made by Amermelao.

Install:


    sudo add-apt-repository ppa:kivy-team/kivy
    sudo apt-get update
    sudo apt-get install python-kivy

"""
import sys
sys.path.append("/home/roma/Documentos/PyCharmWS/OMTGUI/")
from omt.gui.init import GUIStart

if __name__ == "__main__":
    GUIStart().run()
