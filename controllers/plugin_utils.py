#!/usr/bin/env python

'''
File: plugin_utils.py
Author: Ian W. Scott
Description: A collection of utility functions and classes for working on
web2py projects (controllers file).
'''

if 0:
    from gluon import current, BEAUTIFY
    from gluon.sqlhtml import SQLFORM
    from gluon.validators import IS_IN_SET
    from gluon.dal import Field
    request = current.request
    auth = current.auth
from plugin_utils import flatten, makeutf8
#from pprint import pprint
import re


