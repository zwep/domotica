import numpy as np
import scipy.ndimage.interpolation as scint
import scipy.signal
import scipy.ndimage
import scipy.optimize


def get_treshold_label_mask(x, structure=None, class_treshold=0.04, treshold_value=None, debug=False):
    # Class treshold: is a number in [0, 1], which value is used to treshold the size of each labeled region, which
    # are expressed as a parcentage. The labeled regions are the found continuous blobs of a certain size
    # The treshold value is optional, normally the mean is used to treshold the whole image
    # Method of choice
    if treshold_value is None:
        treshold_mask = x > np.mean(x)
    else:
        treshold_mask = x > treshold_value

    treshold_mask = scipy.ndimage.binary_fill_holes(treshold_mask)

    if structure is None:
        structure = np.ones((3, 3))

    labeled, n_comp = scipy.ndimage.label(treshold_mask, structure)
    count_labels = [np.sum(labeled == i) for i in range(1, n_comp)]
    total_count = np.sum(count_labels)

    # If it is larger than 4%... then go (determined empirically)
    count_labels_index = [i + 1 for i, x in enumerate(count_labels) if x / total_count > class_treshold]
    if debug:
        print('Selected labels ', count_labels_index,'/', n_comp)
    if len(count_labels_index):
        x_mask = np.sum([labeled == x for x in count_labels_index], axis=0)
    else:
        x_mask = labeled == 1
    return x_mask
