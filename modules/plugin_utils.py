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
    islist      :Ensure that an object is a list if it was not one already.
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

    backup_db       :Provided by plugin_backup
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


from gluon import SPAN, current, BEAUTIFY, SQLFORM, Field, IS_IN_SET, A
from plugin_backup import backup_db
import os
import re
import json
import traceback
import datetime
import csv
#from pprint import pprint
#auth = current.auth
#request = current.request


def util_interface(funcname):
    """
    Interface function for accessing util logic via the plugin_utils/util view.

    The one required argument 'funcname' should be a string containing the name
    of a function in this module.
    """
    print 'util_interface'
    funcs = {'gather_from_field': gather_from_field,
             'bulk_update': bulk_update,
             'migrate_field': migrate_field,
             'migrate_table': migrate_table,
             'import_from_csv': import_from_csv,
             'make_rows_from_field': make_rows_from_field,
             'make_rows_from_filenames': make_rows_from_filenames,
             'replace_in_field': replace_in_field,
             'do_backup': do_backup}

    form, output = funcs[funcname]()

    return form, output


def do_backup():
    """
    Return a form that triggers a backup of the sqlite database with a message.
    """
    message = 'Click to perform backup.'
    form = A(Field('leave_empty', 'text'),
             Submit='Backup sqlite database now')
    if form.process().accepted:
        if form.vars.leave_empty == '':
            message = backup_db()
            if not message:
                message = 'Sorry, the backup failed.'
    elif form.errors:
        message = BEAUTIFY(form.errors)

    return form, message

def islist(obj):
    """
    Return the supplied object converted to a list if it is not one already.
    """
    if not isinstance(obj, list):
        obj = [obj]
    return obj


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


def makeutf8(rawstring):
    """Return the string decoded as utf8 if it wasn't already."""
    try:
        rawstring = rawstring.decode('utf8')
    except (UnicodeEncodeError, UnicodeDecodeError):  # if already decoded
        rawstring = rawstring
    except (AttributeError, TypeError):  # if rawstring is NoneType
        rawstring = 'None'
    return rawstring


def printutf(string):
    """Convert unicode string to readable characters for printing."""
    string = makeutf8(string)
    return string


def capitalize(letter):
    """
    Convert string to upper case in utf-8 safe way.
    """
    letter = makeutf8(letter)
    newletter = letter.upper()
    return newletter


def capitalize_first(mystring):
    """
    Return the supplied string with its first letter capitalized.
    """
    first, rest = firstletter(mystring)
    first = capitalize(first)
    newstring = first + makeutf8(rest)
    return newstring


def lowercase(letter):
    """
    Convert string to lower case in utf-8 safe way.
    """
    letter = makeutf8(letter)
    newletter = letter.lower()
    return newletter


def firstletter(mystring):
    """
    Find the first letter of a byte-encoded unicode string.
    """
    mystring = makeutf8(mystring)
    let, tail = mystring[:1], mystring[1:]
    #print 'in firstletter: ', mystring[:1], '||', mystring[1:]
    #let, tail = let.encode('utf8'), tail.encode('utf8')
    return let, tail


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


def load_json(data):
    """
    Return a dictionary representing the supplied json string "data".
    """
    myjson = json.loads(data)
    return myjson


def gather_from_field(tablename, fieldname, regex_str, exclude,
                      filter_func=None, unique=True):
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
    form = SQLFORM.factory(Field('target_field'),
                           Field('target_table'),
                           Field('filter_func'),
                           Field('trans_func'),
                           Field('write_table'),
                           Field('write_field'),
                           Field('unique', 'boolean', default=True),
                           Field('testing', 'boolean', default=True))

    if form.process().accepted:
        vv = form.vars
        filter_func = eval(vv.filter_func) if vv.filter_func else None
        trans_func = eval(vv.trans_func) if vv.trans_func else None

        items = []
        rows = db(db[vv.target_table].id > 0).select()
        for r in rows:
            items.append(r['target_field'])

        if filter_func:
            items = filter(filter_func, items)
        if trans_func:
            items = [trans_func(i) for i in items]
        if vv.unique:
            items = list(set(items))
        items = [i for i in items if not i in exclude]

    elif form.errors:
        items = BEAUTIFY(form.errors)

    return form, items


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
    response = current.response
    db = current.db
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
        myrecs = BEAUTIFY(form.errors)
        response.flash = 'form has errors'

    return form, myrecs


