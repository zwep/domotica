#!/bin/bash

cur_date=$(date)
printf "$cur_date"

cd /home/git/code/domotica
/usr/bin/git pull origin master