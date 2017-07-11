#! /bin/bash
IFS="\n"

IPT="$1"
COLSEP="$2"
COL="$3"
TMPDIR="$IPT-tmp"
DEBUG="$4"

# help
if [[ '-h' == "$1" || $# -lt 3 ]]; then
    echo 'Usage: ./redis_key_stat.sh file column-separator column [debug 1|2]'
    exit 2
fi

if [[ ! -f "$IPT" ]]; then
    echo "file NOT exists: '$IPT'"
    exit 1
fi

STAT_BYTE=$(stat -c%s $IPT)
STAT_LINE=$(wc -l $IPT | awk '{print $1}')

# Task Infomation
echo "File: $IPT"
echo "Size: $STAT_BYTE bytes"
echo "Line: $STAT_LINE"
echo "Date: $(date -R)"
echo;

# temporary dir
[[ -d "$IPT-tmp" ]] || mkdir "./$IPT-tmp"
rm ./"$IPT-tmp"/*

# split large file 
split -a 2 -l 100000 "$IPT" '_x' && mv _x* "./$TMPDIR/"

echo "large file split into smaller files(10w lines per file):"
for i in ./$TMPDIR/_x*; do echo '  '$i; done

cd ./$TMPDIR

# load FsdkRal template
IFS=$'\n'
PREG_RAL='xxxxxxxx'
for i in $(grep -P 'key.*?=>.*$' -r "/usr/local/webdata/fsdk/templates/FsdkRal/app" \
    --include="ral_*.tpl.php" --include="sub_*.tpl.php"); do
    PREG_RAL+='|'
    PREG_RAL+=$(echo $i | awk -F">|," '{print $2}' | tr -d "' \"")
done
PREG_RAL=$(echo $PREG_RAL | \
    sed -r 's/\{[0-9a-zA-Z_]*:num\}/[0-9]*/g' | \
    sed -r 's/\{[0-9a-zA-Z_]*:str\}/[0-9a-zA-Z_]*/g')

IFS=$'\n'
for subfile in _x*; do
    echo
    echo "  start ./$TMPDIR/${subfile}..."
    echo -n > "_$subfile"

    if [[ ! '' == "$DEBUG" ]]; then
        echo "debug: split last 20 lines by '$COLSEP' and output column $COL"
    fi

    if [[ '1' == "$DEBUG" ]]; then
        tail -20 "$subfile" | awk -F"$COLSEP" '{print $'$COL'}'
        exit;
    elif [[ '2' == "$DEBUG" ]]; then
        tail -20 "$subfile" | awk -F"$COLSEP" '{print $'$COL'}' | sed -r -e 's/:[0-9][0-9][0-9]+/:\\d+/g'
        exit;
    else
        preg='xxxxxxx'
        IFS=$'\n'
        for line in $(cat $subfile | awk -F"$COLSEP" '{print $'$COL'}' | sort); do
            if [[ $line =~ $preg ]]; then
                echo $preg >> "_$subfile"; continue
            fi

            IFS=$'|'
            for preg in $PREG_RAL; do
                if [[ $line =~ $preg ]]; then
                    echo $preg >> "_$subfile"; break
                fi
            done
        done
    fi
    echo "  end ./$TMPDIR/$subfile"
done

echo -n > ./stat
for file in __x*; do
    uniq -c $file >> ./stat
done

awk -F' ' '{keys[$2] += $1} END{
    for (i in keys){
        printf("%7d %s\n", keys[i], i)
    }
}' ./stat > ./_stat

sort -rn ./_stat > ../"${IPT}.stat"
echo
echo "all stat over: ./${IPT}.stat"

