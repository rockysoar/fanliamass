#!/bin/bash

# project dir
PROJ="$1"
OUTPUTSTYLE="$2"

if [[ '' == $PROJ || ! -d $PROJ || 'h' == ${PROJ:0:1} ]]; then
    echo "Usage: $0 dir [style]"
    echo "    dir: project dir"
    echo "    style: output format, 1(default): output 'grep -n'. 2: aggregate and output"
    exit 255
fi

# 匹配：
# 1：特定标签中的http资源，
# 2：或ThinkPHP模板写法中加载变量而变量未进行fsdk_fit_scheme处理的资源
UNSAFE_IMG='<img.*?src=("|\0x27)?(http:|\{\$.+(?<!\|fsdk_fit_scheme))'
UNSAFE_LINK='<link.*?href=("|\0x27)?(http:|\{\$.+(?<!\|fsdk_fit_scheme))'
UNSAFE_SCRIPT='<script*?src=("|\0x27)?(http:|\{\$.+(?<!\|fsdk_fit_scheme))'

function func_grep () {
    grep -nE "$1" \
        --include=*.php --include=*.htm --include=*.html --include=*.html5 \
        --exclude-dir=.svn \
        -r $2
        #--color=auto \
}

if [[ $OUTPUTSTYLE = "" || $OUTPUTSTYLE = "1" ]]; then
    func_grep "($UNSAFE_IMG|$UNSAFE_LINK|$UNSAFE_SCRIPT)" "$PROJ"
elif [[ $OUTPUTSTYLE != "1" ]]; then
    func_grep "($UNSAFE_IMG|$UNSAFE_LINK|$UNSAFE_SCRIPT)" "$PROJ" | \
        awk -F':' '{
            if(!($1 in arr)) {
                arr[$1] = 1
                print "==== "$1" ===="
            }
            $1 = ""
            print $0
        }'
fi


