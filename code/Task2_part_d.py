from scipy.stats import norm
from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt


p = 1.5
c = 1
pL = 0.15
mu = 110
sigma = 10
cS_values = np.linspace(0, 0.5, 100)

Q_star_values = []
expected_profits = []

for cS in cS_values:
    Q_guess = mu
    
    for _ in range(3):
        surplus_prob = 1 - norm.cdf(Q_guess, loc=mu, scale=sigma)  # P(Q > Y)
        c_tilde = c - (pL - cS) * surplus_prob                     # Adjusted cost
        tau = (p - c_tilde) / p                                    # Critical ratio
        Q_guess = norm.ppf(tau, loc=mu, scale=sigma)               #Updated Q* from inverse CDF

    Q_star = Q_guess
    Q_star_values.append(Q_star)
   
    #E[Pi(Q, Y)] = (p - c)Q - p * ∫ F_Y(y) dy from -inf to Q
    
    integrand = lambda y: norm.cdf(y, loc=mu, scale=sigma)
    integral_value, _ = quad(integrand, -np.inf, Q_star)
    
    expected_profit = (p - c) * Q_star - p * integral_value
    expected_profits.append(expected_profit)


plt.figure(figsize=(14, 6))

#Q* vs cS
plt.subplot(1, 2, 1)
plt.plot(cS_values, Q_star_values, color='blue', linewidth=3)
plt.xlabel('Shipping cost ($c_S$)')
plt.ylabel('Optimal order quantity ($Q^*$)')
plt.title('Effect of ($c_S$) on ($Q^*$)')

#Expected Profit vs cS
plt.subplot(1, 2, 2)
plt.plot(cS_values, expected_profits, color='blue', linewidth=3)
plt.xlabel('Shipping cost ($c_S$)')
plt.ylabel('Expected profit')
plt.title('Effect of ($c_S$) on Expected Profit')

plt.tight_layout()
plt.savefig(f"./report/figures/task2/task2plot", dpi=300)
plt.show()