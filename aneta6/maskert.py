
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import helper.array_transf as harray

ddata = '/home/bugger/Pictures/wijnfleswit.jpeg'
dtarget= '/home/bugger/Pictures/wijnfleswitmask.svg'
dtarget_png = '/home/bugger/Pictures/wijnfleswitmask.png'
pil_obj = Image.open(ddata)
A = np.array(pil_obj)
A_mask = harray.get_treshold_label_mask(A[:, :, 0])
A_mask1 = harray.get_treshold_label_mask(A[:, :, 1])
A_mask2 = harray.get_treshold_label_mask(A[:, :, 2])
plt.imshow(A_mask)
plt.imshow(A_mask1)
B = 1 - A_mask2[:950, 300:800]
fig, ax = plt.subplots()
aximshow = plt.imshow(B)
ax.set_axis_off()
fig.savefig(dtarget, bbox_inches='tight')

img_obj = Image.fromarray(255 * B.astype(np.uint8))
img_obj.save(dtarget_png)


# ANOTHER ONE
ddata = '/home/bugger/Pictures/dirk_auto_unit.jpeg'
dtarget= '/home/bugger/Pictures/dirk_auto_unitmask.svg'
dtarget_png = '/home/bugger/Pictures/dirk_auto_unitmask.png'
pil_obj = Image.open(ddata)
A = np.array(pil_obj)
plt.imshow(A[:, :, 0] < 170)
plt.imshow(A[:, :, 1])
plt.imshow(A[:, :, 2])