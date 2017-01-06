#!python
# -*- coding: utf-8 -*-

import sys, re, urlparse, csv
import url_polymerizer as polymerizer

if '__main__' == __name__: 
    csvFile = '/usr/local/workdata/exchange/kafka-10000.csv'
    # 是否解析querystring
    parseQuery = (len(sys.argv) == 2 and '1' == sys.argv[1])

    f = open(csvFile, 'rb')
    urlRules, ips = {}, {}
    for line in csv.reader(f):
        if len(line) != 2: continue

        url, ip = tuple(line)
        if len(url) == 0 or len(ip) == 0: continue

        urlRule = polymerizer.polymerize(url, parseQuery)
        if not urlRule: continue

        # 统计PV
        if not urlRules.get(urlRule): urlRules[urlRule] = 1
        else: urlRules[urlRule] += 1

        # 统计UV
        if not ips.get(ip): ips[ip] = 1
        else: ips[ip] += 1

    for k in urlRules.items(): print k
    #for k in ips.items(): print k
    print len(urlRules), len(ips)
    f.close()