def migrate_field():
    """
    """
    db = current.db
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


def migrate_table():
    db = current.db
    items = db(db.pages.id > 0).select()
    c = 0
    for i in items:
        db.journal_pages.insert(**{'journal_page': i.page})
        c += 1

    return dict(records_moved=c)


def migrate_back():
    db = current.db
    items = db(db.images_migrate.id > 0).select()
    c = 0
    for i in items:
        c += 1
        db.images[i.id] = i.as_dict()

    return dict(records_updated=c)


def import_from_csv():
    db = current.db
    try:
        db.paragraphs.truncate()
    except:
        print traceback.format_exc(5)
    mydir = '/home/ian/Dropbox/Downloads/Webdev/woh_export'
    files = ['node-export(43-nodes).1335558252.csv',
             'node-export(50-nodes).1335557844.csv',
             'node-export(50-nodes).1335557890.csv',
             'node-export(50-nodes).1335557934.csv',
             'node-export(50-nodes).1335558015.csv',
             'node-export(50-nodes).1335558056.csv',
             'node-export(50-nodes).1335558115.csv',
             'node-export(50-nodes).1335558151.csv',
             'node-export(50-nodes).1335558186.csv'
             ]
    #'node-export[](1-nodes).1335557290.export',
    fullfiles = [os.path.join(mydir, f) for f in files]

    for ff in fullfiles:
        with open(ff, 'rU') as csfile:
            rows = csv.DictReader(csfile)
            for row in rows:
                #pprint(row)
                titlebits = row['title'].split('.') if row['title'] else [None, None, None]
                taxes = [v for k, v in row.iteritems()
                         if re.match(r'.*taxonomy.*', k)
                         and v not in ['NULL', '', 0, 'None', None]]
                topics = '|'.join(taxes) if taxes else None
                pullquote = row['field_pullquote[\'0\'][\'value\']'] \
                    if 'field_pullquote[\'0\'][\'value\']' in row.values() \
                    else None
                audio = row['field_audiolink[\'0\'][\'value\']'] \
                    if 'field_audiolink[\'0\'][\'value\']' in row.values() \
                    else None
                image_id = row['field_images[\'0\'][\'fid\']'] \
                    if 'field_images[\'0\'][\'fid\']' in row.values() \
                    else None
                image_alt = row['field_images[\'0\'][\'data\'][\'alt\']'] \
                    if 'field_images[\'0\'][\'data\'][\'alt\']' \
                    in row.values() else None
                image_title = row['field_images[\'0\'][\'data\'][\'title\']'] \
                    if 'field_images[\'0\'][\'data\'][\'title\']' \
                    in row.values() else None
                image_filename = row['field_images[\'0\'][\'filename\']'] \
                    if 'field_images[\'0\'][\'filename\']' in row.values() \
                    else None
                times = {}
                for k in ['changed', 'created']:
                    errors = 0
                    try:
                        times[k] = datetime.datetime.fromtimestamp(int(row[k]))
                    except (TypeError, ValueError):
                        times[k] = datetime.datetime.utcnow()
                        errors += 1
                    print '{} errors: {}'.format(k, errors)

                matches = {'uid': row['uid'],
                           'chapter': titlebits[0],
                           'section': titlebits[1] if len(titlebits) > 1 else 0,
                           'subsection': titlebits[2] if len(titlebits) > 1 else 0,
                           'display_title': row['field_displaytitle[\'0\'][\'value\']'],
                           'status': row['status'],
                           'changed': times['changed'],
                           'created': times['created'],
                           'body': row['body'],
                           'pullquote': pullquote,
                           'audio': audio,
                           'image_id': image_id,
                           'image_alt': image_alt,
                           'image_title': image_title,
                           'image_filename': image_filename,
                           'topics': topics}
                matches = {k: v for k, v in matches.iteritems() if not v in [None, 'NULL']}
                num = db.paragraphs.insert(**matches)
                print num


