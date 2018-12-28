#!/bin/bash

cur_date=$(date)
printf "$cur_date"

CUR_DIR=$(pwd)
cd /home/git/code/domotica
/usr/bin/git pull origin master
cd ${CUR_DIR}