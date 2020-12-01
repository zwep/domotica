"""

Image enhancement using Bi-Histogram Equalization with adaptive sigmoid functions

Edgar F. Arriaga-Garcia; Raul E. Sanchez-Yanez; M. G. Garcia-Hernande

"""
import numpy as np
import matplotlib.pyplot as plt
import skimage.data as data


# Load an example image
input_256 = data.moon()
x = input_256[input_256 != 0]
mean_value = int(np.round(np.mean(x)))
max_value = int(x.max())
bin_height, bin_value = np.histogram(x, bins=max_value)
# Last value is the max value..
# Now the lengths are equal..
bin_value = bin_value[:-1]
plt.bar(bin_value[bin_value <= mean_value], bin_height[bin_value <= mean_value])
plt.bar(bin_value[bin_value > mean_value], bin_height[bin_value > mean_value])

pdf_HL = bin_height[bin_value <= mean_value] / bin_height[bin_value <= mean_value].sum()
pdf_HU = bin_height[bin_value > mean_value] / bin_height[bin_value < mean_value].sum()

# These ones produce the Median values...
mu_L = np.argmin([np.abs(pdf_HL[:i].sum() - 0.5) for i in range(len(pdf_HL))])
print('Checking median value ', pdf_HL[:mu_L].sum())
mu_U = np.argmin([np.abs(pdf_HU[:i].sum() - 0.5) for i in range(len(pdf_HU))])
print('Checking median value ', pdf_HU[:mu_U].sum())

z_L = 5 * (np.arange(0, mean_value) - mu_L) / mean_value
z_U = 5 * (np.arange(mean_value, max_value) - mu_U) / (max_value - 1 - mean_value)
plt.figure()
plt.plot(np.arange(0, mean_value), z_L)
plt.plot(np.arange(mean_value, max_value), z_U)

gamma = 1.5
sigmoid_L = 1 / (1 + np.exp(-gamma * z_L))
sigmoid_U = 1 / (1 + np.exp(-gamma * z_U))
plt.figure()
plt.plot(np.arange(0, mean_value), sigmoid_L)
plt.plot(np.arange(mean_value, max_value), sigmoid_U)

L0 = 0
Lf = max_value - 1

u_L = L0 + (mean_value - L0) * sigmoid_L
u_U = mean_value + (Lf - mean_value) * sigmoid_U
plt.figure()
plt.plot(np.arange(0, mean_value), u_L)
plt.plot(np.arange(mean_value, max_value), u_U)

alpha_L = (mean_value - L0) / (u_L.max() - u_L.min())
alpha_U = (Lf - mean_value) / (u_U.max() - u_U.min())

T_L = L0 + alpha_L * (u_L - u_L.min())
T_U = mean_value + alpha_U * (u_U - u_L.min())

plt.figure()
plt.plot(T_L)
plt.plot(T_U)

input_256_beahf = np.zeros(input_256.shape)
for i in range(input_256.shape[0]):
    for j in range(input_256.shape[1]):
        x0 = input_256[i, j]
        k_ind = (bin_value < x0).sum()
        k_ind = min(k_ind, mean_value)
        if k_ind >= mean_value:
            # It is from the upper part...
            new_value = T_U[k_ind - mean_value - 1]
        else:
            new_value = T_L[k_ind]

        input_256_beahf[i, j] = new_value

fig, ax = plt.subplots(2)
ax[0].imshow(input_256_beahf, cmap='gray')
ax[1].imshow(input_256, cmap='gray')

