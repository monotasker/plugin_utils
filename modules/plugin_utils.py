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


BulkUpdate     :Controller function to perform a programmatic update to a
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
from gluon import current, SQLFORM, Field, IS_IN_SET
import json
import traceback
import datetime
import os
import csv
from pprint import pprint
from ast import literal_eval
#auth = current.auth
request = current.request
response = current.response


##def util_interface(classname):
    ##"""
    ##Interface function for accessing util logic via the plugin_utils/util view.

    ##The one required argument 'funcname' should be a string containing the name
    ##of a function in this module.

    ##"""
    ##myclasses = {'GatherFromField': GatherFromField,
                 ##'BulkUpdate': BulkUpdate,
                 ##'RowsFromField': RowsFromField,
                 ##'RowsFromFilenames': RowsFromFilenames,
                 ##'ReplaceInField': ReplaceInField}

    ##form, output = myclasses[classname]().make_form()

    ##return form, output


#def islist(dat):
    #"""
    #Return the data, ensuring that it is a single-level list.
    #"""
    #newdat = [dat] if not isinstance(dat, list) else dat
    #return newdat


#def clr(string, mycol='white'):
    #"""
    #Return a string surrounded by ansi colour escape sequences.

    #This function is intended to simplify colourizing terminal output.
    #The default color is white. The function can take any number of positional
    #arguments as component strings, which will be joined (space delimited)
    #before being colorized.
    #"""
    #col = {'white': '\033[95m',
           #'blue': '\033[94m',
           #'green': '\033[92m',
           #'orange': '\033[93m',
           #'red': '\033[91m',
           #'lightblue': '\033[1;34m',
           #'lightgreen': '\033[1;32m',
           #'lightcyan': '\033[1;36m',
           #'lightred': '\033[1;31m',
           #'lightpurple': '\033[1;35m',
           #'white': '\033[1;37m',
           #'endc': '\033[0m'
           #}
    #thecol = col[mycol]
    #endc = col['endc']
    #if isinstance(string, list):
        #try:
            #string = ' '.join(string)
        #except TypeError:
            #string = ' '.join([str(s) for s in string])

    #newstring = '{}{}{}'.format(thecol, string, endc)
    #return newstring


#def printutf(string):
    #"""Convert unicode string to readable characters for printing."""
    #string = makeutf8(string)
    #return string


#def capitalize(letter):
    #"""
    #Convert string to upper case in utf-8 safe way.
    #"""
    #letter = makeutf8(letter)
    #newletter = letter.upper()
    #return newletter.encode('utf-8')


#def lowercase(letter):
    #"""
    #Convert string to lower case in utf-8 safe way.
    #"""
    #letter = makeutf8(letter)
    #newletter = letter.lower()
    #return newletter.encode('utf-8')


#def makeutf8(rawstring):
    #"""Return the string decoded as utf8 if it wasn't already."""
    #try:
        #rawstring = rawstring.decode('utf8')
    #except (UnicodeDecodeError, UnicodeEncodeError):
        #rawstring = rawstring
    #return rawstring


#def firstletter(mystring):
    #"""
    #Find the first letter of a byte-encoded unicode string.
    #"""
    #mystring = makeutf8(mystring)
    #let, tail = mystring[:1], mystring[1:]
    ##print 'in firstletter: ', mystring[:1], '||', mystring[1:]
    #let, tail = let.encode('utf8'), tail.encode('utf8')
    #return let, tail


#def capitalize_first(mystring):
    #"""
    #Return the supplied string with its first letter capitalized.
    #"""
    #first, rest = firstletter(mystring)
    #newstring = '{}{}'.format(capitalize(first), rest)
    #return newstring


#def test_regex(regex, readables):
    #"""
    #Return a re.match object for each given string, tested with the given regex.

    #The "readables" argument should be a list of strings to be tested.
    #"""
    #readables = readables if type(readables) == list else [readables]
    #print 'testing regex =================================='
    #print makeutf8(regex)
    #for r in readables:
        #print makeutf8(r)
    #test_regex = re.compile(regex, re.I | re.U | re.X)
    #mlist = [re.match(test_regex, rsp) for rsp in readables]
    #if all(mlist):
        #return True, []
    #else:
        #print 'some failures'
        #pprint(mlist)
        #return False, mlist


#def flatten(self, items, seqtypes=(list, tuple)):
    #"""
    #Convert an arbitrarily deep nested list into a single flat list.
    #"""
    #for i, x in enumerate(items):
        #while isinstance(items[i], seqtypes):
            #items[i:i + 1] = items[i]
    #return items


