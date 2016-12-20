#!python
# -*- coding: utf-8 -*-

import re, urlparse

def main(csvFile):
    f = open(csvFile, 'r');
    urlCodes = {}
    for url in f:
        url = url.strip(' "\'\r\n\t')
        if not url: continue
        if re.search(r'\.(?:js|css|png|jpg)', url): continue

        info = urlparse.urlparse(url)

        keys_ = []; 
        keys = re.split(r'/|-', info.path)
        for i in range(len(keys)):
            k = keys[i]
            if i == len(keys) - 1: v = ''
            else: v = keys[i+1]

            if dropPair(k, v): i += 1; continue;
            if dropItem(k): continue
            keys_.append(k)
        if len(keys_) > 4: keys_ = keys_[0:4]

        kvs = urlparse.parse_qs(info.query)
        for k, v in kvs.items():
            if not v: continue
            if dropPair(k, v[0]) or dropItem(k): continue;
            keys_.append(k)

        if len(keys_) == 0: continue
        if len(keys_) > 6: keys_ = keys_[0:6]

        urlCode = "%s/%s" % (info.hostname, '.'.join(keys_).strip('.').lower())
        if not urlCodes.get(urlCode): urlCodes[urlCode] = 1
        else: urlCodes[urlCode] += 1

    for k in urlCodes.items(): print k,v
    print len(urlCodes)
    f.close()

def dropPair(k, v):
    drop = False
    k = k.lower()
    drop = drop or (type(v) != str)
    drop = drop or re.search(r'[\w\-\.~=]{31,}', v)
    drop = drop or (re.search(r'^(?:c_)?nt$', k) and re.search(r'^(?:wifi|cell)$', v))
    drop = drop or (k in ['jsoncallback', 'spm', 'lc', '_t_t_t', 't', '_t', '__', '_'])
    drop = drop or ((k in ['size', 'psize', 'page_size', 'pagesize', 'psize', 'page', 'p']) and re.search(r'^\d*$', v))
    drop = drop or ('size' == k and (v in ['small', 'big']))
    drop = drop or ('sort' == k and re.search(r'default|(\w+_(?:asc|desc))', v, re.IGNORECASE))
    drop = drop or (k in ['verify_code', 'app_ref', 'deviceno', 'device_no', 'devid', 'msg', 'security_id'] and re.search(r'^\w{12,}', v))

    return drop

def dropItem(k):
    drop = False
    #drop = drop or 'index' == k
    drop = drop or not re.search(r'^[a-zA-Z_]\w{1,24}$', k)
    drop = drop or re.search(r'^c_(?:src|v|nt|aver)$', k)

    # 数字字母混杂
    m = re.findall(r'(\d+)', k)
    drop = drop or (len(m) == 2 and len(m[1]) >= 3)

    if len(k) >= 12:
        numCount = 0
        for i in k:
            if ord(i) >=48 and ord(i) <= 57: numCount += 1
        numRate = numCount/len(k)
        drop = drop or (numRate >= .575 and numRate <= .675)

    return drop

if '__main__' == __name__: 
    main('/usr/local/workdata/exchange/kafka-path-all.csv')

