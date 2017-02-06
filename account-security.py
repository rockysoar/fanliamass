#!python
# -*- coding: utf-8 -*-

import sys, re, urlparse, csv
import url_polymerizer as polymerizer

if '__main__' == __name__: 
    csvFile = '/usr/local/workdata/exchange/kafka-user.csv'
    # 是否解析querystring
    parseQuery = (len(sys.argv) == 2 and '1' == sys.argv[1])

    f = open(csvFile, 'rb')
    utmos, userids = {}, {}
    for line in csv.reader(f):
        if len(line) != 4: continue

        ip, userid, utmo, path = tuple(line)
        if not url or not ip: continue
        if not utmo: utmo = '-' 
        if not userid: userid = '-' 

        if not utmos.get(ip): utmos[ip] = {}
        if not utmos[ip].get(utmo): utmos[ip][utmo] = 0

        utmos[ip][utmo] += 1

    for k in ips: 
        print k, len(ips[k]), sum(i for i in ips[k].values())

    f.close()

