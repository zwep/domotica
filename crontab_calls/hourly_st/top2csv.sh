#!/bin/bash

# scp -r seb@saruman.bmt.tue.nl:/home/seb/data/top/ ~/data/
DATE=$(date +"%Y_%m_%d")
# MAIN_PATH_TO_DATA="$HOME/data/nvidia_rawtext/${DATE}_rawfile.txt"
MAIN_PATH_TO_DATA="$HOME/data/top"
# python nvidia_rawtext.py -i $MAIN_PATH_TO_DATA
python top_rawtext.py -i $MAIN_PATH_TO_DATA