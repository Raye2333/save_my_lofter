# -*- coding: UTF-8 -*-

"""
This is a script to grab your creation information from the XML diary exported
from LOFTER.
Author: Ergou
Date: 2020/6/12
"""

from xml.etree import ElementTree as ET
import urllib.request
from datetime import datetime
import numpy as np
import time
import os


def makeDir():
    paths = ["Photo",
             "Text",
             "Video"]
    try:
        for p in paths:
            os.mkdir(p)
    except OSError:
        print("Creation of the directory %s failed" % p)
    else:
        print("Successfully created the directory %s " % p)


def getType(item):
    """Helper to get the type of a post"""
    thisType = item.find('type').text
    return thisType


def getTerm(item, keyword, isTxt=True):
    """Find tags"""
    try:
        thisTerm = item.find(keyword)
    except AttributeError as e1:
        thisTerm = 'N/A'
        print(e1)
        print("------(QwQ )Not Found------")
    except TypeError as e2:
        thisTerm = 'N/A'
        print(e2)
        print("------(QwQ )Not Found------")
    if thisTerm == None:
        thisTerm = 'N/A'
    if thisTerm == 'N/A':
        return thisTerm
    if isTxt:
        return thisTerm.text
    else:
        return thisTerm


def getCaption(item):
    thisCap = getTerm(item, 'caption')
    return modifyText(thisCap)


def getTime(item):
    ts = int(getTerm(item, 'publishTime', True))
    tStamp = float(ts/1000)
    tArray = time.localtime(tStamp)
    DateTime = time.strftime("%Y-%m-%d %H:%M:%S", tArray)
    return [ts, DateTime]


def getComments(item):
    cmItem = getTerm(item, 'commentList', False)
    comList = []
    if cmItem != 'N/A':
        com_lst = cmItem.findall('comment')
        for cm in com_lst:
            u_id = getTerm(cm, 'publisherNick', True)
            u_cm = getContent(cm)
            u_time = getTime(cm)
            m = u_id + ': ' + u_cm + '(' + u_time[1] + ')'
            comList.append(m)
    return comList


def getMedia(item, sendTime, tp, file_path):
    if getTerm(item, 'type') == 'Video' or getTerm(item, 'type') == 'Photo':
        if tp == 'Photo':
            links = getTerm(item, 'photoLinks')
            suffix = '.jpg'
            pos1 = links.find('"orign":"')
            if pos1 != -1:
                chopped = links[pos1+9:]
                pos2 = chopped.find('"')
                url = chopped[: pos2]
                print(url)
            else:
                return 'N/A'
        if tp == 'Video':
            links = getTerm(item, 'embed')
            suffix = '.mp4'
            pos1 = links.find('"video_down_url":"')
            if pos1 != -1:
                chopped = links[pos1+18:]
                pos2 = chopped.find('"')
                url = chopped[:pos2]
                print(url)
            else:
                return 'N/A'
        name = file_path + '/' + str(sendTime) + suffix
        print(name)
        urllib.request.urlretrieve(url, name)
        return name


def modifyText(txt):
    txt = txt.replace('<p>', '')
    txt = txt.replace('</p>', '')
    txt = txt.replace('<br />', '\n')
    txt = txt.replace('&nbsp;', ' ')
    txt = txt.replace('&middot;', '·')
    txt = txt.replace('&quot;', '"')
    txt = txt.replace('<a href=', '<')
    txt = txt.replace('</a>', '')
    txt = txt.replace('<li>', '')
    txt = txt.replace('</li>', '')
    return txt


def getContent(item):
    thisCont = getTerm(item, 'content', True)
    thisCont = modifyText(thisCont)
    return thisCont


def getTitle(item):
    thisTitel = getTerm(item, 'titel')
    return modifyText(thisTitel)


def getMusic(item):
    all_info = getTerm(item, 'embed')
    pos_mu_1 = all_info.find('"song_name":"')
    if pos_mu_1 != -1:
        chopped_1 = all_info[pos_mu_1+13:]
        pos_mu_2 = chopped_1.find('"')
        mu_name = chopped_1[:pos_mu_2]
    else:
        mu_name = 'N/A'
    pos_url_1 = all_info.find('"listenUrl":"')
    if pos_url_1 != -1:
        chopped_2 = all_info[pos_url_1+13:]
        pos_url_2 = chopped_2.find('"')
        url = chopped_2[:pos_url_2]
    else:
        url = 'N/A'
    return [mu_name, url]
