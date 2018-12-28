#!/bin/bash

cur_date=$(date)
printf "$cur_date"

/usr/local/bin/pip3 install git+https://github.com/zwep/zwep.git --upgrade
