#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
from itertools import groupby
# easy_install -U 'ftfy<5'
from ftfy import fix_text
from ftfy.fixes import htmlentitydefs

nonstandard_entities = [
    ('ccaron', u'č'),
    ('Ccaron', u'Č'),
    ('cacute', u'ć'),
    ('Sacute', u'Ś'),
    ('Scedil', u'Ş'),
    ('nacute', u'ń'),
    ('ncaron', u'ň'),
    ('scedil', u'ş'),
    ('slig', u'ß'),
    ('zcaron', u'ž'),
]
for name, unicode_value in nonstandard_entities:
    htmlentitydefs.name2codepoint[name] = ord(unicode_value)

def _id_field_iter(text):
    current_id = None
    for match in re.finditer(r'^(\w+)\s+=\s+\{\s*(.*?)\s*\}$', text, re.MULTILINE | re.DOTALL):
        key, value_bytes = match.groups()
        value = fix_text(value_bytes.decode('ISO-8859-2'), normalization='NFKC')
        if key == 'id':
            current_id = value
        yield current_id, (key, value)

def _id_dict_iter(text):
    '''
    Yield tuples of (acl_id, metadata), where metadata is a dict with the keys:
        id, year, title, venue, author
    '''
    for acl_id, id_fields in groupby(_id_field_iter(text), lambda id_keyval: id_keyval[0]):
        yield acl_id, dict(fields for acl_id, fields in id_fields)

text = sys.stdin.read()
for acl_id, metadata in _id_dict_iter(text):
    print u'{id}\t{author}\t{title}\t{venue}\t{year}'.format(**metadata).encode('utf-8')
