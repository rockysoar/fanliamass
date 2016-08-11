#!/usr/bin/python
# coding: utf-8

import sys, math, binascii

def key_slice(key, sliceNum):
    mod = binascii.crc32(key) % int(sliceNum)
    sliceFormat = r's0{0:0%dd}' % math.log(int(sliceNum), 2)
    return sliceFormat.format(int(bin(mod)[2:]))

def redis_cli_assamble(proj, keySlice):
    return 'redis-cli -h %s.redis-%s.51fanli.it ' % (proj, keySlice);

def main():
    if len(sys.argv) != 4:
        raise SystemExit, 'arguments invalid: %s project total-slice-num key' % sys.argv[0]

    proj, sliceNum, key = sys.argv[1:]
    keySlice = key_slice(key, sliceNum)

    cli = redis_cli_assamble(proj, keySlice)
    print cli

if '__main__' == __name__:
    main()

