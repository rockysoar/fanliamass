#!python
# -*- coding: utf-8 -*-

import sys, csv, re
import varnish_vcl_define as vcl
import url_polymerizer as polymerizer

if '__main__' == __name__: 
    csvFile = '/usr/local/workdata/exchange/varnish-hash.csv'
    f = open(csvFile, 'r')
    urlTmpls, hashKeys, c = {}, {}, 0
    for info in csv.reader(f):
        c += 1
        if c > 1000000: break

        serverip, url, hitmiss, utmt = tuple(info)
        # skip the first line
        if len(url) < 24: continue

        hashKey = vcl.vcl_hash_key(url, utmt, serverip)
        #hashKey = vcl.vcl_hash_url(url)
        if not hashKeys.get(hashKey): hashKeys[hashKey] = 0
        hashKeys[hashKey] += 1

    for hashKey in hashKeys:
        try:
            url, utmt, serverip = tuple(hashKey.split('#', 3))
            urlTmpl = '%s#%s#%s' % (polymerizer.polymerize(url), utmt, serverip)
            #[访问量, url变种]
            if not urlTmpls.get(urlTmpl): urlTmpls[urlTmpl] = [0, 0]
            urlTmpls[urlTmpl][0] += hashKeys[hashKey]
            urlTmpls[urlTmpl][1] += 1
        except:
            print hashKey

    for k, v in urlTmpls.items(): print k, ',', v[0], ',', v[1]
    print 'cache key nums/requests', len(hashKeys), sum(hashKeys[k] for k in hashKeys)


