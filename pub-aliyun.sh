#! /bin/bash

ENV="$1"
PROJS=("${@:2}")
CODEROOT='/tmp/git-source'
WEBROOT='/usr/local/webdata'
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
    echo "Usage: $0 [trunk|prod] projectName...
       step 1. su tuangouadmin 
       step 2. export ALIYUN_SSH_PWD='YOUR ALIYUN SSH PASSWORD'.
       step 3. \$bash $0 [trunk|prod] fsdk fans."
    echo 
fi

if [[ 'tuangouadmin' != `whoami` ]]; then
    err 'you should execute with tuangouadmin.'
fi

[ -d $CODEROOT ] || mkdir -p $CODEROOT

if [[ 'prod' != "$ENV" && 'trunk' != "$ENV" ]]; then
    err 'publish enviroment should be: prod OR trunk'
fi

if [[ -z "$PROJS" ]]; then
    err 'you should specify at least on project to publish'
fi

if [[ -z "$SSHPWD" ]]; then
    err '`export ALIYUN_SSH_PWD="YOUR ALIYUN SSH PASSWORD"` first.'
fi

if [[ ! -d "$WEBROOT" ]]; then
    mkdir -p "$WEBROOT"
fi

pull_from_git() {
    local proj="$1"
    log "git clone OR git pull from remote: $GITREPO/${proj}.git"

    local branch=""
    if [[ 'trunk' = $ENV ]]; then
        branch='develop'
    elif [[ 'prod' = $ENV ]]; then
        branch='master'
    fi

    if [[ ! -d "$CODEROOT/$proj/.git" ]]; then
        # git clone --progress -v -b "${branch}" --single-branch "$GITREPO/${proj}.git" "$CODEROOT/$proj"
        git clone --progress -v "$GITREPO/${proj}.git" "$CODEROOT/$proj"
    fi

    (cd "$CODEROOT/$proj" && git checkout "${branch}" && git fetch origin "${branch}" && git reset --hard origin/"${branch}")
}

get_pub_hosts() {
    case "$1" in
    prod)
        echo '47.93.253.116'
        ;;
    trunk)
        echo '47.93.253.116'
        ;;
    esac
}

rsyn_source() {
    local ipAddr="$1"
    local proj="$2"
    rsync -av --max-size=2M --delete --delete-during \
        -e "sshpass -p ${SSHPWD} ssh -o StrictHostKeyChecking=no -l tuangouadmin" \
        --exclude='.env' --exclude='.idel' --exclude='.git*' --exclude='.svn*' --exclude='/Conf' --exclude='/config' --exclude='Runtime' --exclude='/templates_compiled' \
        "$CODEROOT/$proj/" "tuangouadmin@$ipAddr:$WEBROOT/$proj/"
}

cache_clean() {
    local ipAddr="$1"
    local proj="$2"
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
        return 0
    fi

    log "remove remote ${WEBROOT}/${proj}/$rmlist"
    sshpass -p "${SSHPWD}" ssh -o StrictHostKeyChecking=no "tuangouadmin@$ipAddr" "rm -rf ${WEBROOT}/${proj}/$rmlist"
}

IFS=$" \t\n"
for proj in "${PROJS[@]}"; do
    log "publishing ${proj}..."

    pull_from_git $proj

    if [[ ! -d "$CODEROOT/$proj" ]]; then
        err "project NOT exists: $CODEROOT/$proj."
    fi

    targetHosts=$(get_pub_hosts "$ENV")
    # copy symlinks as symlinks
    rsyn_source "${targetHosts}" "$proj"

    cache_clean "${targetHosts}" "$proj"

    log "publish ${proj} complete."
done

