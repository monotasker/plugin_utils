#!/usr/bin/env python

'''
File: plugin_utils.py
Author: Ian W. Scott
Description: A collection of utility functions and classes for working on
web2py projects (controllers file).
'''

if 0:
    from gluon import current
    request = current.request
from plugin_utils import util_interface


def util():
    """
    Controller function to present utility interface view.
    """
    return {}


def action():
    """
    Controller function for input/output access to utility functions.
    """
    print 'hi', request.args
    funcname = request.args[0]
    print funcname

    form, output = util_interface(funcname)

    return {'form': form, 'output': output}
