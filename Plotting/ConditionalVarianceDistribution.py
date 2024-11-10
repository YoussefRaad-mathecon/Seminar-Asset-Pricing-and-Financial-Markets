import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ncx2, norm, lognorm

# Define parameters
kappa = 0.5
theta = 0.04
varepsilon = 1.0
sigma = varepsilon
V_t = 0.09
T = 0.1
t = 0.0

# Calculate n(t, T)
n_t_T = 4 * kappa * np.exp(-kappa * (T - t)) / (varepsilon ** 2 * (1 - np.exp(-kappa * (T - t))))

# Calculate parameters for the non-central chi-square distribution
d = 4 * kappa * theta / (varepsilon ** 2)
lambda_nc = V_t * n_t_T
scale_nc = np.exp(-kappa * (T - t)) / n_t_T

# Generate x values
x = np.linspace(0, 1.5 * (V_t + theta), 10000)

# Non-central chi-square CDF
cdf_nc = ncx2.cdf(x * n_t_T / np.exp(-kappa * (T - t)), d, lambda_nc)

# Parameters for the Gaussian distribution
mean_gaussian = theta + (V_t - theta) * np.exp(-kappa * (T - t))
variance_gaussian = (V_t * varepsilon ** 2 * np.exp(-kappa * (T - t))) / kappa * (1 - np.exp(-kappa * (T - t))) + (theta * varepsilon ** 2) / (2 * kappa) * (1 - np.exp(-kappa * (T - t))) ** 2
std_gaussian = np.sqrt(variance_gaussian)

# Gaussian CDF
cdf_gaussian = norm.cdf(x, mean_gaussian, std_gaussian)

# Parameters for the Lognormal distribution
mean_lognormal = np.log(mean_gaussian ** 2 / np.sqrt(variance_gaussian + mean_gaussian ** 2))
sigma_lognormal = np.sqrt(np.log(variance_gaussian / mean_gaussian ** 2 + 1))

# Lognormal CDF
cdf_lognormal = lognorm.cdf(x, sigma_lognormal, scale=np.exp(mean_lognormal))


### QE scheme psi > psi_c
dt = T - t
exponent = np.exp(-kappa * dt)
m = theta + (V_t - theta) * exponent
s2 = ((V_t * sigma ** 2 * exponent * (1 - exponent)) / kappa +
      (theta * sigma ** 2 * (1 - exponent) ** 2 / (2 * kappa)))
psi = s2 / m ** 2
Uv = np.random.uniform(size=10000)
# Generate v_next values using the QE scheme for ψ ≤ ψ_c
p = (psi - 1) / (psi + 1)
beta = (1 - p) / m
v_next = (1 / beta) * np.log((1 - p) / (1 - Uv))
# Generate QE CDF from v_next values
cdf_qe2 = np.array([np.sum(v_next <= xi) for xi in x]) / len(v_next)

# Plotting
plt.figure(figsize=(12, 8))

# Update rcParams to use LaTeX
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "text.latex.preamble": r"\usepackage{amsmath} \usepackage{amssymb}"
})

# Plotting CDFs
plt.plot(x, cdf_nc, label='Exact', color='blue', linestyle='-')
plt.plot(x, cdf_gaussian, label='Gaussian', color='red', linestyle='--')
plt.plot(x, cdf_lognormal, label='Lognormal', color='green', linestyle='-.')
plt.plot(x, cdf_qe2, label=r'QE ($\psi > \psi_c$)', color='saddlebrown', linestyle=':')

# Customizing the plot
plt.xlabel(r'$x$', fontsize=18)  # Larger font size for x-axis label
plt.ylabel(r'$\mathbb{P}(v_T \leq x \mid v_t)$', fontsize=18)  # Larger font size for y-axis label
plt.legend(fontsize=14)  # Larger font size for legend

# Adjust tick label sizes
plt.xticks(fontsize=14)  # Larger font size for x-axis ticks
plt.yticks(fontsize=14)  # Larger font size for y-axis ticks

# Remove the upper and right borders
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout
plt.show()
