#!python
# -*- coding: utf-8 -*-

import sys
import url_polymerizer as polymerizer

if '__main__' == __name__: 
    csvFile = '/usr/local/workdata/exchange/kafka-ocp.csv'
    # 是否解析querystring
    parseQuery = (len(sys.argv) > 1 and '1' == sys.argv[1])

    f = open(csvFile, 'r')
    urlRules = {}
    for url in f:
        urlRule = polymerizer.polymerize(url, parseQuery)
        if not urlRule: continue

        if not urlRules.get(urlRule): urlRules[urlRule] = 1
        else: urlRules[urlRule] += 1

    for k in urlRules.items(): print k
    print len(urlRules)
    f.close()

