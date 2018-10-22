# encoding: utf-8

"""
Here we are going to create functions that can plot the results of nvidia text..
Can be used for a ... website?

Dit is dus echt kut. Ik haaaat pandas ...
Hopelijk kan t ook met numpy

Of plotted met pandas moet ik ff leren.
En moet natuurlijk ff bedenkn hoe ik dit dan kan embedded in een html pagina..
zou vet zijn als je pet plotly ofzo iets "interactiefs" kan doen.
"""

import os
import pandas as pd
import numpy as np


path_to_csv = '/home/charmmaria'
file_name = 'test_test_csv.csv'
A = pd.read_csv(os.path.join(path_to_csv, file_name))
A['Time'] = A['Time'].
A.loc[:, ['Time', 'Fan']]
A.groupby('GPU')