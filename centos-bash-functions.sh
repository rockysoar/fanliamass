#! /bin/bash
# put this file in /etc/profile.d/
# run '. /etc/profile.d/centos-bash-functions.sh' to make this defination work.

alias ..='cd ../'
alias ...='cd ../../'
alias .2='cd ../../'
alias .3='cd ../../../'
alias mkdir='mkdir -pv'

alias ping='ping -c 100 -s.2'
alias netstat.l='netstat -tulanp'
alias curl.debug='curl -Iv'

alias df='df -Tha --total'
alias du='du -ach | sort -h'
alias free='free -mh'
alias ps='ps auxf'
alias ip.self="curl http://ipecho.net/plain; echo"

alias ssh.pub='ssh junhua.zhang@192.168.0.xx'
alias git.lazy="/usr/local/lazygit"
alias vi.vhost='_(){ VHOSTROOT="/usr/local/apache2/conf/vhosts"; echo "$VHOSTROOT/$1"; usleep 1000000; vim "$VHOSTROOT/${1}_vhost.conf"; }; _'

function g.code {
    grep -Pn --color=auto --include=*.{sh,py,php,js,css,html,c} --exclude=.{svn,gitignore} --exclude-dir=Runtime "$1" $2 $3 $4
}

if [[ ! -z $(which git) ]]; then
    git config --global alias.co checkout
    git config --global alias.st status
    git config --global alias.ci commit 
    git config --global alias.di diff
fi

alias vi.php5='vi /usr/local/php5/lib/php-safe.ini'
alias vi.php7='vi /usr/local/php7/lib/php.ini'
alias vi.httpd='vi /usr/local/apache2/conf/httpd.conf'
alias cd.php5='cd /usr/local/php5'
alias cd.php7='cd /usr/local/php7'
alias cd.apache='cd /usr/local/apache2/conf'

