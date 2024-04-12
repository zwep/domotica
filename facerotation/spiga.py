import os.path

import spiga.demo.analyze.extract.spiga_processor as pr_spiga

spiga_dataset = '300wpublic'
processor = pr_spiga.SPIGAProcessor(dataset=spiga_dataset)

from retinaface import RetinaFace
import matplotlib.pyplot as plt
faces = RetinaFace.extract_faces(img_path = "/home/bme001/20184098/data/facerotation/mid/c21.jpeg", align = False)
fig, ax = plt.subplots()
for face in faces:
  ax.imshow(face)

fig.savefig(os.path.expanduser("~/test.png"))

detector = RetinaFace.detect_faces(img_path = "/home/bme001/20184098/data/facerotation/mid/c21.jpeg")

