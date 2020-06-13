# -*- coding: UTF-8 -*-

import pandas as pd
from xml.etree import ElementTree as ET
import urllib.request
from datetime import datetime
import time
import os
import os.path
import requests


def makeDir(p):
    try:
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
        if thisTerm == None:
            thisTerm = 'N/A'
            return thisTerm
        if thisTerm == 'N/A':
            return thisTerm
        if isTxt:
            return thisTerm.text
        else:
            return thisTerm
    except AttributeError as e1:
        thisTerm = 'N/A'
        print(e1)
        print("------(QwQ )Not Found------")
        if thisTerm == None:
            thisTerm = 'N/A'
            return thisTerm
        if thisTerm == 'N/A':
            return thisTerm
        if isTxt:
            return thisTerm.text
        else:
            return thisTerm
    except TypeError as e2:
        thisTerm = 'N/A'
        print(e2)
        print("------(QwQ )Not Found------")
        if thisTerm == None:
            thisTerm = 'N/A'
            return thisTerm
        if thisTerm == 'N/A':
            return thisTerm
        if isTxt:
            return thisTerm.text
        else:
            return thisTerm


def modifyText(txt):
    if type(txt) != str:
        return 'N/A'
    else:
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
    thisTitle = getTerm(item, 'title')
    return modifyText(thisTitle)


def getCaption(item):
    thisCap = getTerm(item, 'caption', True)
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


def download(URL, path):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
              AppleWebKit/537.36 (KHTML, like Gecko) \
              Chrome/35.0.1916.114 Safari/537.36',
              'Cookie': 'AspxAutoDetectCookieSupport=1'}
    reqst = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        pic = urllib.request.urlopen(reqst)
        print('downloading:' + URL)
        print(path)
        path = os.path.abspath(path)
        with open(path, 'wb') as localFile:
            localFile.write(pic.read())
    except Exception as e:
        print(e)


def getMedia(item, sendTime, tp, file_path):
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
    download(url, name)
    return [name, url]


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


Title = []
Date = []
Type = []
File = []
Link = []
Comments = []
Content = []
Tag = []


def addArchive(t, d, p, f, l, cm, cn, tag):
    Title.append(t)
    Date.append(d)
    Type.append(p)
    File.append(f)
    Link.append(l)
    Comments.append(cm)
    Content.append(cn)
    Tag.append(tag)


def grabMedia(item, tp):
    title = getTitle(item)
    time = getTime(item)
    file, link = getMedia(item, time[0], tp, tp)
    cm = getComments(item)
    cn = getCaption(item)
    tag = getTerm(item, 'tag')
    addArchive(title, time[1], tp, file, link, cm, cn, tag)


def grabText(item, tp):
    title = getTitle(item)
    time = getTime(item)
    ts = time[0]
    cn = getContent(item)
    file = 'Text/'+str(ts)+'.txt'
    text_file = open(file, "w")
    n = text_file.write(cn)
    text_file.close()
    cm = getComments(item)
    link = file
    tag = getTerm(item, 'tag')
    addArchive(title, time[1], tp, file, link, cm, cn, tag)


def grabMusic(item, tp):
    title = getTitle(item)
    time = getTime(item)
    cn = getCaption(item)
    file, link = getMusic(item)
    cm = getComments(item)
    tag = getTerm(item, 'tag')
    addArchive(title, time[1], tp, file, link, cm, cn, tag)


def save_my_lofter(src):
    for p in ['Video', 'Photo', 'Text']:
        try:
            with open(os.path.abspath(p)) as f:
                print(f.readlines())
        except IOError:
            makeDir(p)
            print("Create Directory " + p)

    tree = ET.parse(src)
    items = tree.findall('.//PostItem')
    i = 1
    for item in items:
        tp = getType(item)
        if tp == 'Video' or tp == 'Photo':
            grabMedia(item, tp)
            print(tp)
        elif tp == 'Text':
            grabText(item, tp)
            print(tp)
        else:
            grabMusic(item, tp)
            print(tp)
        print(i)
        i += 1

    data = {'标题':  Title,
            '日期': Date,
            '类别': Type,
            '文件名': File,
            '文件链接': Link,
            '评论': Comments,
            '内容': Content,
            '相关标签': Tag
            }
    pos1 = src.find('.xml')
    chopped = src[:pos1]
    info_name = chopped + '.csv'
    info_pd = pd.DataFrame(data, columns=['标题',
                                          '日期', '类别', '文件名', '文件链接',
                                          '评论', '内容', '相关标签'])
    info_pd.to_csv(info_name, encoding='utf_8_sig')


if __name__ == "__main__":
    src = input('请输入你的Lofter日志文件名称（含.xml后缀）：')
    save_my_lofter(src)
