#!python
# -*- coding: utf-8 -*-

import sys
import url_polymerizer as polymerizer

if '__main__' == __name__: 
    csvFile = '/usr/local/workdata/exchange/kafka-ocp.csv'
    # 聚合度
    degree = sys.argv[1] if len(sys.argv) > 1 else '3'
    degree = int(degree)
    if degree not in [1, 2, 3]: degree = 3;

    f = open(csvFile, 'r')
    urlRules = {}
    for url in f:
        urlRule = polymerizer.polymerize(url, degree)
        if not urlRule: continue

        if not urlRules.get(urlRule): urlRules[urlRule] = 1
        else: urlRules[urlRule] += 1

    for k in urlRules.items(): print k
    print len(urlRules)
    f.close()

