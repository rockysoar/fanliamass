#!python
# -*- coding: utf-8 -*-

import sys
import url_polymerizer as polymerizer

if '__main__' == __name__: 
    csvFile = '/usr/local/workdata/exchange/kafka-path-1000.csv'
    # 是否解析querystring
    parseQuery = (len(sys.argv) == 2 and '1' == sys.argv[1])

    f = open(csvFile, 'r')
    urlCodes = {}
    for url in f:
        urlCode = polymerizer.polymerize(url, parseQuery)
        if not urlCode: continue

        if not urlCodes.get(urlCode): urlCodes[urlCode] = 1
        else: urlCodes[urlCode] += 1

    for k in urlCodes.items(): print k
    print len(urlCodes)
    f.close()

