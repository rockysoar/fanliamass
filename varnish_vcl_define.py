# -*- coding: utf-8 -*-

import sys, re, urlparse

## 尝试计算varnish cache object key, 参考default.vcl
def vcl_hash_url(url):
    url = re.sub(r'(?:\?|&)(?:spm|devid|c_aver|c_src|c_v|c_nt|mc|abtest)=[^&]*', '', url, re.I)
    return url

def vcl_hash_key(url, utmt, serverip):
    url = vcl_hash_url(url)
    uniqKey = '%s#%s#%s' % (url, utmt, serverip[8:])
    return uniqKey

def vcl_key_polymerize(hashKey):
    if not hashKey or len(hashKey) < 24: return

    url, utmt, serverip = tuple(hashKey.split('#', 3))
    urlTmpl = polymerizer.polymerize(url, 2)
    return (urlTmpl, utmt, serverip)
