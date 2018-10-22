#!/bin/bash

DATE=$(date +"%Y_%m_%d")
MAIN_PATH_TO_DATA="$HOME/data/nvidia/${DATE}_rawfile.txt"
TIME=$(date +"%H:%M")

echo >> $MAIN_PATH_TO_DATA
echo TIMESTAMP: $TIME >> $MAIN_PATH_TO_DATA
nvidia-smi >> $MAIN_PATH_TO_DATA