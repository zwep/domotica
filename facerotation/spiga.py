import os
import cv2
import pkg_resources
from PIL import Image
import numpy as np
# My libs
import spiga.demo.analyze.extract.spiga_processor as pr_spiga
from spiga.demo.analyze.analyzer import VideoAnalyzer
from spiga.demo.visualize.viewer import Viewer
from retinaface import RetinaFace

import matplotlib.pyplot as plt

# Initialize face tracker
# faces_tracker = tr.get_tracker(tracker)
# faces_tracker.detector.set_input_shape(capture.get(4), capture.get(3))
# Initialize processors
spiga_dataset = '300wpublic'
processor = pr_spiga.SPIGAProcessor(dataset=spiga_dataset)
tracked_obj = []
path1 = '/home/bme001/20184098/data/facerotation/mid/c25.jpeg'
frame = Image.open(path1)
frame_array = np.array(frame)

resp = RetinaFace.detect_faces(path1)
x0, y0, x1, y1 = resp['face_1']['facial_area']

bboxes = [[x0, y0, x1-x0, y1-y0]]
batch_crops, crop_bboxes = processor.processor.pretreat(frame_array, bboxes)
outputs = processor.processor.net_forward(batch_crops)
features = processor.processor.postreatment(outputs, crop_bboxes, bboxes)
#
fig, ax = plt.subplots()
ax.imshow(frame_array)
fig.savefig(os.path.expanduser("~/test.png"))

for ilandmark in features['landmarks'][0]:
    _ = ax.scatter(*ilandmark, c='r')

fig.savefig(os.path.expanduser("~/test2.png"))
