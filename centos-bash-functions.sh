#! /bin/bash

alias ..='cd ..'
alias ...='cd ../..'

function g.code {
    grep -Pn --color=auto --include=*.{sh,py,php,js,css,html,c} --exclude=.{svn,gitignore} "$1" $2 $3
}

