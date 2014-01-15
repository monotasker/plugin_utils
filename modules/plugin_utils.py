#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
File: plugin_utils.py
Author: Ian W. Scott
Description: A collection of utility functions and classes for working on
web2py projects.

Many of these functions are meant to be called directly from elsewhere in an
app's business logic, providing helper functions for common tasks. They can
also, however, be accessed via the

This module file holds most of the business logic accessed through the
controller functions. It exposes one main interface through the
util_interface function. Through this function the following specific actions
can be called:

clr         :Surround a string with ansi color sequences for console output.
printutf    :Convert unicode (utf-8) string to readable characters for printing.
capitalize  :Capitalize a utf-8 string in a unicode-safe way.
lowercase   :Convert string to lower case in utf-8 safe way.
firstletter :Isolate the first letter of a byte-encoded unicode string.
test_regex  :Return a re.match object for each given string, tested with the
             given regex.
flatten     :Convert an arbitrarily deep nested list into a single flat list.
send_error  :Send an email reporting error and including debug info. """
make_json   :Return a json object representing the provided dictionary, with
             extra logic to handle datetime objects.


bulk_update     :Controller function to perform a programmatic update to a
                 field in one table.
migrate_field   :
migrate_table   :
migrate_back    :

When called via the plugin_utils/util controller, which accesses the
util_interface clearinghouse function, a form for input and a view of the
returned values is provided via the plugin_utils/util.html view.

These functions can also be called directly from other functions and classes.

'''

import re
from gluon import SPAN, current, BEAUTIFY, SQLFORM, Field, IS_IN_SET
import json
from paideia_utils import test_step_regex, gather_vocab
import paideia_path_factory
import traceback
#from pprint import pprint
auth = current.auth
request = current.request
response = current.response


def util_interface(funcname):
    """
    Interface function for accessing util logic via the plugin_utils/util view.

    The one required argument 'funcname' should be a string containing the name
    of a function in this module.
    """
    output = {}
    form = SQLFORM.factory(
    )
    if form.process

    return form, output


def clr(string, mycol='white'):
    """
    Return a string surrounded by ansi colour escape sequences.

    This function is intended to simplify colourizing terminal output.
    The default color is white. The function can take any number of positional
    arguments as component strings, which will be joined (space delimited)
    before being colorized.
    """
    col = {'white': '\033[95m',
           'blue': '\033[94m',
           'green': '\033[92m',
           'orange': '\033[93m',
           'red': '\033[91m',
           'lightblue': '\033[1;34m',
           'lightgreen': '\033[1;32m',
           'lightcyan': '\033[1;36m',
           'lightred': '\033[1;31m',
           'lightpurple': '\033[1;35m',
           'white': '\033[1;37m',
           'endc': '\033[0m'
           }
    thecol = col[mycol]
    endc = col['endc']
    if isinstance(string, list):
        try:
            string = ' '.join(string)
        except TypeError:
            string = ' '.join([str(s) for s in string])

    newstring = '{}{}{}'.format(thecol, string, endc)
    return newstring


def printutf(string):
    """Convert unicode string to readable characters for printing."""
    string = string.decode('utf-8').encode('utf-8')
    return string


def capitalize(letter):
    #if letter in caps.values():
    letter = letter.decode('utf-8').upper()
    print 'capitalized'
    print letter.encode('utf-8')
    return letter


def lowercase(string):
    """
    Convert string to lower case in utf-8 safe way.
    """
    string = string.decode('utf-8').lower()
    return string.encode('utf-8')


def firstletter(mystring):
    """
    Find the first letter of a byte-encoded unicode string.
    """
    print mystring
    print 'utf-8'
    mystring = mystring.decode('utf-8')
    print mystring
    let, tail = mystring[:1], mystring[1:]
    print 'in firstletter: ', mystring[:1], '||', mystring[1:]
    let, tail = let.encode('utf-8'), tail.encode('utf-8')
    return let, tail
    #else:
        #try:
            #if mystring[:3] in caps.values():
                #first_letter = mystring[:3]
            #else:
                #first_letter = mystring[:3]
                #tail = mystring[3:]
        #except KeyError:
            #try:
                #first_letter = mystring[:2]
                #tail = mystring[2:]
            #except KeyError:
                #first_letter = mystring[:2]
                #tail = mystring[2:]
    #return first_letter, tail


def test_regex(regex, readables):
    """
    Return a re.match object for each given string, tested with the given regex.

    The "readables" argument should be a list of strings to be tested.
    """
    readables = readables if type(readables) == list else [readables]
    test_regex = re.compile(regex, re.I | re.U)
    rdict = {}
    for rsp in readables:
        match = re.match(test_regex, rsp)
        rdict[rsp] = SPAN('PASSED', _class='success') if match \
            else SPAN('FAILED', _class='success')
    return rdict


def flatten(self, items, seqtypes=(list, tuple)):
    """
    Convert an arbitrarily deep nested list into a single flat list.
    """
    for i, x in enumerate(items):
        while isinstance(items[i], seqtypes):
            items[i:i + 1] = items[i]
    return items


def send_error(myclass, mymethod, myrequest):
    """ Send an email reporting error and including debug info. """
    mail = current.mail
    msg = '<html>A user encountered an error in {myclass}.{mymethod}' \
          'report failed.\n\nTraceback: {tb}' \
          'Request:\n{rq}\n' \
          '</html>'.format(myclass=myclass,
                           mymethod=mymethod,
                           tb=traceback.format_exc(5),
                           rq=myrequest)
    title = 'Paideia error'
    mail.send(mail.settings.sender, title, msg)


def make_json(data):
    """
    Return json object representing the data provided in dictionary "data".
    """
    date_handler = lambda obj: obj.isoformat() \
        if isinstance(obj, datetime.datetime) else None
    myjson = json.dumps(data,
                        default=date_handler,
                        indent=4,
                        sort_keys=True)
    return myjson


def gather_from_field(tablename, fieldnames, regex_str, exclude,
                      filter_func=None unique=True):
    """
    Return a list of all strings satisfying the supplied regex.

    The fieldnames argument should be a list, so that multiple target fields
    can be searched at once.

    The optional 'unique' keyword argument determines whether duplicates will
    be removed from the list. (Defaults to True.)

    The optional 'filterfunc' keyword argument allows a function to be passed
    which which will be used to alter the gathered strings. This alteration will
    happen before duplicate values are removed. So, for example, the strings
    can be normalized for case or accent characters if those variations are
    not significant.
    """
    db = current.db
    rows = db(db[fieldname].id > 0).select()

    items = []
    for r in rows:
        regex = re.compile(u'{}'.format(regex_str))
        targets = ' '.join([r[field] for field in fieldnames])
        items.extend(regex.findall(targets))
    if filter_func:
        items = filter(filter_func, items)
    if unique:
        items = list(set(items))
    items = [i for i in items if not i in exclude]

    return items


def multiple_replacer(*key_values):
    """
    Returns a lambda function to perform replacements on a series of strings.

    This is a helper function for the multiple_replace() function. The
    key_values argument should be an n-length tuple of 2-item tuples, each of
    which represents one pair of old_value/replacement_value.
    """
    replace_dict = dict(key_values)
    replacement_function = lambda match: replace_dict[match.group(0)]
    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)
    return lambda string: pattern.sub(replacement_function, string)


def multiple_replace(string, *key_values):
    """
    Perform multiple string replacements simultaneously.

    Because the replacements are simultaneous the results of one replacement
    will not be seen in making other replacements. For example, if 're' is to
    be replaced by 'in' and 'nt' is to be replaced by 'ch' (('re', 'in'),
    ('int', 'ch')), the input string 'return' would become 'inturn' not 'churn'.

    The key_values argument should be an n-length tuple of 2-item tuples, each
    of which represents one pair of old_value/replacement_value.

    """
    return multiple_replacer(*key_values)(string)


def bulk_update():
    """
    Controller function to perform a programmatic update to a field in one table.
    """
    myrecs = None
    form = SQLFORM.factory(
        Field('table', requires=IS_IN_SET(db.tables)),
        Field('field'),
        Field('query'),
        Field('new_value'))
    if form.process().accepted:
        query = eval(form.vars.query)
        try:
            recs = db(query)
            recs.update(**{form.vars.field: form.vars.new_value})
            myrecs = recs.select()
            response.flash = 'update succeeded'
        except Exception:
            print traceback.format_exc(5)
    elif form.errors:
        response.flash = 'form has errors'

    return dict(form=form, recs=myrecs)


def migrate_field():
    fields = {'plugin_slider_slides': ('content', 'slide_content')}

    for t, f in fields.iteritems():
        table = t
        source_field = f[0]
        target_field = f[1]
        items = db(db[table].id > 0).select()
        c = 0
        for i in items:
            values = {target_field: i[source_field]}
            i.update_record(**values)
            c += 1

    return {'records_copied': c}


def to_migrate_table():
    items = db(db.pages.id > 0).select()
    c = 0
    for i in items:
        db.journal_pages.insert(**{'journal_page': i.page})
        c += 1

    return dict(records_moved=c)


def migrate_back():
    items = db(db.images_migrate.id > 0).select()
    c = 0
    for i in items:
        c += 1
        db.images[i.id] = i.as_dict()

    return dict(records_updated=c)
