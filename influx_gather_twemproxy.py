#!/usr/bin/env python
# coding: utf-8

import os, sys, socket, json, threading, re
from influxdb import InfluxDBClient

def influx_create_points(points):
    if type(points) is dict: points = [points]
    if type(points) is not list: return

    # InfluxDBClusterClient
    dbCfg = {"host": "192.168.75.114", "port": "8086", "user": "influx", "password": "influx", "database": "twemproxy"}
    influxClient = InfluxDBClient(dbCfg['host'], dbCfg['port'], dbCfg['user'], dbCfg['password'], dbCfg['database'])
    influxClient.write_points(points)

def twemproxy_info_dump(ncHost, ncPort=22222):
    '''
    collect twemproxy(as know as nutcracker) statistic information
    '''
    # collect all grafana points to this list
    influxPoints = []

    # @todo handle timeout
    socketHandler = socket.socket()
    socketHandler.settimeout(3)
    socketHandler.connect((ncHost, int(ncPort)))
    jsonStr = ""
    while 1:
        resp = socketHandler.recv(2048)
        if not resp: break
        jsonStr += resp
    socketHandler.close()
    twInfo = json.loads(jsonStr)

    # 并发连接数
    influxPoints.append({
        'measurement': 'nc_connections',
        "tags": {'host': ncHost},
        "fields": {
            'connections': twInfo.get('curr_connections', 0), 
        }
    })

    # 统计一台twemproxy所有redis的总量
    requests, responses, client_err, server_err, server_timeout = 0, 0, 0, 0, 0
    for key, twInfo_ in twInfo.iteritems():
        if type(twInfo_) is not dict: continue

        # parse substructure information
        subkey = re.sub(r'^(.+)-(\d{4,5})$', r'\1:\2', key)
        redisInfo = twInfo_.get(subkey)

        influxPoints.append({
            'measurement': 'nc_requests',
            'tags': {'host': ncHost, 'group': subkey.split('.')[0], 'redis': subkey},
            'fields': {
                'client_err': twInfo_.get('client_err', 0), 'server_err': redisInfo.get('server_err', 0),
                'requests': redisInfo.get('requests', 0), 'responses': redisInfo.get('responses', 0),
                'server_timeout': redisInfo.get('server_timeout', 0)
            }
        })

    # write to influxDB
    influx_create_points(influxPoints)

if '__main__' == __name__:
    iplist = "/opt/scripts/grafana/twemproxy/iplist";
    if not os.path.exists(iplist): 
        raise SystemExit, 'File %s Not Exists!' % iplist

    threads = []
    for host in open(iplist):
        t = threading.Thread(target = twemproxy_info_dump, args = tuple(host.split(':')))
        threads.append(t)

    [t.start() for t in threads]
    [t.join(3) for t in threads]

    print 'Collection complate: %d' % len(threads) 

