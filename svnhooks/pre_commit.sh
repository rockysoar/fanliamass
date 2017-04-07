#!/bin/bash  
REPOS="$1"  
TXN="$2"  

# Make sure that the log message contains some text.  
SVNLOOK=/usr/bin/svnlook  
PY=/usr/bin/python

MSG=$($SVNLOOK log -t "$TXN" "$REPOS")  
$PY inspector_message.py "$MSG"

while read changedfile; do
    $PY inspector_syntax.py "$changedfile"
    
    $PY inspector_encoding.py "$changedfile"
done <<< $($SVNLOOK changed -t "$TXN" "$REPOS")

while read changedline; do
    $PY inspector_pear_cs.py "$TXN" "$REPOS"
done <<< $($SVNLOOK diff -t "$TXN" "$REPOS")