def make_rows_from_field():
    """
    Use values from one table to create new records in another.

    The strings provided for

    The values for source_fields, target_fields, filter_funcs, and
    transform_funcs will be aligned by index.
    """
    db = current.db
    out = []
    form = SQLFORM.factory(Field('target_table'),
                           Field('source_table'),
                           Field('source_fields', 'list:string'),
                           Field('target_fields', 'list:string'),
                           Field('filter_funcs', 'list:string'),
                           Field('trans_funcs', 'list:string'),
                           Field('unique', 'boolean', default=True),
                           Field('testing', 'boolean', default=True))

    if form.process().accepted:
        vv = form.vars
        sourcerows = db(db[vv.target_table].id > 0).select()
        out = []
        for srow in sourcerows:
            trow = []
            for idx, f in enumerate(vv.source_fields):
                tval = vv.trans_funcs[idx](srow[f]) \
                    if len(vv.trans_funcs) > idx else srow[f]
                if len(vv.filter_funcs) > idx:
                    if not vv.filter_funcs[idx](tval):
                        tval = None
                if tval:
                    trow[vv.target_fields[idx]] = tval
            out.append(trow)

        if vv.unique:
            out = list(set(out))
        if not vv.testing:
            db[vv.target_table].bulk_insert(out)

    elif form.errors:
        out = BEAUTIFY(form.errors)

    return form, out


def make_rows_from_filenames():
    """
    TODO: unfinished
    """
    db = current.db
    out = []
    form = SQLFORM.factory(Field('folder_path'),
                           Field('target_field'),
                           Field('target_table'),
                           Field('filter_func'),
                           Field('extra_fields', 'list:string'),
                           Field('unique', 'boolean', default=True),
                           Field('testing', 'boolean', default=True))

    if form.process().accepted:
        vv = form.vars
        mypath = vv.folder_path
        fullpath = os.path.join()
        dirpath, dirnames, filenames = os.walk(mypath).next()
        xfield, xfunc = tuple([(x[0].strip(), x[1].strip()) for x in vv.extra_fields.split(',')])
        if xfunc:
            xfunc = eval(xfunc)
        filter_func = eval(vv.filter_func)

        out = []
        for f in filenames:
            kwargs = {}
            kwargs[vv.target_field] = f
            if xfunc:
                kwargs[xfield] = xfunc(f)
            if filter_func and not filter_func(f):
                kwargs = None
            if kwargs:
                out.append(kwargs)

        if not vv.testing:
            db[vv.target_table].bulk_insert(out)

    elif form.errors:
        out = BEAUTIFY(form.errors)

    return form, out


def replace_in_field():
    """
    Make a systematic set of string replacements for all values of one
    db field.
    """

    db = current.db
    form = SQLFORM.factory(Field('target_field'),
                           Field('target_table'),
                           Field('filter_func'),
                           Field('replacement_pairs', 'list:string'),
                           Field('testing', 'boolean', default=True))

    if form.process().accepted:
        vv = form.vars
        reps = vv.replacement_pairs
        myreps = []
        for r in reps:
            pieces = r.split(',')
            myset = (pieces[0].strip(), pieces[1].strip())
            myreps.append(myset)

        myrows = db(db[vv.target_table].id > 0).select()
        count = 0
        pairs = {}
        for m in myrows:
            startval = m[vv.target_field]
            endval = multiple_replace(startval, myreps)
            if not vv.testing:
                m.update_record(**{vv.target_field: endval})
            pairs[startval] = endval
            count += 1

        out = {'records_updated': count,
               'pairs': pairs}

    elif form.errors:
        out = BEAUTIFY(form.errors)

    return form, out
