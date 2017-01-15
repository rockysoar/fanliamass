# -*- coding: utf-8 -*-

import sys, re, urlparse

########## URL聚合 提取关键词数量限制8个 #########
# degree聚合程度: 
# 1: 低 pathinfo + querystring
# 2: 中 pathinfo + querystring, 仅保留符合PHP变量命名规则的关键词
# 3: 高 pathinfo, 仅保留符合PHP变量命名规则的关键词
def polymerize(url, degree = 3):
    url = url.strip(' "\'\r\n\t')
    if not url: return 

    info = urlparse.urlparse(url)
    if not info.hostname: return
    if re.search(r'\.(?:js|css|ico|png|jpe?g)', info.path): return

    keysPath, keysQuery = [], [] 
    keys = re.split(r'/|-', info.path)
    # 处理pathinfo
    for i in range(len(keys)):
        k = keys[i]
        v = k if i == len(keys) - 1 else keys[i+1]

        if dropPair(k, v, info.path, degree): i += 1; continue;
        if dropItem(k): continue
        keysPath.append(k)
    if len(keysPath) > 6: keysPath = keysPath[0:6]

    # 处理QueryString
    if degree < 3:
        kvs = urlparse.parse_qsl(info.query)
        for kv in kvs:
            if not kv: continue
            if keepPair(kv[0], kv[1], info.path): pass
            elif dropPair(kv[0], kv[1], info.path, degree) or dropItem(kv[0]): continue;
            kvStr = '%s=%s' % (kv[0], valueAbstract(kv[1]))
            keysQuery.append(kvStr)
        # 去重
        keysQuery = list(set(keysQuery))
    pickNum = min(6, 8 - len(keysPath))
    if len(keysQuery) > pickNum: keysQuery = keysQuery[0:pickNum]
    keysQuery.sort()

    hostname = polymerizeHostname(info.hostname)
    path = '/'.join(keysPath).strip('/')
    query = '&'.join(keysQuery).strip('&')

    urlCode = "%s/%s?%s" % (hostname, path, query)
    return urlCode.lower().strip(' /?')

def valueAbstract(value):
    if re.search(r'^[\d,;]+$', value): return '%d'
    return '%s'

def dropPair(k, v, path = '', degree = 3):
    drop = False
    k = k.lower()
    drop = drop or (type(v) != str)
    drop = drop or (len(v) < 3 or len(v) > 24)
    # 中度聚合
    drop = drop or (2 == degree and re.search(r'^[a-z]\w{2,23}$', v, re.I) is None)
    # ocp图片处理
    drop = drop or re.search(r'/ocp/', path)
    # 图片大小
    drop = drop or re.search(r'\d+(?:x|\*)\d*', v) or re.search(r'\d*(?:x|\*)\d+', v)
    # 网络类型
    drop = drop or re.search(r'^(?:c_)?nt$', k) and re.search(r'^(?:wifi|cell)$', v)
    # 追踪信息
    drop = drop or k in ['jsoncallback', 'callback', 'spm', 'lc', '_t_t_t', 't', '_t', '__', '_', 'abtest', 'v']
    # 页码
    drop = drop or k in ['size', 'psize', 'page_size', 'pagesize', 'psize', 'page', 'pidx', 'p', 't'] and re.search(r'^[\.\d-]*$', v)
    drop = drop or re.search('page|limit|offset', k) and re.search(r'^[\d-]*$', v)
    drop = drop or ('size' == k and (v in ['small', 'big']))
    # 排序
    drop = drop or re.search(r'^a?sort$', k) and re.search(r'sort|default|asc|des', v, re.I)
    drop = drop or k in ['verify_code', 'app_ref', 'deviceno', 'device_no', 'deviceid', 'devid', 'msg', 'security_id'] and len(v) > 12
    drop = drop or re.search(r'(start|end)_price', k) and v.isdigit()
    drop = drop or re.search(r'time', k) and re.search(r'\d{10}|0', v)
    drop = drop or k in ['ajax'] and v.isdigit()
    drop = drop or re.search(r'^http', v)
    drop = drop or re.search(r'^(start|offset|limit)$', k) and re.search(r'search', path)
    drop = drop or re.search(r'^utm_.*$', k) and len(v) > 12

    return drop

def keepPair(k, v, path = '', degree = 3):
    keep = False
    keep = keep or 'api' == k
    return keep 

def dropItem(k):
    drop = False
    k = k.lower()
    if (re.search(r'\.(php5?|htm|html5?|do|jsp|asp)$', k)):
        return False

    drop = drop or not re.search(r'^[a-z]\w{0,23}$', k)
    drop = drop or re.search(r'^c_(?:src|v|nt|aver)$', k)
    drop = drop or re.search(r'^\w+_(?:asc|desc)$', k)
    #http://zhide.fanli.com/p{N}分页参数
    drop = drop or re.search(r'^p\d+$', k)
    if drop: return drop

    # 数字字母混杂
    numTimes = re.findall(r'(\d+)', k)
    numCount = sum(c.isdigit() for c in k)
    numRate = numCount/len(k)
    #16进制字符串数字比例一般为0.625 上下浮动0.05
    drop = drop or (len(numTimes) >= 2 and numRate >= .575 and numRate <= .675)

    return drop

def polymerizeHostname(hostname):
    hostname = hostname.replace('51fanli', 'fanli')
    hostname = re.sub('l\d+', 'l%d', hostname)
    return hostname


########## 身份信息提取 ##########
def identity_picker(path, ip, utmo):
    pass
