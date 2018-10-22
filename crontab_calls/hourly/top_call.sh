#!/bin/bash

DATE=$(date +"%Y_%m_%d")
MAIN_PATH_TO_DATA="$HOME/data/top/${DATE}_rawfile.txt"
TIME=$(date +"%H:%M")

echo >> $MAIN_PATH_TO_DATA
echo TIMESTAMP: $TIME >> $MAIN_PATH_TO_DATA
top -bin 1 | grep -E "^ |^[0-9]" >> $MAIN_PATH_TO_DATA