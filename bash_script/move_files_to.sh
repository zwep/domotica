#!/bin/bash

FILES=/home/git/code/domotica/bash_script/*
DEST=/var/log/domotica

for f in ${FILES}
do
    printf "\n Moving file: ${f}"
    mv ${f} ${DEST}
done