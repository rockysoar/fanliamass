#!python
# -*- coding: utf-8 -*-

import sys, re, urlparse

def main(csvFile, parseQuery):
    f = open(csvFile, 'r');
    urlCodes = {}
    for url in f:
        url = url.strip(' "\'\r\n\t').lower()
        if not url: continue
        if re.search(r'\.(?:js|css|ico|png|jpg)', url): continue

        info = urlparse.urlparse(url)
        if not info.hostname: continue

        keys_ = []; 
        keys = re.split(r'/|-', info.path)
        # 从pathinfo中提取4个关键字
        for i in range(len(keys)):
            k = keys[i]
            if i == len(keys) - 1: v = ''
            else: v = keys[i+1]

            if dropPair(k, v, url): i += 1; continue;
            if dropItem(k): continue
            keys_.append(k)
        if len(keys_) > 4: keys_ = keys_[0:4]

        # 从querystring中提取1个关键字
        if parseQuery:
            kvs = urlparse.parse_qsl(info.query)
            for kv in kvs:
                if not kv: continue
                if dropPair(kv[0], kv[1], url) or dropItem(kv[0]): continue;
                keys_.append(kv[0])
                break

        hostname = info.hostname.replace('51fanli', 'fanli')
        urlCode = "%s/%s" % (hostname, '.'.join(keys_).strip('.'))
        if not urlCodes.get(urlCode): urlCodes[urlCode] = 1
        else: urlCodes[urlCode] += 1

    for k in urlCodes.items(): print k,v
    print len(urlCodes)
    f.close()

def dropPair(k, v, url = ''):
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
    drop = drop or re.search(r'keywords?', k) and re.search(r'search', url)

    return drop

def dropItem(k):
    drop = False
    drop = drop or 'index.php' == k
    drop = drop or not re.search(r'^[a-zA-Z_]\w{1,24}$', k)
    drop = drop or re.search(r'^c_(?:src|v|nt|aver)$', k)
    drop = drop or re.search(r'^\w+_(?:asc|desc)$', k)
    #http://zhide.fanli.com/p{N}分页参数
    drop = drop or re.search(r'^p\d+$', k, re.IGNORECASE)
    if drop: return drop

    # 数字字母混杂
    numTimes = re.findall(r'(\d+)', k)
    numCount = sum(c.isdigit() for c in k)
    numRate = numCount/len(k)
    drop = drop or (len(numTimes) >= 2 and numRate >= .575 and numRate <= .675)

    return drop

if '__main__' == __name__: 
    csvFile = '/usr/local/workdata/exchange/kafka-path-all.csv'
    # 是否解析querystring
    parseQuery = (len(sys.argv) == 2 and '1' == sys.argv[1])
    main(csvFile, parseQuery)

