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
UNSAFE_HTML_IMG='<img.+?src\s*=\s*("|\0x27)?(http:|\{\$.+(?<!\|fsdk_fit_scheme)\})'
UNSAFE_HTML_LINK='<link.+?href\s*=\s*("|\0x27)?(http:|\{\$.+(?<!\|fsdk_fit_scheme)\})'
UNSAFE_HTML_SCRIPT='<script.+?src\s*=\s*("|\0x27)?(http:|\{\$.+(?<!\|fsdk_fit_scheme)\})'
UNSAFE_CSS_BACKGROUND='background(-image)?\s*:.*?url\(("|\0x27)?(http:|\{\$.+(?<!\|fsdk_fit_scheme)\})'
# match "http://xxx" that not commented out
UNSAFE_JS_SOURCE='^(?!\s*(\/|\*)).*?("|\0x27)?http:\/\/'

function func_grep () {
   grep -nP "$UNSAFE_HTML_IMG|$UNSAFE_HTML_LINK|$UNSAFE_HTML_SCRIPT" --exclude-dir=.svn --include=*.php -r $1
   grep -nP "$UNSAFE_CSS_BACKGROUND" --exclude-dir=.svn --include=*.css -r $1
   grep -nP "$UNSAFE_JS_SOURCE|$UNSAFE_HTML_IMG|$UNSAFE_HTML_LINK|$UNSAFE_HTML_SCRIPT" --exclude-dir=.svn --include=*.js -r $1
   grep -nP "$UNSAFE_HTML_IMG|$UNSAFE_HTML_LINK|$UNSAFE_HTML_SCRIPT|$UNSAFE_CSS_BACKGROUND|$UNSAFE_JS_SOURCE" --exclude-dir=.svn --include=*.htm --include=*.html --include=*.html5 -r $1
}

if [[ $OUTPUTSTYLE = "" || $OUTPUTSTYLE = "1" ]]; then
    func_grep "$PROJ"
elif [[ $OUTPUTSTYLE != "1" ]]; then
    func_grep "$PROJ" | \
        gawk -F':' '{
            if(!($1 in arr)) {
                arr[$1] = 1
                print "==== "$1" ===="
            }
            for(i=2; i<NF; i++) {
                printf $i":"
            }
            print $NF
        }'
fi

