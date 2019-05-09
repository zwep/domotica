#!/bin/bash

# scp -r seb@saruman.bmt.tue.nl:/home/seb/data/nvidia/2019_05* C:\Users\20184098\Documents\data\nvidia
DATE=$(date +"%Y_%m_%d")
# MAIN_PATH_TO_DATA="$HOME/data/nvidia_rawtext/${DATE}_rawfile.txt"
MAIN_PATH_TO_DATA="$HOME/data/nvidia"
# python nvidia_rawtext.py -i $MAIN_PATH_TO_DATA
python nvidia_rawtext.py -i $MAIN_PATH_TO_DATA