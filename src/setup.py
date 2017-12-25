#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This is the setup file for the project."""
from setuptools import find_packages
from setuptools import setup

setup(name='plasoscaffolder',
      version='0.1',
      packages=find_packages(),
      include_package_data=True,
      package_data={'plasoscaffolder.bll.templates': ['*.jinja2'],'':['.style.yapf']},
      install_requires=['Click>=6.7',
                        'setuptools>=35.0.2',
                        'jinja2>=2.9.6',
                        'colorama>=0.3.7',
                        'yapf==0.16.1',
                        'pexpect>=4.2.1'],
      entry_points={'console_scripts': [
          'plasoscaffolder=plasoscaffolder.frontend.main:entry_point']},
      
    # metadata for upload to PyPI
    author="Claudia Saxer",
    description="This is a scaffolder for sqlite plugins for plaso.",
    keywords="plaso scaffolder",
    url="http://plasoscaffolder.readthedocs.io")
