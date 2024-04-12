"""

"""

# import gradio as gr
import numpy as np

import torch
from torchvision import transforms
from torch.autograd import Variable

from PIL import Image
import matplotlib.pyplot as plt

import warnings

warnings.filterwarnings('ignore')

from facerotation.network import G as G_generator
g_net = G_generator()
import sys
sys.path.append("/home/bugger/PycharmProjects/domotica/facerotation")
g_net.load_state_dict(torch.load("/home/bugger/Documents/data/pretr/scaleaway/generator_v0.pt", map_location=torch.device('cpu')))
# Load the saved Frontalization generator model
saved_model = torch.load("/home/bugger/Documents/data/pretr/scaleaway/generator_v0.pt", map_location=torch.device('cpu'))


def frontalize(image):
    # Convert the test image to a [1, 3, 128, 128]-shaped torch tensor
    # (as required by the frontalization model)
    preprocess = transforms.Compose((transforms.ToPILImage(),
                                     transforms.Resize(size=(128, 128)),
                                     transforms.ToTensor()))
    input_tensor = torch.unsqueeze(preprocess(image), 0)

    # Use the saved model to generate an output (whose values go between -1 and 1,
    # and this will need to get fixed before the output is displayed)
    generated_image = saved_model(Variable(input_tensor.type('torch.FloatTensor')))
    generated_image = generated_image.detach().squeeze().permute(1, 2, 0).numpy()
    generated_image = (generated_image + 1.0) / 2.0

    return generated_image

import harreveltools.helper.file_handeling as hfile
import harreveltools.helper.plot as hplot
A = hfile.load_array("/home/bugger/Pictures/facerotation/mid/converted_c21.jpg")
B = frontalize(A)
hplot.ListPlot([A[None], B[None]], cmap='rgb', sub_col_row=(1,1))
#iface = gr.Interface(frontalize, gr.inputs.Image(type="numpy"), "image")
# iface.launch()
