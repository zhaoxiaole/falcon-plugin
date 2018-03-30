#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-28 19:14:32
# @Author  : zhaoxiaole (zhaoxiaole1993@sina.com)

from xml.etree import ElementTree as ET
from itertools import chain
import time
import json
import socket
import urllib2

url = 'http://127.0.0.1:8161/admin/xml/queues.jsp'
username = 'admin'
password = 'admin'

def get_queues_info():
    req = urllib2.HTTPPasswordMgrWithDefaultRealm()
    req.add_password(None, url, username, password)
    handler = urllib2.HTTPBasicAuthHandler(req)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    page = urllib2.urlopen(url,timeout=3)
    html =page.read()
    per = ET.fromstring(html)
    name=per.findall('queue')
    othercolumn=per.findall('queue/stats')
    info=list(chain(*zip(name, othercolumn)))
    return info
def get_ip_address(key):
    if key=='ip':
        return socket.gethostbyname(socket.gethostname())
    elif key=='hostname':
        return socket.gethostname()
def get_xml_size():
    output = []
    qinfo=get_queues_info()
    l=len(qinfo)
    column=[('pending','size'),('consumers','consumerCount'),('enqueue','enqueueCount'),('dequeued','dequeueCount')]
    counterType=['GAUGE','COUNTER']
    i=0
    while i<l:
        dic=dict((qinfo[i+1].attrib).items()+(qinfo[i].attrib).items())
        i=i+2
        for ctype in counterType:
            for item in column:
                t = {}
                t['endpoint'] = get_ip_address('hostname')
                t['timestamp'] = int(time.time())
                t['step'] = 60
                t['tags'] = 'name=%s' % dic["name"]
                if ctype=='COUNTER':
                    if item[0]=='consumers' or item[0]=='pending':
                        continue
                    t['metric'] = 'activemq_%s_rate' % item[0]
                elif ctype=='GAUGE':
                    t['metric'] = 'activemq_%s' % item[0]
                t['value'] = dic[item[1]]
                t['counterType'] = ctype
                output.append(t)
    return output   
if __name__ == "__main__":
    d = get_xml_size()
    if d:
        print json.dumps(d)
