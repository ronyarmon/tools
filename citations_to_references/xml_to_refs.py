#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
import re
import os
def citation_to_reference (index, citation):
    split1,split2,split3 = citation.split ('NameList')
    split1 = (split1 + split3).split('\n')
    keep_fields = ['Year','Title','JournalName','Volume','Pages']
    field_content = {}
    for field in keep_fields:
        if field in citation:
            content = [item for item in split1 if field in item][0]
            content = re.findall('{f}>(.*)<'.format(f=field),content)[0]
            field_content [field] = content
        else:
                field_content [field] = '!!!MISSING: {f}!!!'.format (f=field)

    # Author names
    author_names = split2.split ('\n')
    author_names = [re.sub("<|>|ns|:|\/|\d|'|Person|\s{2,}", ' ',item) for item in author_names]
    author_names = [item.rstrip().lstrip() for item in author_names if (('First' in item)|('Last' in item))]
    first_names = [item for item in author_names if 'First' in item]
    first_names = [re.sub ('First','',item).rstrip().lstrip() for item in first_names]
    first_names = [ ('').join ([(name.split(' ')[0][0]),(('').join(name.split(' ')[1:]))]) for name in first_names]
    first_names = [re.sub('\.','',name) for name in first_names]
    last_names = [item for item in author_names if 'Last' in item]
    last_names = [re.sub ('Last','',item).rstrip().lstrip() for item in last_names]

    if len (first_names)==1:
        authors = '{ln0} {fn0}'.format (ln0=last_names[0],fn0=first_names[0])
    elif len (first_names)==2:
        authors = '{ln0} {fn0} & {ln1} {fn1}'.format (ln0=last_names[0],fn0=first_names[0],ln1=last_names[1],fn1=first_names[1])
    elif len (first_names)==3:
        authors = '{ln0} {fn0}, {ln1} {fn1} & {ln2} {fn2}'.format (ln0=last_names[0],fn0=first_names[0],                                                                   ln1=last_names[1],fn1=first_names[1],                                                                   ln2=last_names[2],fn2=first_names[2])
    else:
        authors = '{ln0} {fn0}, {ln1} {fn1}, {ln2} {fn2} et al.'.format (ln0=last_names[0],fn0=first_names[0],                                                                   ln1=last_names[1],fn1=first_names[1],                                                                   ln2=last_names[2],fn2=first_names[2])
    field_content ['Authors'] = authors

    reference = '{authors}({year}) {title}. {jname} {volume}: {pages}'.format (authors = field_content['Authors'],\
                year = field_content['Year'],title = field_content ['Title'], jname = field_content ['JournalName'],\
                volume = field_content ['Volume'], pages = field_content ['Pages'])
    return reference

tree = ET.parse('citations.xml')
root = tree.getroot()
as_string = ET.tostring(root, encoding='utf8').decode('utf8')
citations = as_string.split('<ns0:Tag>')[1:]
with open ('references_extracted.txt','w') as f:
    for index, citation in enumerate (citations):
        reference = citation_to_reference (index,citation)
        print (reference)
        f.write ('{ref}\n'.format(ref = reference))
