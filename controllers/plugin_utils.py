#!/usr/bin/env python

'''
File: plugin_utils.py
Author: Ian W. Scott
Description: A collection of utility functions and classes for working on
web2py projects (controllers file).
'''

from gluon import request
from modules.plugin_utils import util_interface


def util():
    """
    Controller function for input/output access to utility functions.
    """
    return {}


def action():
    funcname = request.args[0] if request.args else 'default'

    form, output = util_interface(funcname)

    return {'form': form, 'output': output}
