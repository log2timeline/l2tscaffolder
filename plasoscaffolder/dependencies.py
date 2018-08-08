# -*- coding: utf-8 -*-
# fyi: those methods are copied from plaso
"""Functionality to check for the availability and version of dependencies."""

from __future__ import print_function

# Dictionary that contains version tuples per module name.
#
# A version tuple consists of:
# (version_attribute_name, minimum_version, maximum_version, is_required)
#
# Where version_attribute_name is either a name of an attribute,
# property or method.
PYTHON_DEPENDENCIES = {
    u'click': (u'__version__', u'6.7', u'6.7', True),
    u'setuptools': (u'__version__', u'34.4.1', u'34.4.1', True),
    u'Jinja2': (u'__version__', u'2.9.6', u'2.9.6', True),
    u'colorama': (u'__version__', u'0.3.7', u'0.3.7', True),
    u'yapf': (u'__version__', u'0.16.1', u'0.16.1', True), }

PYTHON_TEST_DEPENDENCIES = {}

# Maps Python module names to DPKG packages.
_DPKG_PACKAGE_NAMES = {
    u'click': u'python-click',
    u'setuptools': u'python-setuptools',
    u'Jinja2': u'python-jinja2',
    u'colorama': u'python-colorama',
    u'yapf': u'yapf3'}

# Maps Python module names to PyPI projects.
_PYPI_PROJECT_NAMES = {
    u'click': u'click',
    u'setuptools': u'setuptools ',
    u'Jinja2': u'Jinja2',
    u'colorama': u'colorama',
    u'yapf': u'yapf'}

# Maps Python module names to RPM packages.
_RPM_PACKAGE_NAMES = {
    u'click': u'python-click',
    u'setuptools': u'python-setuptools',
    u'Jinja2': u'python-Jinja2',
    u'colorama': u'python-colorama',
    u'yapf': u'yapf'}
