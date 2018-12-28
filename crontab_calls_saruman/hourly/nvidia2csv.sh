#!/bin/bash

# scp -r seb@saruman.bmt.tue.nl:/home/seb/data/nvidia/ ~/data/
DATE=$(date +"%Y_%m_%d")
# MAIN_PATH_TO_DATA="$HOME/data/nvidia_rawtext/${DATE}_rawfile.txt"
MAIN_PATH_TO_DATA="$HOME/data/nvidia"
# python nvidia_rawtext.py -i $MAIN_PATH_TO_DATA
python nvidia_rawtext.py -i $MAIN_PATH_TO_DATA