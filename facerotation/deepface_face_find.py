
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

- Use the .find() function to test which parameters can say that all images are of the same person


This appeared to be the best face detector...? Although... I dont know anything about false positives yet...
    'SFace', 'ArcFace', 'euclidean'

Here it is important to note that the following tresholds are used. They differ per model and metric

 thresholds = {
        # "VGG-Face": {"cosine": 0.40, "euclidean": 0.60, "euclidean_l2": 0.86}, # 2622d
        "VGG-Face": {
            "cosine": 0.68,
            "euclidean": 1.17,
            "euclidean_l2": 1.17,
        },  # 4096d - tuned with LFW
        "Facenet": {"cosine": 0.40, "euclidean": 10, "euclidean_l2": 0.80},
        "Facenet512": {"cosine": 0.30, "euclidean": 23.56, "euclidean_l2": 1.04},
        "ArcFace": {"cosine": 0.68, "euclidean": 4.15, "euclidean_l2": 1.13},
        "Dlib": {"cosine": 0.07, "euclidean": 0.6, "euclidean_l2": 0.4},
        "SFace": {"cosine": 0.593, "euclidean": 10.734, "euclidean_l2": 1.055},
        "OpenFace": {"cosine": 0.10, "euclidean": 0.55, "euclidean_l2": 0.55},
        "DeepFace": {"cosine": 0.23, "euclidean": 64, "euclidean_l2": 0.64},
        "DeepID": {"cosine": 0.015, "euclidean": 45, "euclidean_l2": 0.17},
        "GhostFaceNet": {"cosine": 0.65, "euclidean": 35.71, "euclidean_l2": 1.10},
    }
    
"""

storage_dir = os.path.expanduser("~/storage_deepface")
model_list = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace", "SFace", "GhostFaceNet"]
metric_list = ['cosine', 'euclidean', 'euclidean_l2']
normalize_list = ["base", "raw", "Facenet", "Facenet2018", "VGGFace", "VGGFace2", "ArcFace"]

MAX_IMAGES = 27
path1 = '/home/sharreve/local_scratch/plain_data/me/transformed_c21.jpg'
path2 = '/home/sharreve/local_scratch/plain_data/me/transformed_c25.jpg'
path3 = '/home/sharreve/local_scratch/plain_data/me/c25.jpeg'

"""
Explain
"""

sel_detector = 'retinaface'  # This is based on the deepface_face_detection.py script
result_dict = {}
# Loop over all interesting parameters
for i_model in model_list:
    result_dict.setdefault(i_model, {})
    for i_normalizer in normalize_list:
        result_dict[i_model].setdefault(i_normalizer, {})
        for i_metric in metric_list:
            result_dict[i_model][i_normalizer].setdefault(i_metric, None)
            try:
                dfs = DeepFace.find(img_path=path3, db_path=os.path.dirname(path3),
                                    model_name=i_model,
                                    detector_backend=sel_detector,
                                    normalization=i_normalizer,
                                    distance_metric=i_metric
                                    )
                result_dict[i_model][i_normalizer][i_metric] = dfs
            except ValueError as e:
                print(" ====== ", i_model, i_normalizer, i_metric, " ====== ")
                print(e)

str_distance = 30
count_results = []
# Now I can check per type the distance to the given image (c21)
for model_name, normalizer_dict in result_dict.items():
    for normalizer, metric_dict in normalizer_dict.items():
        for metric, dfs_obj in metric_dict.items():
            print(model_name, normalizer, metric, ' ' * (str_distance - len(model_name) - len(normalizer) - len(metric)), len(dfs_obj[0]))
            count_results.append((len(dfs_obj[0]), model_name, normalizer, metric))
            dfs = dfs_obj[0].sort_values('distance')
            for i, iterrow in dfs.iterrows():
                basename = os.path.basename(iterrow['identity'])
                print('\t', basename, ' ' * (str_distance - len(basename)), iterrow['distance'])

# Plot the counts of the top10 models
for ii in sorted([x for x in count_results if x[-1] == 'euclidean'], key=lambda x: x[0])[-10:]:
    print(ii)

for ii in sorted([x for x in count_results if x[-1] == 'euclidean_l2'], key=lambda x: x[0])[-10:]:
    print(ii)

for ii in sorted([x for x in count_results if x[-1] == 'cosine'], key=lambda x: x[0])[-10:]:
    print(ii)