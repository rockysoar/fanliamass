#! /bin/bash

alias ..='cd ..'
alias ...='cd ../..'
alias ssh.pub='ssh junhua.zhang@192.168.0.246'
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

