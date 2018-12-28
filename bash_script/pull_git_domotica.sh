#!/bin/bash

cur_date=$(date)
printf "$cur_date"

CUR_DIR=$(pwd)
GIT_DIR="/home/git/code/domotica"
BASH_FILES="/home/git/code/domotica/bash_script/*"
BASH_DEST="/usr/local/bin/"

cd ${GIT_DIR}
/usr/bin/git pull origin master

for f in ${BASH_FILES}
do
    printf "\n Moving file: ${f}"
    \cp ${f} ${BASH_DEST}
done
printf "\n"

cd ${CUR_DIR}