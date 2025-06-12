from scipy.stats import norm
from scipy.integrate import quad
import numpy as np

p = 4.64
c = 3.85
p_L = 0.15
c_S = 0.00
mu = 110
sigma = 10

tau = (p - c) / (p - p_L + c_S)

Q_star = norm.ppf(tau, loc=mu, scale=sigma)

def expected_min(mu, sigma, Q):
    f = lambda y: y * norm.pdf(y, loc=mu, scale=sigma)
    
    #i split the integral with min(Q, y) into summation of 2 integrals where y>Q and y<=Q

    term1, _ = quad(f, -np.inf, Q) #underscore is to ignore the second output of quad
    term2 = Q * (1 - norm.cdf(Q, loc=mu, scale=sigma))
    return term1 + term2

def expected_leftover(mu, sigma, Q):
    f = lambda y: (Q - y) * norm.pdf(y, loc=mu, scale=sigma)
    result, _ = quad(f, -np.inf, Q)
    return result