#def send_error(myclass, mymethod, myrequest):
    #""" Send an email reporting error and including debug info. """
    #mail = current.mail
    #msg = '<html>A user encountered an error in {myclass}.{mymethod}' \
          #'report failed.\n\nTraceback: {tb}' \
          #'Request:\n{rq}\n' \
          #'</html>'.format(myclass=myclass,
                           #mymethod=mymethod,
                           #tb=pprint(traceback.format_exc(5)),
                           #rq=pprint(myrequest))
    #appname = request.application
    #title = '{} error encountered'.format(capitalize_first(appname))
    #mail.send(mail.settings.sender, title, msg)


#def make_json(data):
    #"""
    #Return json object representing the data provided in dictionary "data".
    #"""
    #date_handler = lambda obj: obj.isoformat() \
        #if isinstance(obj, datetime.datetime) else None
    #myjson = json.dumps(data,
                        #default=date_handler,
                        #indent=4,
                        #sort_keys=True)
    #return myjson


##def multiple_replace(string, *key_values):
    ##"""
    ##Perform multiple string replacements simultaneously.

    ##Because the replacements are simultaneous the results of one replacement
    ##will not be seen in making other replacements. For example, if 're' is to
    ##be replaced by 'in' and 'nt' is to be replaced by 'ch' (('re', 'in'),
    ##('int', 'ch')), the input string 'return' would become 'inturn' not 'churn'.

    ##The key_values argument should be an n-length tuple of 2-item tuples, each
    ##of which represents one pair of old_value/replacement_value.

    ##"""
    ##def multiple_replacer(*key_values):
        ##"""
        ##Returns lambda function to perform the replacements.
        ##"""
        ##replace_dict = dict(key_values)
        ##replacement_function = lambda match: replace_dict[match.group(0)]
        ##pattern = re.compile("|".join([re.escape(k)
                                       ##for k, v in key_values]), re.M)
        ##return lambda string: pattern.sub(replacement_function, string)

    ##return multiple_replacer(*key_values)(string)


##class UtilForm(object):
    ##"""
    ##Abstract parent class for constructing util interfaces.

    ##Returns a tuple of two items: form and out.

    ##"""
    ##def make_form(self, fieldlist=[]):
        ##"""
        ##Return a tuple including a web2py form object and any processed output.

        ##field_list should be a list of Field objects.

        ##"""
        ##db = current.db
        ##out = None
        ##standard = [Field('source_table', requires=IS_IN_SET(db.tables)),
                    ##Field('source_fields', 'list:string'),
                    ##Field('filter_funcs', 'list:string'),
                    ##Field('trans_funcs', 'list:string'),
                    ##Field('unique', 'boolean', default=True),
                    ##Field('write', 'boolean', default=False)
                    ##]
        ##fieldlist = fieldlist.extend(standard)
        ##form = SQLFORM.factory(*fieldlist)
        ##if form.process().accepted:
            ##out = self.process_result(form.vars)
            ##out = list(set(out)) if form.vars.unique else out
            ##if form.vars.write:
                ##self.write_vals(out)
        ##elif form.errors:
            ##out = self.process_errors(form.errors)
        ##return form, out

    ##def write_vals(self, ttable, outvals):
        ##"""docstring for write_vals"""
        ##db = current.db
        ##return db[ttable].bulk_insert(outvals)

    ##def process_result(self, formvars):
        ##return formvars

    ##def process_errors(self, errors):
        ##return errors


##class GatherFromField(UtilForm):
    ##"""
    ##Return a list of all strings satisfying the supplied regex.

    ##The fieldnames argument should be a list, so that multiple target fields
    ##can be searched at once.

    ##The optional 'unique' keyword argument determines whether duplicates will
    ##be removed from the list. (Defaults to True.)

    ##The optional 'filterfunc' keyword argument allows a function to be passed
    ##which which will be used to alter the gathered strings. This alteration will
    ##happen before duplicate values are removed. So, for example, the strings
    ##can be normalized for case or accent characters if those variations are
    ##not significant.

    ##"""
    ##def make_form(self):
        ##"""
        ##"""
        ##fieldlist = [Field('target_field'),
                     ##Field('target_table'),
                     ##Field('filter_func', 'list:string'),
                     ##Field('trans_func', 'list:string')]
        ##return super(GatherFromField, self).make_form(fieldlist)

    ##def process_result(self, vars):
        ##"""docstring for process_result"""
        ##db = current.db
        ##filter_func = literal_eval(vars.filter_func) if vars.filter_func else None
        ##trans_func = literal_eval(vars.trans_func) if vars.trans_func else None

        ##rows = db(db[vars.source_table].id > 0).select()
        ##out = [r['target_field'] for r in rows]
        ##out = filter(filter_func, out) if filter_func else out
        ##out = [trans_func(i) for i in out] if trans_func else out
        ##out = [{vars.target_field: i} for i in out]
        ##return out


