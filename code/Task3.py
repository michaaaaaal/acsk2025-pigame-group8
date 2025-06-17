from scipy.stats import norm
from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(60) #reproducability

mu = 115
sigma = 10
n = 50

demand_sample = np.random.normal(loc=mu, scale=sigma, size=n)

print(demand_sample)