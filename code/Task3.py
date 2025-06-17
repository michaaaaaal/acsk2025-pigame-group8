from scipy.stats import norm
from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(60) #this is just for reproducability btw

mu = 115
sigma = 10
n = 50
tau = 0.9
M = 1000

Q_star =lambda tau: norm.ppf(tau,loc=115,scale=10)

Q_np_list = []
Q_p_list = []
Q_star_val = Q_star(tau)

for _ in range(M):
    demand_sample = np.random.normal(loc=mu, scale=sigma, size=n)
    mu_hat = np.mean(demand_sample)
    sigma_hat = np.std(demand_sample, ddof=1)

    #non-parametric
    sorted_sample = np.sort(demand_sample)
    Q_np = sorted_sample[int(np.ceil(tau * n)) - 1] #item from sorted demand sample at tau quantile
    Q_np_list.append(Q_np)
    
    #parametric
    Q_p = norm.ppf(tau, loc=mu_hat, scale=sigma_hat)
    Q_p_list.append(Q_p)

#RMSE
Q_np_array = np.array(Q_np_list)
Q_p_array = np.array(Q_p_list)

rmse_np = np.sqrt(np.mean((Q_np_array - Q_star_val)**2))
rmse_p = np.sqrt(np.mean((Q_p_array - Q_star_val)**2))

print(f"RMSE (Nonparametric): {round(rmse_np, 2)}")
print(f"RMSE (Parametric):    {round(rmse_p, 2)}")
print(f"RMSE Ratio (NP / P):  {round((rmse_np / rmse_p), 2)}")