##class BulkUpdate(UtilForm):
    ##"""
    ##Perform a programmatic update to a field in one table.

    ##"""
    ##def process_result(self, vars):
        ##"""docstring for make_form"""
        ##db = current.db
        ##myrows = db(db[vars.source_table].id > 0).select()
        ##out = []
        ##for row in myrows:
            ##odict = {'id': row.id}
            ##for idx, sfield in vars.source_field:
                ##filterfunc = literal_eval(vars.filter_func[idx])
                ##if filterfunc(row[sfield]):
                    ##transfunc = literal_eval(vars.trans_func[idx])
                    ##odict[sfield] = transfunc(row[sfield])
                ##else:
                    ##pass
            ##out.append(odict)

    ##def write_vals(self, ttable, out):
        ##"""docstring for write_vals"""
        ##db = current.db
        ##db[ttable].BulkUpdate(**out)


##def migrate_field():
    ##"""
    ##"""
    ##db = current.db
    ##fields = {'plugin_slider_slides': ('content', 'slide_content')}
    ##for t, f in fields.iteritems():
        ##table = t
        ##source_field = f[0]
        ##target_field = f[1]
        ##items = db(db[table].id > 0).select()
        ##c = 0
        ##for i in items:
            ##values = {target_field: i[source_field]}
            ##i.update_record(**values)
            ##c += 1

    ##return {'records_copied': c}


##def migrate_table():
    ##db = current.db
    ##items = db(db.pages.id > 0).select()
    ##c = 0
    ##for i in items:
        ##db.journal_pages.insert(**{'journal_page': i.page})
        ##c += 1

    ##return dict(records_moved=c)


##def migrate_back():
    ##db = current.db
    ##items = db(db.images_migrate.id > 0).select()
    ##c = 0
    ##for i in items:
        ##c += 1
        ##db.images[i.id] = i.as_dict()

    ##return dict(records_updated=c)


##def import_from_csv():
    ##db = current.db
    ##try:
        ##db.paragraphs.truncate()
    ##except:
        ##print traceback.format_exc(5)
    ##mydir = '/home/ian/Dropbox/Downloads/Webdev/woh_export'
    ##files = ['node-export(43-nodes).1335558252.csv',
             ##'node-export(50-nodes).1335557844.csv',
             ##'node-export(50-nodes).1335557890.csv',
             ##'node-export(50-nodes).1335557934.csv',
             ##'node-export(50-nodes).1335558015.csv',
             ##'node-export(50-nodes).1335558056.csv',
             ##'node-export(50-nodes).1335558115.csv',
             ##'node-export(50-nodes).1335558151.csv',
             ##'node-export(50-nodes).1335558186.csv'
             ##]
    ###'node-export[](1-nodes).1335557290.export',
    ##fullfiles = [os.path.join(mydir, f) for f in files]

    ##for ff in fullfiles:
        ##with open(ff, 'rU') as csfile:
            ##rows = csv.DictReader(csfile)
            ##for row in rows:
                ###pprint(row)
                ##titlebits = row['title'].split('.') if row['title'] else [None, None, None]
                ##taxes = [v for k, v in row.iteritems()
                         ##if re.match(r'.*taxonomy.*', k)
                         ##and v not in ['NULL', '', 0, 'None', None]]
                ##topics = '|'.join(taxes) if taxes else None
                ##pullquote = row['field_pullquote[\'0\'][\'value\']'] \
                    ##if 'field_pullquote[\'0\'][\'value\']' in row.values() \
                    ##else None
                ##audio = row['field_audiolink[\'0\'][\'value\']'] \
                    ##if 'field_audiolink[\'0\'][\'value\']' in row.values() \
                    ##else None
                ##image_id = row['field_images[\'0\'][\'fid\']'] \
                    ##if 'field_images[\'0\'][\'fid\']' in row.values() \
                    ##else None
                ##image_alt = row['field_images[\'0\'][\'data\'][\'alt\']'] \
                    ##if 'field_images[\'0\'][\'data\'][\'alt\']' \
                    ##in row.values() else None
                ##image_title = row['field_images[\'0\'][\'data\'][\'title\']'] \
                    ##if 'field_images[\'0\'][\'data\'][\'title\']' \
                    ##in row.values() else None
                ##image_filename = row['field_images[\'0\'][\'filename\']'] \
                    ##if 'field_images[\'0\'][\'filename\']' in row.values() \
                    ##else None
                ##times = {}
                ##for k in ['changed', 'created']:
                    ##errors = 0
                    ##try:
                        ##times[k] = datetime.datetime.fromtimestamp(int(row[k]))
                    ##except (TypeError, ValueError):
                        ##times[k] = datetime.datetime.utcnow()
                        ##errors += 1
                    ##print '{} errors: {}'.format(k, errors)

                ##matches = {'uid': row['uid'],
                           ##'chapter': titlebits[0],
                           ##'section': titlebits[1] if len(titlebits) > 1 else 0,
                           ##'subsection': titlebits[2] if len(titlebits) > 1 else 0,
                           ##'display_title': row['field_displaytitle[\'0\'][\'value\']'],
                           ##'status': row['status'],
                           ##'changed': times['changed'],
                           ##'created': times['created'],
                           ##'body': row['body'],
                           ##'pullquote': pullquote,
                           ##'audio': audio,
                           ##'image_id': image_id,
                           ##'image_alt': image_alt,
                           ##'image_title': image_title,
                           ##'image_filename': image_filename,
                           ##'topics': topics}
                ##matches = {k: v for k, v in matches.iteritems() if not v in [None, 'NULL']}
                ##num = db.paragraphs.insert(**matches)
                ##print num


