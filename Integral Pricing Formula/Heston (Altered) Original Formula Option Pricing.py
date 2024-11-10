import numpy as np
from scipy.integrate import quad
import time

np.random.seed(11223344)


# Given parameters
S0 = 100
v0 = 0.04
r = 0.00
kappa = 0.3
theta = 0.04    
sigma = 0.9
rho = -0.5
tau = 15
lambda_=0
K = 140

# 60 100 140 for K
#Case 1
#S0 = 100
#v0 = 0.04
#r = 0.00
#kappa = 0.5
#theta = 0.04    
#sigma = 1
#rho = -0.9
#tau = 10
#lambda_=0
#The option price is (OriginalFT): 44.329975068269974
#The computing time is (OriginalFT): 0.018950462341308594 seconds
#The estimated numerical integration error is: 1.0260029475654468e-08


#The option price is (OriginalFT): 13.084670136959673
#The computing time is (OriginalFT): 0.009973287582397461 seconds
#The estimated numerical integration error is: 5.118146115856962e-09

#The option price is (OriginalFT): 0.2957744352991494
#The computing time is (OriginalFT): 0.007978439331054688 seconds
#The estimated numerical integration error is: 1.4275899406208714e-09


#Case 2
#S0 = 100
#v0 = 0.09
#r = 0.05
#kappa = 1
#theta = 0.09    
#sigma = 1
#rho = -0.3
#tau = 5
#lambda_=0

#The option price is (OriginalFT): 56.575081859298884
#The computing time is (OriginalFT): 0.005018472671508789 seconds
#The estimated numerical integration error is: 8.994435524831609e-09


#The option price is (OriginalFT): 33.59687159343891
#The computing time is (OriginalFT): 0.005574226379394531 seconds
#The estimated numerical integration error is: 3.7763409258373756e-10

#The option price is (OriginalFT): 18.157002079695353
#The computing time is (OriginalFT): 0.0055081844329833984 seconds
#The estimated numerical integration error is: 5.375598209426825e-09


#Case 3
#S0 = 100
#v0 = 0.04
#r = 0.00
#kappa = 0.3
#theta = 0.04    
#sigma = 0.9
#rho = -0.5
#tau = 15
#lambda_=0
#K = 60

#The option price is (OriginalFT): 45.10147423567165
#The computing time is (OriginalFT): 0.012376785278320312 seconds
#The estimated numerical integration error is: 5.7470997243745944e-09

#The option price is (OriginalFT): 16.245256498934182
#The computing time is (OriginalFT): 0.00810551643371582 seconds
#The estimated numerical integration error is: 6.586573425104762e-12

#The option price is (OriginalFT): 4.8885397955808365
#The computing time is (OriginalFT): 0.0025482177734375 seconds
#The estimated numerical integration error is: 5.068075775556235e-09

def characteristicFunctionHeston(u, St, vt, r, kappa, theta, sigma, rho, lambda_, tau, j):
    i = complex(0, 1)
    a = kappa * theta
    b1 = kappa + lambda_ - rho * sigma
    b2 = kappa + lambda_
    u1 = 0.5
    u2 = -0.5

    if j == 1:
        b_j = b1
        u_j = u1
    else:
        b_j = b2
        u_j = u2

    d_j = np.sqrt((b_j - rho * sigma * i * u) ** 2 - sigma ** 2 * (2 * u_j * i * u - u ** 2))
    g_j = (b_j - rho * sigma * i * u - d_j) / (b_j - rho * sigma * i * u + d_j)
    C_j = r * i * u * tau + (a / sigma ** 2) * ((b_j - rho * sigma * i * u - d_j) * tau - 2 * np.log((1 - g_j * np.exp(-d_j * tau)) / (1 - g_j)))
    D_j = (b_j - rho * sigma * i * u - d_j) * ((1 - np.exp(-d_j * tau) / sigma ** 2 * (1 - g_j * np.exp(-d_j * tau))))

    return np.exp(C_j + D_j * vt + i * u * np.log(St))

def priceHestonCallViaOriginalFT(St, vt, r, kappa, theta, sigma, rho, lambda_, tau, K):
    integrationlimit = np.inf
    integrandQj = lambda u, j: np.real(np.exp(-complex(0, 1) * u * np.log(K)) * characteristicFunctionHeston(u, St, vt, r, kappa, theta, sigma, rho, lambda_, tau, j) / (complex(0, 1) * u))
    Q1, errorQ1 = quad(integrandQj, 0, integrationlimit, args=(1,))
    Q2, errorQ2 = quad(integrandQj, 0, integrationlimit, args=(2,))
    
    option_price = St * (0.5 + (1 / np.pi) * Q1) - np.exp(-r * tau) * K * (0.5 + (1 / np.pi) * Q2)
    total_error = (1 / np.pi) * (np.abs(errorQ1) + np.abs(errorQ2))
    
    return option_price, total_error

start_time = time.time()
option_price, total_error = priceHestonCallViaOriginalFT(S0, v0, r, kappa, theta, sigma, rho, lambda_, tau, K)
end_time = time.time()
computing_time = end_time - start_time

print(f"The option price is (OriginalFT): {option_price}")
print(f"The computing time is (OriginalFT): {computing_time} seconds")
print(f"The estimated numerical integration error is: {total_error}")
