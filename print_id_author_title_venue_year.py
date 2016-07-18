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
        # &#X only happens once, but it's wrong and ftfy doesn't treat it the same way as &#x
        value_bytes = value_bytes.replace('&#X', '&#x')
        # same for ,, -- only happens once
        value_bytes = value_bytes.replace(',,', ',')
        # reverse line feed? no thanks
        value_bytes = value_bytes.replace('&#x8D;', '')
        # I don't even know...
        value_bytes = value_bytes.replace('&#scaron;', '&scaron;')
        # you'd think that ;; sequences would make sense -- a non-final author
        # with a first name ending in an html entity, but this actually fixes
        # more things than it breaks (need to address the few cases where it does break)
        value_bytes = value_bytes.replace(';;', ';')
        # UTF-8 is a better first guess, but will break on some of the input
        try:
            value_unicode = value_bytes.decode('UTF-8')
        except UnicodeDecodeError:
            value_unicode = value_bytes.decode('ISO-8859-2')
        value = fix_text(value_unicode, fix_entities=True, normalization='NFKC')
        # ftfy docs says it will repeat if needed, but it doesn't?
        value = fix_text(value, fix_entities=True, normalization='NFKC')
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