##class RowsFromField(UtilForm):
    ##"""
    ##Use values from one table field to create new records in another table.

    ##The strings provided for

    ##The values for source_fields, target_fields, filter_funcs, and
    ##transform_funcs will be aligned by index within the list of return values
    ##for each field. So source_fields[0] will be applied to target_fields[0],
    ##etc.

    ##"""
    ##def make_form(self):
        ##"""
        ##Return a form object to add rows from data in fields in another table.
        ##"""
        ##fieldlist = [Field('target_table'),
                     ##Field('target_fields', 'list:string')]
        ##return super(RowsFromField, self).make_form(fieldlist)

    ##def process_result(self, vars):
        ##db = current.db
        ##sourcerows = db(db[vars.target_table].id > 0).select()
        ##outrows = []
        ##for srow in sourcerows:
            ##outvals = {}
            ##for idx, sfield in enumerate(vars.source_fields):
                ##transval = vars.trans_funcs[idx](srow[sfield]) \
                    ##if len(vars.trans_funcs) > idx else srow[sfield]
                ##transval = vars.filter_funcs[idx](srow[sfield]) \
                    ##if len(vars.filter_funcs) > idx else None
                ##if transval:
                    ##outvals[vars.target_fields[idx]] = transval
            ##outrows.append(outvals)
        ##return outrows


##class RowsFromFilenames(UtilForm):
    ##"""
    ##"""
    ##def make_form(self):
        ##"""
        ##"""
        ##fieldlist = [Field('folder_path'),
                     ##Field('extra_fields', 'list:string')]
        ##return super(RowsFromFilenames, self).make_form(fieldlist)

    ##def process_result(self, vars):
        ##"""
        ##Return a list of dictionaries representing new rows in the target table.

        ##This version draws the values for the new rows from filenames in the
        ##specified directory.

        ##"""
        ##out = []
        ##mypath = vars.folder_path
        ##dirpath, dirnames, filenames = os.walk(mypath).next()
        ##filter_funcs = [literal_eval(ff) for ff in vars.filter_funcs]
        ##filenames = [n for ff in filter_funcs for n in filenames if ff(n)]
        ##out = [{vars.target_field: f} for f in filenames]
        ##xfields = [(x[0], literal_eval(x[1])) for x
                   ##in vars.extra_fields.split('|')]
        ##for orow in out:
            ##for xfield in xfields:
                ##orow[xfield[0]] = xfield[1](f)
        ##return out


##class ReplaceInField(UtilForm):
    ##"""
    ##Make a systematic set of string replacements for all values of one
    ##db field.
    ##"""
    ##def make_form(self):
        ##"""
        ##"""
        ##fieldlist = [Field('filter_func'),
                     ##Field('replacement_pairs', 'list:string')]
        ##return super(ReplaceInField, self).make_form(fieldlist)

    ##def process_result(self, vars):
        ##"""docstring for process_result"""
        ##db = current.db
        ##tf = vars.target_field
        ##reps = vars.replacement_pairs
        ##mypairs = [(v[0], v[1]) for r in reps for v in r.split('|')]
        ##myrows = db(db[vars.target_table].id > 0).select()
        ##out = [(row.id, multiple_replace(row[tf], mypairs)) for row in myrows]
        ##return out

    ##def write_vals(self, ttable, tfield, out):
        ##"""
        ##Update existing rows in ttable with the new value for tfield.
        ##"""
        ##db = current.db
        ##for outval in out:
            ##db[ttable](outval[0]).update(tfield=outval[1])
