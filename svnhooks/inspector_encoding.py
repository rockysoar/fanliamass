# utf-8, not BOM, tab => space * 4, eol

# Make sure that all files to be committed are encoded in UTF-8.  
while read changeline;   
do  
  # Get just the file (not the add / update / etc. status).  
  file=${changeline:4}  
  # Only check source files.  
  if [[ $file == *.java || $file == *.xhtml || $file == *.css || $file == *.xml || $file == *.js ]] ; then  
    $SVNLOOK cat -t "$TXN" "$REPOS" "$file" | $ICONV -f UTF-8 -t UTF-8 -o /dev/null  
    if [ "${PIPESTATUS[1]}" != 0 ] ; then  
      echo "Only UTF-8 files can be committed ("$file")" 1>&2  
      exit 1  
    fi  
  fi  
done < <($SVNLOOK changed -t "$TXN" "$REPOS")  

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
