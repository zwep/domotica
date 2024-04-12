
from deepface.modules import detection, verification
import collections
import itertools
import matplotlib.pyplot as plt
from deepface import DeepFace
# oneDNN custom operations are on. You may see slightly different numerical results due to
# floating-point round-off errors from different computation orders.
# To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
from PIL import Image
import numpy as np
import os

"""

https://github.com/serengil/deepface

Using the repo above, we are going to do some experiments


Compare two images... with verify... However, I think this doesnt add much to the face_find function

So we will just use the "best" model we have found so far and simply re-do the experiment on all images...
Create a nice heatmap or something

We did it, yay (see test.png)

All values were within the margin

"""

storage_dir = os.path.expanduser("~/storage_deepface")
sel_model = "SFace"  # This is based on the deepface_face_find.py script
sel_metric = 'euclidean'  # This is based on the deepface_face_find.py script
sel_normalizer = "ArcFace"  # This is based on the deepface_face_find.py script
sel_detector = 'retinaface'  # This is based on the deepface_face_detection.py script
image_dir = '/home/sharreve/local_scratch/plain_data/me'

"""
Explain
"""

MAX_IMAGES = 27
distance_matrix = np.zeros((MAX_IMAGES, MAX_IMAGES))
# Loop over all interesting parameters
i_img_counter = -1
j_img_counter = -1
for i_pos in range(1, 4):
    for i_img in range(1, 10):
        i_img_counter += 1
        path1 = f'/home/sharreve/local_scratch/plain_data/me/transformed_c{i_pos}{i_img}.jpg'
        j_img_counter = -1
        for j_pos in range(1, 4):
            for j_img in range(1, 10):
                j_img_counter += 1
                print(i_img_counter, j_img_counter)
                path2 = f'/home/sharreve/local_scratch/plain_data/me/transformed_c{j_pos}{j_img}.jpg'
                dfs = DeepFace.verify(img1_path=path1,
                                      img2_path=path2,
                                      model_name=sel_model,
                                      detector_backend=sel_detector,
                                      normalization=sel_normalizer,
                                      distance_metric=sel_metric
                                      )
                d = dfs['distance']
                distance_matrix[i_img_counter, j_img_counter] = d

fig, ax = plt.subplots()
aximshow = ax.imshow(distance_matrix)
plt.colorbar(aximshow)
fig.savefig(os.path.expanduser("~/test.png"))