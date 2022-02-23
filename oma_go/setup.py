#!/usr/bin/env python
from setuptools import setup


setup(
   name='oma_go',
   version='0.1dev',
   license='Creative Commons Attribution-Noncommercial-Share Alike license',
   description='oma_go.py retrives GO IDs from OMA Browser',
   long_description=open('README.md').read(),
   author='Daniel',
   author_email='d.zendler@gmx.com',
   packages=['oma_go'],  #same as name
   install_requires=['pandas', 'omadb'], 
)