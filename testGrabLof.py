# -*- coding: UTF-8 -*-

"""Testing file for GrabLof script"""
from grabLof import getTerm
from grabLof import getType
from grabLof import getCaption
from grabLof import getContent
from grabLof import getTime
from grabLof import getComments
from grabLof import getMedia
from grabLof import makeDir
from grabLof import getContent
from grabLof import modifyText
from grabLof import getMusic

from xml.etree import ElementTree as ET
import urllib.request
from datetime import datetime
import numpy as np

source = "tormenta.xml"
s2 = "ergo.xml"
tree1 = ET.parse(source)
t2 = ET.parse(s2)

items1 = tree1.findall('.//PostItem')
items2 = t2.findall('.//PostItem')

"""
for item in items1:
    try:
        thisType = getType(item)
        print(thisType)
    except AttributeError as Err:
        print(Err)


for level in items2:
    tag = getTerm(level, 'title')
    print(tag)


for item in items2:
    cap = getCaption(item)
    print(cap)

for item in items1:
    cap = getCaption(item)
    print(cap)

for item in items1:
    cont = getContent(item)
    print(cont)

i = 0
for item in items2:
    cont = getTime(item)
    i = i+1
    print(cont)
print(i)

for item in items2:
    getComments(item)

# makeDir()

for item in items2:
    tm = getTime(item)
    tp = getType(item)
    print(getMedia(item, tm[0], tp, tp))

for item in items1:
    print(getContent(item))

for item in items2:
    print(getCaption(item))
"""

for item in items1:
    print(getMusic(item))
