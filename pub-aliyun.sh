#! /bin/bash

ENV="$1"
PROJS=("${@:1}")
WEBROOT='/tmp'
SSHPWD=${ALIYUN_SSH_PWD:-''}

GITREPO='git@gitea.office.51fanli.com:phpweb'

COL_RED='\033[0;31m'
COL_NO='\033[0;0m'

# Tells bash that it should exit the script if any statement returns a non-true return value
set -e

err() {
    echo -e "[${COL_RED}error${COL_NO}] ${1}"
    exit 255
}

log() { 
    echo -e "${COL_NO}[info] ${1}" 
}

if [[ -z "$1" ]]; then
    echo "Usage: $0 projectName...
       su tuangouadmin 
       step 1: export ALIYUN_SSH_PWD='YOUR ALIYUN SSH PASSWORD'.
       step 2: bash $0 fsdk fans."
    echo 
fi

if [[ 'tuangouadmin' != `whoami` ]]; then
    err 'you should execute with tuangouadmin.'
fi

if [[ -z "$SSHPWD" ]]; then
    err '`export ALIYUN_SSH_PWD="YOUR ALIYUN SSH PASSWORD"` first.'
fi

if [[ ! -d "$WEBROOT" ]]; then
    mkdir -p "$WEBROOT"
fi

pull_from_git() {
    local proj="$1"
    log "git clone OR git pull from remote: $proj."

    if [[ ! -d "$WEBROOT/$proj/.git" ]]; then
        rm -rf "$WEBROOT/$proj" && mkdir "$WEBROOT/$proj"
        git clone --progress -v -b master --single-branch "$GITREPO/${proj}.git" "$WEBROOT/$proj"
    elif [[ ! -d "$WEBROOT/$proj" ]]; then
        mkdir "$WEBROOT/$proj"
        git clone --progress -v -b master --single-branch "$GITREPO/${proj}.git" "$WEBROOT/$proj"
    else
        (cd "$WEBROOT/$proj" && git pull origin master)
    fi

    (cd "$WEBROOT/$proj" && git reset --hard && git checkout master)
}

rsyn_source() {
    local proj="$1"
    rsync -av --max-size=2M --delete --delete-during \
        -e "sshpass -p ${SSHPWD} ssh -o StrictHostKeyChecking=no -l tuangouadmin" \
        --exclude='.env' --exclude='.idel' --exclude='.git*' --exclude='.svn*' --exclude='/Conf' --exclude='/config' --exclude='Runtime' --exclude='/templates_compiled' \
        "$WEBROOT/$proj/" "tuangouadmin@47.93.253.116:$WEBROOT/$proj/"
}

cache_clean() {
    local proj="$1"
    local rmlist=""

    case $proj in
    fsdk)
        rmlist="templates_compiled/"
        ;;
    daishu|daishu-app)
        rmlist="*/Runtime/"
        ;;
    esac

    if [[ -z "$rmlist" ]]; then
        return
    fi

    log "remove ${WEBROOT}/${proj}/$rmlist"
    sshpass -p "${SSHPWD}" ssh -o StrictHostKeyChecking=no tuangouadmin@47.93.253.116 "rm -rf ${WEBROOT}/${proj}/$rmlist"
}

IFS=$" \t\n"
for proj in "${PROJS[@]}"; do
    log "publishing ${proj}..."

    pull_from_git $proj

    if [[ ! -d "$WEBROOT/$proj" ]]; then
        err "project NOT exists: $WEBROOT/$proj."
    fi

    # copy symlinks as symlinks
    rsyn_source "$proj"

    cache_clean "$proj"

    log "publish ${proj} complete."
done

