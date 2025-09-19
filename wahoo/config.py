from collections import deque
import cv2
import os
from pathlib import Path

"""
Store some constants about the game
"""


# BLE UUID for Cycling Power Measurement
# Overview of other UUIDs
# https://gist.github.com/sam016/4abe921b5a9ee27f67b3686910293026

# This shows how the data is encoded
# https://bitbucket.org/bluetooth-SIG/public/src/main/gss/
# This shows all the specifications
# https://btprodspecificationrefs.blob.core.windows.net/gatt-specification-supplement/GATT_Specification_Supplement.pdf

# This also helped me
# https://github.com/hbldh/bleak/discussions/1579
main_path = Path(r"F:\Documents\lenn")
ICON_PATH = main_path / "cycler_with_head.png"
ALP_IMG_PATH = main_path / "alpe_sat.jpg"
ALP_ROUTE_PATH = main_path / "route_alpe_sat.txt"
IMG_FOLDER = main_path / "images"
POWER_UUID = "00002a63-0000-1000-8000-00805f9b34fb"
BLE_DEVICE_ADDRESS = "C6:76:C5:B6:3C:14"


# BGR is the color coding
white_color = (255, 255, 255)
black_color = (0, 0, 0)
green_color = (13, 158, 13)
red_color = (13, 13, 158)
grey_color = (158, 158, 158)

paused = True
simulation = True
latest_power = 0
frame_index = 0
time_index = 0
difficulty_factor = 1
window_name = "Lenn's power extravaganza"

"""
Set up image loading...
"""

SLIDESHOW_IMG_PATHS = {i: [] for i in range(22)}
SLIDESHOW_IMG_PATHS.update({3: ["PICT0001", "PICT0002", "PICT0009"],
 7: ["PICT0011", "PICT0014"],
 12: ["DSC_0284"],
 16: ["HRF_2780"],
 18: ["f_ANS1205"],
19: ["f_ANS1158"]})
