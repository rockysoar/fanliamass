#! /bin/bash

ENV="$1"
PROJS=("${@:1}")
WEBROOT='/usr/local/webdata'
SSHPWD=${ALIYUN_SSH_PWD:-''}

COL_RED='\033[0;31m'
COL_NO='\033[0;0m'

if [[ -z "$1" ]]; then
    echo "Usage: $0 projectName...
       step 1: export ALIYUN_SSH_PWD='YOUR ALIYUN SSH PASSWORD'.
       step 2: bash $0 fsdk fans."
    echo 
fi

err() {
    echo -e "[${COL_RED}error${COL_NO}] ${1}"
    exit 255
}

log() { 
    echo -e "[info] ${1}" 
}

if [[ -z "$SSHPWD" ]]; then
    err '`export ALIYUN_SSH_PWD="YOUR ALIYUN SSH PASSWORD"` first.'
fi

IFS=$" \t\n"
for proj in "${PROJS[@]}"; do
    log "publishing ${proj}..."

    if [[ ! -d "$WEBROOT/$proj" ]]; then
        err "project NOT exists: $WEBROOT/$proj."
    fi

    # copy symlinks as symlinks
    rsync -av --max-size=2M --delete --delete-during \
        -e "sshpass -p ${SSHPWD} ssh -o StrictHostKeyChecking=no -l tuangouadmin" \
        --exclude='.env' --exclude='.idel' --exclude='.git*' --exclude='.svn*' --exclude='Conf' --exclude='config' --exclude='Runtime' \
        "$WEBROOT/$proj" "tuangouadmin@47.93.253.116:$WEBROOT/$proj"

    log "publish ${proj} complete."
done

