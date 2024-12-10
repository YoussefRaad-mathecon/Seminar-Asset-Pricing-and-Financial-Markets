import numpy as np
import time

# Monte Carlo simulation using full truncation scheme for Heston model
def heston_euler_mc(S0, v0, r, kappa, theta, sigma, rho, T, K, N, time_steps):
    dt = T / time_steps
    sqrt_dt = np.sqrt(dt)

    # Initialize arrays
    S = np.zeros((N, time_steps + 1))
    v = np.zeros((N, time_steps + 1))
    S[:, 0] = S0
    v[:, 0] = v0

    for t in range(1, time_steps + 1):
        Z1 = np.random.normal(0, 1, N)
        Z2 = rho * Z1 + np.sqrt(1 - rho**2) * np.random.normal(0, 1, N)

        v_t_positive = np.maximum(v[:, t-1], 0)

        # Variance update
        v[:, t] = (
            v[:, t-1]
            + kappa * (theta - v_t_positive) * dt
            + sigma * np.sqrt(v_t_positive) * Z1 * sqrt_dt
        )

        # Asset price update
        S[:, t] = S[:, t-1] * np.exp(r * dt
            -0.5 * v_t_positive * dt + np.sqrt(v_t_positive) * Z2 * sqrt_dt
        )

    # Discount factor
    discount_factor = np.exp(-r * T)

    # Calculate the call option payoff
    call_payoffs = discount_factor * np.maximum(S[:, -1] - K, 0)

    # Calculate option price and statistics
    price = np.mean(call_payoffs)
    std_dev = np.std(call_payoffs, ddof=1)
    Zc = 2.576  # 99% confidence level
    CI = Zc * std_dev / np.sqrt(N)

    return price, CI, std_dev

# Simulation cases
cases = {
    "Case I": {
        "S0": 100,
        "v0": 0.04,
        "r": 0.00,
        "kappa": 0.5,
        "theta": 0.04,
        "sigma": 1,
        "rho": -0.9,
        "T": 10,
        "time_steps": [10, 20, 40, 80, 160, 320],
        "actual_prices": {60: 44.329975068269974, 100: 13.084670136959673, 140: 0.2957744352991494},
    },
    "Case II": {
        "S0": 100,
        "v0": 0.09,
        "r": 0.05,
        "kappa": 1,
        "theta": 0.09,
        "sigma": 1,
        "rho": -0.3,
        "T": 5,
        "time_steps": [5, 10, 20, 40, 80, 160],
        "actual_prices": {60: 56.575081859298884, 100: 33.59687159343891, 140: 18.157002079695353},
    },
    "Case III": {
        "S0": 100,
        "v0": 0.04,
        "r": 0.00,
        "kappa": 0.3,
        "theta": 0.04,
        "sigma": 0.9,
        "rho": -0.5,
        "T": 15,
        "time_steps": [15, 30, 60, 120, 240, 480],
        "actual_prices": {60: 45.10147423567165, 100: 16.245256498934182, 140: 4.8885397955808365},
    },
}

# Monte Carlo settings
N = 1000000  # Number of paths
K_values = [60, 100, 140]

# Run simulations for all cases
for case_name, params in cases.items():
    print(f"\n--- Running simulations for {case_name} ---")
    S0, v0, r = params["S0"], params["v0"], params["r"]
    kappa, theta, sigma, rho = params["kappa"], params["theta"], params["sigma"], params["rho"]
    T, time_steps, actual_prices = params["T"], params["time_steps"], params["actual_prices"]

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

            print(f"K={K}, n={n}, dt={dt:.6f}, Price={option_price:.6f}, "
                  f"Bias={bias:.3f}, CI={CI:.3f}")
