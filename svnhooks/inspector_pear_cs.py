# tab => space * 4, eol

import sys  
ignore = True  
SUFFIXES = [ ".java", ".css", ".xhtml", ".js", ".xml", ".properties" ]  
filename = None  
for ln in sys.stdin:  
    if ignore and ln.startswith("+++ "):  
        filename = ln[4:ln.find("\t")].strip()  
        ignore = not reduce(lambda x, y: x or y, map(lambda x: filename.endswith(x), SUFFIXES))  
    elif not ignore:  
        if ln.startswith("+"):  
           if ln.count("\t") > 0:  
              sys.stderr.write("\n*** Transaction blocked, %s contains tab character:\n\n%s" % (filename, ln))  
              sys.exit(1)  
        if not (ln.startswith("@") or \  
           ln.startswith("-") or \  
           ln.startswith("+") or \  
           ln.startswith(" ")):  
           ignore = True  
sys.exit(0)  


# Check files for svn:eol-style property  
# Exit on all errors.  
set -e  
EOL_STYLE="LF"  
echo "`$SVNLOOK changed -t "$TXN" "$REPOS"`" | while read REPOS_PATH  
do  
 if [[ $REPOS_PATH =~ A[[:blank:]]{3}(.*)\.(java|css|properties|xhtml|xml|js) ]]  
 then  
  if [ ${#BASH_REMATCH[*]} -ge 2 ]  
    then  
  FILENAME=${BASH_REMATCH[1]}.${BASH_REMATCH[2]};  
  # Make sure every file has the right svn:eol-style property set  
   if [ $EOL_STYLE != "`$SVNLOOK propget -t \"$TXN\" \"$REPOS\" svn:eol-style \"$FILENAME\" 2> /dev/null`" ]  
    then  
    ERROR=1;  
      echo "svn ps svn:eol-style $EOL_STYLE \"$FILENAME\"" >&2  
   fi  
  fi  
 fi  
 test -z $ERROR || (echo "Please execute above commands to correct svn property settings. EOL Style LF must be used!" >& 2; exit 1)  
done 
