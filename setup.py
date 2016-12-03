#!/usr/bin/env python
"""
setup.py
This is the setup file for the SimISR python package

@author: John Swoboda
"""
import os,subprocess
from setuptools import setup

try:
    subprocess.call(['conda','install','--yes','--file','requirements.txt'])
except Exception as e:
    pass


config = {
    'description': 'An ISR data simulator',
    'author': 'John Swoboda',
    'url': 'https://github.com/jswoboda/SimISR.git',
    'version': '1',
    'install_requires': ['ISRSpectrum','lmfit'],
    'dependency_links': ['https://github.com/jswoboda/ISRSpectrum/tarball/master#egg=ISRSpectrum'],
    'packages': ['SimISR','beamtools','radarsystools'],
    'name': 'SimISR'
}

curpath = os.path.dirname(__file__)
testpath = os.path.join(curpath,'Testdata')
try:
    os.mkdir(testpath)
except OSError:
    pass
print("created {}".format(testpath))

setup(**config)
