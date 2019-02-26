#! /bin/bash

set -e

ENV="$1"
PROJ="$2"

PROJBASE="/usr/local/publish/${ENV}/webdata/"
CNFPATH=""

info() {
    echo "[info] ${1}."
}

err() {
    echo "[error] ${1}."
    if [[ 0 -eq "$2" ]]; then 
        exit 0
    fi
    exit 255
}

if [[ -f "${PROJBASE}/${PROJ}/${PROJ}/Conf/config.php" ]]; then
    CNFPATH="${PROJBASE}/${PROJ}/${PROJ}/Conf/config.php"
fi

case "$PROJ" in
    fans|XXX):
        CNFPATH="/usr/local/publish/configs/${PROJ}/${ENV}/Conf/config.php"
        break
esac

# debug
# CNFPATH='/usr/local/workdata/master/mobile/Conf/config.php'

if [[ ! -f "$CNFPATH" ]]; then
    err "no ${PROJ}/Conf/config.php file found" 0
fi

info "Config path for 'CSS_JS_TIME': ${CNFPATH}"

# 'CSS_JS_TIME' => '201902254_6991249989',
currentTS=$(sed -rn '/[\x27|"]CSS_JS_TIME[\x27|"]\s*=>\s*\w*/p' "$CNFPATH")
if [[ -z "$currentTS" ]]; then
    err "skip ${CNFPATH}" 0
fi

# 201902254_6991249989
currentTS=$(echo "$currentTS" | sed -r 's/\s|\x27|CSS_JS_TIME|=>|,//g')
currentTS_="$currentTS"
currentTS=(${currentTS//_/ })

if [[ "${currentTS[0]}" != $(date '+%Y%m%d') ]]; then
    currentTS[0]=$(date '+%Y%m%d')
    currentTS[1]="11${RANDOM}00"
fi
currentTS[1]=$((currentTS[1] + 1))

currentTS="${currentTS[0]}_${currentTS[1]}"
sed -in "s/$currentTS_/$currentTS/" "$CNFPATH"

info "new timestamp: $currentTS"

