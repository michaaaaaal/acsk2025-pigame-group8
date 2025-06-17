from scipy.stats import norm
from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(60) #reproducability

mu = 115
sigma = 10
n = 50
tau = 0.9

demand_sample = np.random.normal(loc=mu, scale=sigma, size=n)
mu_hat = np.mean(demand_sample)
sigma_hat = np.std(demand_sample, ddof=1)
Q_star =lambda tau: norm.ppf(tau,loc=115,scale=10)

#non-parametric
sorted_sample = np.sort(demand_sample)
index = int(np.ceil(tau * n)) - 1
Q_np = sorted_sample[index]

print(Q_np)
print("True optimal Q:", Q_star(tau))