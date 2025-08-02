import numpy as np
import os
from pathlib import Path
from PIL import Image

import matplotlib
matplotlib.use("tkagg")
import matplotlib.pyplot as plt

minx = 162
miny = 1114
maxx = 318
maxy = 1268


ddata = Path(r"F:\Pictures\feet\processed")
ddest = Path(r"F:\Pictures\feet\scaled")

image_paths = [ddata / x for x in os.listdir(ddata)]
images = []

for image_path in image_paths:
    img = Image.open(image_path)
    image = np.array(img)
    sample = image[minx : maxx, miny: maxy,  :]
    avg = sample.mean(axis=(0,1))
    scaled_image = (image / avg) * (0.6*255)
    scaled_image = np.clip(scaled_image, 0, 255)
    img = Image.fromarray(scaled_image.astype(np.uint8))
    images.append(img)
    img.save(ddest / image_path.name)


images[0].save(ddest / "array.gif", save_all=True, append_images=images[1:], duration=300, loop=0)