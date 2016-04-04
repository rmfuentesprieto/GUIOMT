#!/bin/bash

# never forget to change the current path 
# in the main.py appending it to sys.path

sudo add-apt-repository ppa:kivy-team/kivy
sudo apt-get update

sudo apt-get --yes install python-setuptools
sudo apt-get --yes install python-dev
sudo apt-get --yes install python-kivy
sudo apt-get --yes install python-numpy
sudo apt-get --yes install libffi-dev
sudo apt-get --yes install libhdf5-dev
sudo apt-get --yes install python-gnuplot

sudo pip install katcp
sudo pip install corr
sudo pip install aipy
sudo pip install ephem
sudo pip install gnuplotlib
