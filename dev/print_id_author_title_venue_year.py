#!/usr/bin/env python
import sys
import re
from itertools import groupby
from ftfy import fix_text

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
