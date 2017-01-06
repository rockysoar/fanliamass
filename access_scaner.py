#!python
# -*- coding: utf-8 -*-
# 账户扫描行为监控

import sys, re

RE_COOKIE_ID = re.compile(r'ID:([\d-]+)', re.IGNORECASE)
RE_USERID = re.compile(r'\b(?:userid|uid)=(\d+)', re.IGNORECASE)
RE_UNAME = re.compile(r'\b(?:useremail|username|user_email)=([^&]+)', re.IGNORECASE)
RE_DEVID = re.compile(r'\bdevid=(\d+)', re.IGNORECASE)
RE_MOBILE = re.compile(r'\b(?:mobile|tel|smobile)=(1[34578]\d{9})\b', re.IGNORECASE)
RE_IP_IGNORE = re.compile(r'^(?:192\.168\.2|10\.0\.8)\.\d{1,3}$')

def visitor_identity(path, ip, utmo, cookie):
    # 内网访问不处理
    if RE_IP_IGNORE.match(ip): return

    cookieId = RE_COOKIE_ID.search(cookie)
    userId = RE_USERID.search(path)
    userName = RE_UNAME.search(path)
    devId = RE_DEVID.search(path)
    mobile = RE_MOBILE.search(path)

    # 字典描述访问者身份, 攻击者可能变化身份
    return {
        'ip' : ip,
        'utmo' : utmo,
        'cookieId' : cookieId,
        'userId' : userId,
        'userName' : userName,
        'devId' : devId,
        'mobile' : mobile,
    }

def identity_recognition():
    pass
