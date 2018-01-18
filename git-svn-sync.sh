#! /bin/bash
repoSvn="svn://192.168.0.178/flip-notify/release"
repoGit="git@192.168.75.114:master/flip-notify.git"
repoGitLocal="/var/svn-git-exchange/flip-notify.git"

# switch workspace to git
if [[ ! -d $repoGitLocal ]]; then
    mkdir $repoGitLocal
fi
cd $repoGitLocal
chdir $repoGitLocal

if [[ ! -f ./svn.cursor ]]; then
    echo 2389 > ./svn.cursor
fi

svnRev=$((1+`cat ./svn.cursor`)
git2svnRev=2389

# fetch one commit from svn
svn log -r$svnRev:HEAD -l 1 $repoSvn > ./svn.log

parse revision number
svnRev=$(sed -n '2p' ./svn.log | awk -F'|' '{gsub(/ /, "", $1); print substring($1, 2)}')
# parse username
svnName=$(sed -n '2p' ./svn.log | awk -F'|' '{gsub(/ /, "", $2); print $2}')
# parse message
svnMsg=$(head -n -2 ./svn.log | tail -n +4)

if [[ /--sync from git--/ ~ $svnMsg ]]; then
    echo $svnRev > ./svn.cursor
    exit 0
fi

svn diff -c$svnRev $repoSvn > ./svn.patch
patch -p0 -t --dry-run < ./svn.patch
if [[ 0 -nq $? ]]; then
    mail -s "$repoGitLocal patch failed!" junhua.zhang@fanli.com
    exit 1
fi

rm ./svn.log ./svn.patch ./svn.cursor
sleep 0.2

git commit -a -m "--sync from svn $svnRev--\n$svnMsg"

# log the current successed revision number
echo $svnRev > ./svn.cursor

git push

