import pickle


"""

This was too much work

"""

pickle_path = ''
with open('DeepFace168.pickle', 'rb') as file:  # Binary read
    u = pickle._Unpickler(file)
    u.encoding = 'latin1'
    p = u.load()
    data_dict = p

