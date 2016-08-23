#!/usr/bin/env python
# coding: utf-8

import os, sys, socket, json, threading, re, redis
from influxdb import InfluxDBClient

def influx_create_points(points):
    if type(points) is dict: points = [points]
    if type(points) is not list: return

    # InfluxDBClusterClient
    dbCfg = {"host": "192.168.75.114", "port": "8086", "user": "influx", "password": "influx", "database": "twemproxy"}
    influxClient = InfluxDBClient(dbCfg['host'], dbCfg['port'], dbCfg['user'], dbCfg['password'], dbCfg['database'])
    influxClient.write_points(points)

def redis_info_dump(redisHost, redisPort):
    r = redis.Redis(redisHost, int(redisPort))
    info = r.info()
    influxPoints = []
    influxPoints.append({
        'measurement': 'redis_connections',
        "tags": {'group': redisHost.split('.')[0],'host': '%s:%s' % (redisHost, redisPort)},
        "fields": {
            'connected': info.get('connected_clients'), 
            'blocked': info.get('blocked_clients'),
            'max_input_buffer': info.get('client_biggest_input_buf'),
            'max_output_list': info.get('client_longest_output_list'),
        }
    })
    influx_create_points(influxPoints)

if '__main__' == __name__:
    instances = "/opt/scripts/grafana/twemproxy/redis-instances";
    if not os.path.exists(instances): 
        raise SystemExit, 'File %s Not Exists!' % instances

    threads = []
    for host in open(instances):
        host = host.strip('\n')
        if not host: continue
        t = threading.Thread(target = redis_info_dump, args = tuple(host.split(':')))
        threads.append(t)

    [t.start() for t in threads]
    [t.join(3) for t in threads]

    print 'Collection complate: %d' % len(threads) 

