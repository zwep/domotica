import os
import numpy as np
import harreveltools.helper.file_handeling as hfile
import harreveltools.helper.plot as hplot
import skimage.transform as sktransform
from PIL import Image

"""

We are testing the following github repo

https://github.com/yeongjoonJu/CFR-GAN?tab=readme-ov-file

For that, we are going to manually preprocess the images to jpg, 256x256, 8 bit images
(they say you should use some other repo, but I think this should be enough)

"""

ddata = '/home/bugger/Pictures/facerotation/top'


for i_file in os.listdir(ddata):
    if i_file.startswith('c'):
        file_path = os.path.join(ddata, i_file)
        base_name = hfile.get_base_name(i_file)
        dest_file_path = os.path.join(ddata, 'transformed_' + base_name + '.jpg')
        A = hfile.load_array(file_path)
        A_resize = sktransform.resize(A, (256, 256))
        A_bit = (A_resize * 256).astype(np.uint8)
        # hplot.ListPlot([A_bit[None, 128-80:128+80, 128-80:128+80]], cmap='rgb', sub_col_row=(1,1))
        # Cropping
        image_obj = Image.fromarray(A_bit[128-80:128+80, 128-80:128+80])
        image_obj.save(dest_file_path)
