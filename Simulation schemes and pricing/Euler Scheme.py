import numpy as np
import time
# Parameters
#case 2 example
S0 = 100
v0 = 0.09
r = 0.05
kappa = 1
theta = 0.09
sigma = 1
rho = -0.3
T = 5
N = 1000000



K_values = [60, 100, 140]
#time_steps = [10, 20, 40, 80, 160, 320]
time_steps = [5, 10, 20, 40, 80, 160]
#time_steps = [15, 30, 60, 120, 240, 480]
actual_prices = {60: 56.575081859298884,
    100: 33.59687159343891,
    140: 18.157002079695353
}


np.random.seed(112233)
# Initialize results dictionary
methods = ["Euler"]
results = {method: {K: [] for K in K_values} for method in methods}
def heston_euler_mc(S0, v0, r, kappa, theta, sigma, rho, T, K, N, time_steps):
    dt = T / time_steps
    S = np.zeros((N, time_steps + 1))
    v = np.zeros((N, time_steps + 1))

    S[:, 0] = S0
    v[:, 0] = v0

    for t in range(1, time_steps + 1):
        # Correlated Brownian motions
        Z1 = np.random.normal(0, 1, N)
        Z2 = rho * Z1 + np.sqrt(1 - rho**2) * np.random.normal(0, 1, N)

        # Variance process
        v[:, t] = v[:, t-1] + kappa * (theta - np.maximum(v[:, t-1], 0)) * dt + sigma * np.sqrt(np.maximum(v[:, t-1], 0)) * np.sqrt(dt) * Z1
        v[:, t] = np.maximum(v[:, t], 0)  # Ensure non-negative variance

        # Log-asset price process
        S[:, t] = S[:, t-1] * np.exp((r - 0.5 * np.maximum(v[:, t-1], 0) ) * dt + np.sqrt(np.maximum(v[:, t-1], 0)) * np.sqrt(dt) * Z2)

    # Compute discounted payoffs
    payoffs = np.exp(-r * T) * np.maximum(S[:, -1] - K, 0)
    call_price = np.mean(payoffs)
    std_dev = np.std(payoffs, ddof=1) # Standard deviation of payoffs
    Zc = 2.576
    CI = Zc * std_dev / np.sqrt(N)  # 99% Confidence Interval
    
    return call_price, CI, std_dev


# Adjusted usage in the loop
for method in methods:
    print(f"Running simulations for method: {method}")
    for K in K_values:
        for n in time_steps:
            dt = T / n
            start_time = time.time()
            option_price, CI, std_dev = heston_euler_mc(S0, v0, r, kappa, theta, sigma, rho, T, K, N, n)
            end_time = time.time()
            computing_time = end_time - start_time
            
            # Calculate bias
            actual_price = actual_prices[K]
            bias = actual_price - option_price
            
            lower_bound = option_price - CI
            upper_bound = option_price + CI
            within_CI = lower_bound <= actual_price <= upper_bound
            star = "*" if within_CI else ""

            results[method][K].append((dt, option_price, std_dev, computing_time, 0, CI, bias))

            print(f"Finished K={K}, n={n}, dt={dt:.6f}, Price={option_price:.6f}, Bias={bias:.3f}, CI={CI:.3f}{star}")
