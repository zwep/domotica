
from deepface.modules import detection
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

- Use the .find() function to test which parameters can detect faces 
- Verify with the .extract_faces() function detectors can detect faces
- Verify the extracted faces using the top 3 detectors (based on how many faces they recognize)

Conclusion is that retinaface is a great detector

"""


storage_dir = os.path.expanduser("~/storage_deepface")
model_list = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace", "SFace", "GhostFaceNet"]
metric_list = ['cosine', 'euclidean', 'euclidean_l2']
detector_list = ['opencv', 'retinaface', 'mtcnn', 'ssd', 'dlib', 'mediapipe', 'yolov8']
normalize_list = ["base", "raw", "Facenet", "Facenet2018", "VGGFace", "VGGFace2", "ArcFace"]

MAX_IMAGES = 27
path1 = '/home/sharreve/local_scratch/plain_data/me/transformed_c21.jpg'
path2 = '/home/sharreve/local_scratch/plain_data/me/transformed_c25.jpg'

img1 = np.array(Image.open(path1))
img2 = np.array(Image.open(path2))

"""
The experiment below was used to check which model/detector/normalizer could find faces 
Then I found out that the function 'find' aims to "find" the given image in a database of images (with location "db_path")
The content of the database is based on the image directory I gave...

So although I did get a warning that a face wasnt found, it did more than I wanted.
From this I found that the following detectors didnt work well: opencv and dlib

The normalization and model used didnt affect face detection 
(later I noticed that the normalization step is not applied before face detection, 
 and the model is not used for detection only for comparison I believe)
"""

result = []
# Loop over all interesting parameters
for i_model in model_list:
    for i_detector in detector_list:
        for i_normalizer in normalize_list:
                try:
                    dfs = DeepFace.find(img_path=path1, db_path=os.path.dirname(path1),
                                        model_name=i_model,
                                        detector_backend=i_detector,
                                        normalization=i_normalizer
                                        )
                    setting_list = [i_model, i_detector, i_normalizer]
                    result.append(setting_list)
                except ValueError:
                    pass

collections.Counter([x[0] for x in result])

"""
To verify that specific backends dont work well, I want to do the detection again but then without the 'find' function
Here I only use detection and extract faces, which should be the core of the thing I want to check

When supplying only the image path (not the image itself) I obtained the following results:
For MID images:
Best detectors on full images: {'yolov8', 'mediapipe', 'retinaface'}
Best detectors on transformed images: {'yolov8', 'mediapipe', 'retinaface'}

For all images (bottom, mid, top):
Best detectors on full images: ...{'retinaface'}
Best detectors on transformed images: {'retinaface'}

When supplying the image itself (as an np.array) doesnt change the outcome.
Neither does it change when we normalize to 0 - 1 (min/max)
(This was tested on the transformed images to save time. I assume original images will produce the same result)
"""

#path1 = f'/home/sharreve/local_scratch/plain_data/me/c{i_pos}{i_img}.jpeg'
result_dict = {}
img_counter = 0
for i_pos in range(1, 4):
    for i_img in range(1, 10):
        img_counter += 1
        path1 = f'/home/sharreve/local_scratch/plain_data/me/transformed_c{i_pos}{i_img}.jpg'
        # img1 = np.array(Image.open(path1))
        # img1 = img1/ 256
        useful_detectors = []
        for i_detector in detector_list:
            try:
                img_objs = detection.extract_faces(
                    img_path=path1,
                    detector_backend=i_detector,
                    grayscale=False,
                    enforce_detection=True
                )
                useful_detectors.append(i_detector)
            except ValueError as e:
                print(f" ======  {i_detector} ====== ")
                print(e)
                pass
        result_dict[img_counter] = useful_detectors


for k, v in result_dict.items():
    print(k, len(v))


collections.Counter(list(itertools.chain(*result_dict.values())))
u = set.intersection(*[set(x) for x in list(result_dict.values())])
# Which model shows up over all the views
print(u)
# Show the count of success (of finding a face) per model
print(collections.Counter(list(itertools.chain(*result_dict.values()))))
# {'retinaface': 27, 'mediapipe': 26, 'yolov8': 26, 'mtcnn': 23, 'ssd': 20, 'dlib': 11, 'opencv': 10}

"""
Now I want to test the top 3 model (retinaface, mediapipe and yolov8)

Conclusion: retinaface is also a good face extractor (not only detector)
"""

from deepface.modules import detection
sel_detector_list = ['retinaface', 'mediapipe', 'yolov8']
result_dict = {}
img_counter = 0
# Collect all the resulting faces
for i_pos in range(1, 4):
    for i_img in range(1, 10):
        img_counter += 1
        path1 = f'/home/sharreve/local_scratch/plain_data/me/transformed_c{i_pos}{i_img}.jpg'
        img_obj_dict = {}
        for i_detector in sel_detector_list:
            try:
                img_objs = detection.extract_faces(
                    img_path=path1,
                    detector_backend=i_detector,
                    grayscale=False,
                    enforce_detection=True
                )
                img_obj_dict[i_detector] = img_objs
            except ValueError:
                pass
        result_dict[img_counter] = img_obj_dict

# Below are plotting the resulting faces
for i_img in range(1, MAX_IMAGES+1):
    fig, ax = plt.subplots(len(sel_detector_list))
    file_name = f'detect_face_{i_img}.jpg'
    for ii, i_detector in enumerate(sel_detector_list):
        ax[ii].set_title(i_detector)
        if i_detector in result_dict[i_img]:
            face_obj = result_dict[i_img][i_detector]
            # Iterate over all the found faces...
            for i_face in face_obj:
                ax[ii].imshow(i_face['face'][0])
        else:
            ax[ii].imshow(np.zeros((224, 224)))
    fig.savefig(os.path.join(storage_dir, file_name))
