#!/bin/bash

FILES=/home/git/code/domotica/bash_script/*
DEST=/usr/local/bin/

for f in ${FILES}
do
    printf "\n Moving file: ${f}"
    \cp ${f} ${DEST}
done