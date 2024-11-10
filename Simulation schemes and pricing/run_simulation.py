import numpy as np
import time
from HestonModel import HestonModel

np.random.seed(112233)

# Given parameters case 3 efficient, almost exact **reim euler times FIX ACTUAL PRICES THO**
S0 = 100
v0 = 0.04
r = 0.00
kappa = 0.5
theta = 0.04    
sigma = 1
rho = -0.9
T = 10
N = 10000 # Number of paths for Monte Carlo
lambdaa = 0
K_values = [60, 100, 140]
#time_steps = [15, 30, 60, 120, 240, 480]
time_steps = [10, 20, 40, 80, 160, 320]
methods = ["EulerDisc", "MilsteinDisc", "QEDisc", "QEMDisc", "TGMDisc", "TGDisc", "BKDI"]

# Actual prices from OriginalFT stable
actual_prices = {
    60: 44.329975068269974,
    100: 13.084670136959673,
    140: 0.2957744352991494
}


# Initialize results dictionary
results = {method: {K: [] for K in K_values} for method in methods}

# Run simulations for each method, strike price, and time step
heston_model = HestonModel(S0, v0, r, kappa, theta, sigma, rho, lambdaa, gamma1=0.5, gamma2=0.5, alpha=4.5)

for method in methods:
    print(f"Running simulations for method: {method}")
    for K in K_values:
        for n in time_steps:
            dt = T / n
            start_time = time.time()
            option_price, v_zero_counts, CI = heston_model.priceHestonCallViaMC(K, T, n, N, method)
            end_time = time.time()
            computing_time = end_time - start_time
            std_dev = np.std(option_price)
            total_v_zero_count = np.sum(v_zero_counts)
            
            # Calculate bias
            actual_price = actual_prices[K]
            bias = actual_price - option_price
            
            # Check if the actual price is within the confidence interval
            lower_bound = option_price - CI
            upper_bound = option_price + CI
            within_CI = lower_bound <= actual_price <= upper_bound
            star = "*" if within_CI else ""
            
            results[method][K].append((dt, option_price, std_dev, computing_time, total_v_zero_count, CI, bias))
            print(f"Finished K={K}, n={n}, dt={dt}, Price={option_price}, Time={computing_time}s, Bias={bias}, CI={CI}{star}, zero variance={total_v_zero_count}")
 