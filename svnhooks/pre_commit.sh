#!/bin/bash  
REPOS="$1"  
TXN="$2"  

# Make sure that the log message contains some text.  
SVNLOOK=/usr/bin/svnlook  
PY=/usr/bin/python

MSG=$($SVNLOOK log "$REPOS")  
ERR=$($PY inspector_message.py "$MSG")
if [ $? -ne 0 ]; then
    echo "$ERR" >&2
    exit 1
fi

while read changedfile; do
    ERR=$($PY inspector_encoding.py "$REPOS" "$changedfile")
    if [ $? -ne 0 ]; then
        echo "$ERR" >&2
        exit 1
    fi
done <<< $($SVNLOOK changed "$REPOS")

while read changedline; do
    echo 1
    #$PY inspector_pear_cs.py "$REPOS"
done <<< $($SVNLOOK diff "$REPOS")

