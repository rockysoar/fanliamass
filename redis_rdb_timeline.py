#!/usr/bin/env python
# coding: utf-8

'''Used to analyze redis RDB timeline: when rdb started or terminated'''

import glob, re, sys
from datetime import datetime

# 时间轴起点
baseTime = int(datetime.strptime('2017-01-29 00:00:00', '%Y-%m-%d %H:%M:%S').timestamp())
redisLogs = '/usr/local/workdata/exchange/redislog/redis_*.log'

'''Read log line by line and parse the start time and terminate time of every rdb process'''
def rdb_dtline_picker(log):
    timeline, startTime, endTime, tmpTime = ('', 0, 0, baseTime)

    with open(log, 'r') as fd:
        for line in fd:
            rdbDtline = re.search(r'\[\d+\] (.+?) \* Background saving (started|terminated)', line, re.I)
            if rdbDtline is None: continue

            if 'started' == rdbDtline.group(2): 
                startTime = int(datetime.strptime('2017 ' + rdbDtline.group(1), '%Y %d %b %H:%M:%S.%f').timestamp())
            else: 
                endTime = int(datetime.strptime('2017 ' + rdbDtline.group(1), '%Y %d %b %H:%M:%S.%f').timestamp()) + 1

            if startTime < baseTime: continue
            if startTime > baseTime + 1 * 86400: break
            if startTime > endTime: continue
            
            if startTime > tmpTime:
                timeline += '_'.ljust(startTime - tmpTime, '_')
            timeline += '.'.ljust(endTime - startTime, '.')

            tmpTime = endTime
            startTime, endTime = (0, 0)

        timeline = timeline.ljust(86400, '_')
        return timeline

if '__main__' == __name__:
    timeRanges = {}
    for log in glob.glob(redisLogs):
        port = re.sub(r'\D', '', log)
        timeRanges[port] = rdb_dtline_picker(log)

    ports = list(timeRanges.keys())
    ports.sort()
    sys.stdout.write('%8s' % ('Time'))
    for port in ports: sys.stdout.write('%5s' % (port))
    sys.stdout.write("%6s\n" % ("count"))

    for i in range(0, 86400):
        sys.stdout.write(datetime.fromtimestamp(baseTime + i).strftime('%H:%M:%S'))

        cnt = 0
        for port in ports:
            if '.' == timeRanges[port][i]: cnt += 1
            sys.stdout.write('%5s' % (timeRanges[port][i]))
        sys.stdout.write("%6d\n" % (cnt))


