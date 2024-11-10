import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from scipy.stats import gaussian_kde

np.random.seed(112233)

# Given parameters
S0 = 100
v0 = 0.04
r = 0.00
kappa = 0.5
theta = 0.04    
sigma = 1
rho = -0.9
lambdaa = 0.00
T = 10
N = 1000000# Number of paths for Monte Carlo
K_values = [100]
#K_values = [60, 100, 140]
time_steps = [320]

# Function to generate a Heston path using Euler discretization with full truncation
def generateHestonPathEulerDisc(S0, v0, r, kappa, theta, sigma, rho, lambdaa, T, n):
    kappa_tilde = kappa + lambdaa
    theta_tilde = (kappa * theta) / (kappa + lambdaa)
    dt = T / n
    S = np.zeros(n + 1)
    S[0] = S0
    v = np.zeros(n + 1)
    v[0] = v0
    v_zero_count = 0
    Z1 = np.random.normal(0, 1, n)
    Z2 = np.random.normal(0, 1, n)
    Zv = Z1
    Zs = rho * Z1 + np.sqrt(1 - rho ** 2) * Z2
    for i in range(1, n + 1):
        dv = kappa_tilde * (theta_tilde - v[i - 1]) * dt + sigma * np.sqrt(v[i - 1] * dt) * Zv[i-1]

        v[i] = v[i - 1] + dv
        if v[i] <= 0:
            v_zero_count += 1
            v[i] = 0  # full truncation scheme

        dS = r * S[i - 1] * dt + np.sqrt(v[i - 1] * dt) * S[i - 1] * Zs[i-1]
        S[i] = S[i - 1] + dS

    return S, v_zero_count

# Function to price a Heston call option using Euler Monte Carlo simulation
def priceHestonCallViaEulerMC(S0, v0, r, kappa, theta, sigma, rho, lambda_, T, n, N, K):
    start_time = time.time()
    total_v_zero_count = 0
    payoffs = np.zeros(N)

    for i in range(N):
        S, v_zero_count = generateHestonPathEulerDisc(S0, v0, r, kappa, theta, sigma, rho, lambda_, T, n)
        total_v_zero_count += v_zero_count
        payoffs[i] = max(S[-1] - K, 0)

    option_price = np.exp(-r * T) * np.mean(payoffs)
    std_dev = np.std(payoffs, ddof=1) / np.sqrt(N)
    end_time = time.time()
    computing_time = end_time - start_time

    return option_price, std_dev, computing_time, total_v_zero_count

# Different time steps
time_steps = [10, 20, 40, 80, 160, 320]

# Store results for each time step
results = {K: [] for K in K_values}

for K in K_values:
    for n in time_steps:
        option_price, std_dev, computing_time, total_v_zero_count = priceHestonCallViaEulerMC(S0, v0, r, kappa, theta, sigma, rho, lambdaa, T, n, N, K)
        results[K].append((T/n, option_price, std_dev, computing_time, total_v_zero_count))

print("Results (Euler):")
# Print results
total_computing_time = 0
for K in K_values:
    print(f"Results for K = {K}:")
    for result in results[K]:
        dt, option_price, std_dev, computing_time, total_v_zero_count = result
        total_computing_time += computing_time
        print(f"Time step (dt): {dt}")
        print(f"Option price: {option_price}")
        print(f"Standard deviation: {std_dev}")
        print(f"Computing time: {computing_time} seconds")
        print(f"Zero variance occurrences: {total_v_zero_count}\n")
print(f"Total computing time: {total_computing_time} seconds")

# Number of paths to simulate
num_paths = 1000
# Number of time steps for each path
n = 32

# Generate the paths
paths = np.zeros((num_paths, n+1))
final_prices = np.zeros(num_paths)
for i in range(num_paths):
    S, _ = generateHestonPathEulerDisc(S0, v0, r, kappa, theta, sigma, rho, lambdaa, T, n)
    paths[i] = S
    final_prices[i] = S[-1]

from matplotlib import rcParams
# Update matplotlib settings to use LaTeX with Computer Modern Roman font
rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "text.latex.preamble": r"\usepackage{amsmath} \usepackage{amssymb}",
    "axes.labelsize": 15,
    "axes.titlesize": 15,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12
})

# Create the figure with gridspec for better control
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), gridspec_kw={'width_ratios': [2, 1]})

# Plotting stock price paths
for i in range(num_paths):
    ax1.plot(np.linspace(0, T, n+1), paths[i], lw=0.5)
ax1.set_xlabel(r"\textbf{Time (Years)}")
ax1.set_ylabel(r"\textbf{Stock Price}")
ax1.set_xlim(0, 1)

# Compute density
kde = gaussian_kde(final_prices, bw_method='scott')
x = np.linspace(min(final_prices), max(final_prices), 1000)
density = kde(x)

# Plot histogram of final stock prices
hist, bins, patches = ax2.hist(final_prices, bins=50, orientation='horizontal', color='lightblue', edgecolor='black', density=True)

# Create a color map
norm = Normalize(vmin=min(density), vmax=max(density))
cmap = cm.ScalarMappable(norm=norm, cmap='coolwarm')

# Plot density as a heatmap
for i in range(len(patches)):
    bin_cent = 0.5 * (bins[i] + bins[i + 1])
    density_val = kde(bin_cent)
    patches[i].set_facecolor(cmap.to_rgba(density_val))
    patches[i].set_edgecolor('black')

# Add a color bar
cbar = plt.colorbar(cmap, ax=ax2, orientation='vertical')
cbar.set_label('Density')

ax2.set_xlabel(r"\textbf{Frequency}")
ax2.set_ylabel(r"\textbf{Final Stock Price}")

plt.tight_layout()
plt.show()
