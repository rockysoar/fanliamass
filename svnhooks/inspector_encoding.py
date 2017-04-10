# syntax, utf-8, no BOM

import sys,subprocess

SVNLOOK='/usr/bin/svnlook'
PHPBIN='/usr/bin/php'

# the Changed File
resp = sys.argv[1]
cf = sys.argv[2].split(' ')[1]
if not cf.endswith('.php'): sys.exit(0);

# php syntax check
try:
    cmd = '%s cat %s %s | %s -l' % (SVNLOOK, resp, cf, PHPBIN)
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as e:
    print(e.output)
    sys.exit(1)

# BOM check
cmd = '%s cat %s %s | head -1' % (SVNLOOK, resp, cf)
firstLine = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
if "\0xEF\0xBB\0xBF" == firstLine[0:3]:
    print('BOM file-header in file %s must be removed.' % (cf))
    sys.exit(1)

sys.exit(0)

