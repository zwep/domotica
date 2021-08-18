import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt


def print_dict(d, level=0):
    # Prints a dictionary
    for k, v in d.items():
        if isinstance(v, dict):
            print(level * '\t', k, ':')
            print_dict(v, level + 1)
        else:
            print(level * '\t', k, '-', v)


# parameters and grid
n = 100
x_matrix = np.linspace(0, n, n+1)
x = np.linspace(0, 1, n+1)

# Create the response functions
u_11 = np.zeros(n+1)
u_11[x > 0.3] = 1
u_12 = np.zeros(n+1)
u_12[x > 0.7] = 1
u_1 = u_11 - u_12

u_2 = x * (1 - x)

# Display response functions
plt.plot(x, u_1)
plt.plot(x, u_2)

# define forward operator
a = 1
c = np.exp(-a * x_matrix ** 2) / ((n - 1) * np.sqrt(np.pi/a))
K = la.toeplitz(c)
K_cond_nr = np.linalg.cond(K)
print('Condition number... ', K_cond_nr)

# Okay we are off good...
# Now let use vary that delta.. and recover u...
# But also see the impact of a.
result_dict = {}
for i, u_sel in enumerate([u_1, u_2]):
    u_key = f'u_{i+1}'
    result_dict.setdefault(u_key, {})

    for delta in [0.001, 0.01, 0.1]:
        temp_key = f"delta:{delta}"
        u_svd, s_svd, vh_svd = np.linalg.svd(K, full_matrices=True)
        K_svd_inv = vh_svd.conj().T @ np.diag(1 / s_svd) @ u_svd.conj().T
        f_delta = K @ u_sel + delta * np.random.randn(n + 1)
        u_delta = np.matmul(K_svd_inv, f_delta)
        difference_value = np.linalg.norm(u_sel - u_delta)
        result_dict[u_key].update({temp_key: difference_value})

print_dict(result_dict)

# Exercise 3..
# Now we ware going to calculate the truncated SVD

# Okay we are off good...
# Now let use vary that delta.. and recover u...
# But also see the impact of a.
result_dict = {}
for i, u_sel in enumerate([u_1, u_2]):
    u_key = f'u_{i+1}'
    result_dict.setdefault(u_key, {})

    for delta in [0.001, 0.01, 0.1]:
        temp_key = f"delta:{delta}"
        u_svd, s_svd, vh_svd = np.linalg.svd(K, full_matrices=True)
        f_delta = K @ u_sel + delta * np.random.randn(n + 1)
        f = K @ u_sel
        picard_f_delta = np.array([np.abs(np.dot(u_svd[:, i], f_delta)) for i in range(n + 1)])

        # Visualization of the discrete Picard condition
        fig, ax = plt.subplots()
        plt.plot([np.abs(np.dot(u_svd[:, i], f)) for i in range(n+1)], 'r', label='|<u_i, f>|')
        plt.plot(picard_f_delta, 'b', label='|<u_i, f_delta>|')
        plt.plot(s_svd, 'k', label='sigma_i')
        plt.title(f'Delta: {delta}')
        ax.set_yscale('log')
        plt.legend()

        trunc_ind_list = np.where((picard_f_delta - s_svd) > 0)
        plt.plot(trunc_ind_list)
        if trunc_ind_list:
            trunc_ind = trunc_ind_list[0][0]
            print('Trunc ID ', trunc_ind, delta)
        else:
            print('NO ID FOUND')
            trunc_ind = 1

        trunc_svd = np.copy(1 / s_svd)
        trunc_svd[trunc_ind:] = 0
        K_svd_inv_trunc = vh_svd.conj().T @ np.diag(trunc_svd) @ u_svd.conj().T

        u_delta = np.matmul(K_svd_inv_trunc, f_delta)
        plt.figure()
        plt.plot(u_delta)
        plt.plot(u_sel)
        difference_value = np.linalg.norm(u_delta - u_sel)

        result_dict[u_key].update({temp_key: difference_value})

print_dict(result_dict)


