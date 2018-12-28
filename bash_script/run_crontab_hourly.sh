#!/bin/bash

cur_date=$(date)
printf "\n $cur_date"

. ${HOME}/.bash_profile

FILES=/home/git/code/domotica/crontab_calls/hourly/*

for f in ${FILES}
do
    printf "\n Processing ${f} file..."
    /usr/local/bin/python3 ${f}
done
