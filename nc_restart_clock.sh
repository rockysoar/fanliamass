#! /bin/bash
#crontab * * * * * /bin/bash nc_restart_clock.sh

MAIL_ALARM='junhua.zhang@fanli.com'
RESTART_LOCK='/usr/local/webdata/fsdk/tools/restart.lock'
RESTART_REASON='/tmp/nc_restart_reason.log'

# fsdk项目不存在
if [ ! -f $RESTART_LOCK ]; then
    return 0
fi

if [ '1' -ne `cat $RESTART_LOCK` ]; then
    return 0
fi

# new line
echo >> $RESTART_REASON
`/etc/init.d/nutcracker restart >> $RESTART_REASON 2>&1`

tr -t "\r" "\n" < $RESTART_REASON | tr -cd '\11\12\40-\176' | mail -s "Twemproxy restart alarm" $MAIL_ALARM 

#重置锁文件
echo -n > $RESTART_LOCK
echo -n > $RESTART_REASON

exit 0

