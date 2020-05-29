import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.misc import factorial

def randomPoisson(self, lam, iteration):
    y = []
    for k in range(iteration):
        p = 1
        L = exp(-lam)
        k = 0
        while (1):
            k += 1
            p *= uniform(0, 1)
            if (p <= L):
                break
        y.append((k - 1))
    return y
# get poisson deviated random numbers
data = np.random.poisson(2, 1000)

# the bins should be of integer width, because poisson is an integer distribution
counts, bins = np.histogram(data, bins=40, range=[0, 40], density=True)
bins = bins[:-1] + (bins[0] + bins[1])/2

plt.bar(bins, counts)
# entries, bin_edges, patches = plt.hist(data, bins=11, range=[-0.5, 10.5], density=True)

# calculate binmiddles
# bin_middles = 0.5*(bin_edges[1:] + bin_edges[:-1])

# # poisson function, parameter lamb is the fit parameter
# def poisson(k, lamb):
#     return (lamb**k/factorial(k)) * np.exp(-lamb)

# # fit with curve_fit
# parameters, cov_matrix = curve_fit(poisson, bin_middles, entries) 

# # plot poisson-deviation with fitted parameter
# x_plot = np.linspace(0, 20, 1000)

# plt.plot(x_plot, poisson(x_plot, *parameters), 'r-', lw=2)
plt.show()