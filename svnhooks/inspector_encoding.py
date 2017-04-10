# syntax, utf-8, no BOM

import sys,subprocess

SVNLOOK='/usr/bin/svnlook'
PHP='/usr/local/bin/php'

# the Changed File
resp = sys.argv[1]
cf = sys.argv[2].split(' ')[1]
cf = resp
if not cf.endswith('.php'): sys.exit(0);

# php syntax check
try:
    exitCode = subprocess.check_output('%s cat %s %s | %s -l | head -2 | tail -1')
except subprocess.CalledProcessError, e:
    print e
    sys.exit(1)

# BOM check
if "\0xEF\0xBB\0xBF" == open(cf,'rb').read(3):
    print 'BOM file-header in file %s must be removed.' % (cf)
