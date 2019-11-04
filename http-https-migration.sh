#!/bin/bash

# project dir
PROJ="$1"
CTX="$2"
OUTPUTSTYLE="$3"

if [[ '' == $PROJ || ! -d $PROJ || 'h' == ${PROJ:0:1} ]]; then
    echo "Usage: $0 dir [context] [output style]
    dir: project dir
    context: 
        af:  search anchor and form
        src(default): search resource
    output style: 
        1(default), output like 'grep -Pn \"perl-regex\"'. 
        2: aggregated by file name."
    exit 255
fi

# 匹配：
# 1：特定标签中的http资源，
# 2：或ThinkPHP模板写法中加载变量而变量未进行fsdk_fit_scheme处理的资源
UNSAFE_HTML_IMG='<img.+?(src|data-original)\s*=\s*("|\0x27)?(http:|\{\$[^}]+(?<!\|fsdk_fit_scheme)\})'
UNSAFE_HTML_LINK='<link.+?href\s*=\s*("|\0x27)?(http:|\{\$[^}]+(?<!\|fsdk_fit_scheme)\})'
UNSAFE_HTML_SCRIPT='<script.+?src\s*=\s*("|\0x27)?(http:|\{\$[^}]+(?<!\|fsdk_fit_scheme)\})'
UNSAFE_CSS_BACKGROUND='background(-image)?\s*:.*?url\(("|\0x27)?http:\/\/'
# match "http://xxx" that not commented out
UNSAFE_JS_SOURCE='^(?!\s*(\/|\*)).*?("|\0x27)?http:\/\/'

# switch http to https step by step, switch passport.fanli.com first
UNSAFE_HTML_FORM='<form.+?action\s*=\s*("|\0x27)?http:\/\/\w+\.(51)?fanli.com\/'
UNSAFE_HTML_ANCHOR='<a.+?href\s*=\s*("|\0x27)?http:\/\/\w+\.(51)?fanli.com\/'

function func_regex_grep () {
   if [[ 'af' == "$CTX" ]]; then
       grep -nP "$UNSAFE_HTML_ANCHOR|$UNSAFE_HTML_FORM" --exclude-dir=.svn --exclude-dir=Runtime --include=*.htm --include=*.html --include=*.html5 -r $PROJ
   elif [[ -z "$CTX" || 'src' == "$CTX" ]]; then
       grep -nP "$UNSAFE_HTML_IMG|$UNSAFE_HTML_LINK|$UNSAFE_HTML_SCRIPT" --exclude-dir=.svn --exclude-dir=Runtime --include=*.php -r $PROJ
       grep -nP "$UNSAFE_CSS_BACKGROUND" --exclude-dir=.svn --exclude-dir=Runtime --include=*.css -r $PROJ
       #grep -nP "$UNSAFE_JS_SOURCE|$UNSAFE_HTML_IMG|$UNSAFE_HTML_LINK|$UNSAFE_HTML_SCRIPT" --exclude-dir=.svn --exclude-dir=Runtime --include=*.js -r $PROJ
       grep -nP "$UNSAFE_HTML_IMG|$UNSAFE_HTML_LINK|$UNSAFE_HTML_SCRIPT|$UNSAFE_CSS_BACKGROUND" --exclude-dir=.svn --exclude-dir=Runtime --include=*.htm --include=*.html --include=*.html5 -r $PROJ
   fi
}

if [[ $OUTPUTSTYLE = "" || $OUTPUTSTYLE = "1" ]]; then
    func_regex_grep
elif [[ $OUTPUTSTYLE != "1" ]]; then
    func_regex_grep | \
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

