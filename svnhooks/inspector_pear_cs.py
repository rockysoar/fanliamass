
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
