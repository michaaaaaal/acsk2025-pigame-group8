from scipy.stats import norm
from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

np.random.seed(60) #this is just for reproducability btw

def nvp_formula(Q, Y, c, p):
    return p * min(Q, Y) - c * Q

mu = 115
sigma = 10
n = 50
tau = 0.9
M = 1000

n_list = [10, 50, 100, 200]
tau_list = [0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]

#this is for PLR
c = 1 - tau
p = 1

results = []
for n in n_list:
    for tau in tau_list:
            
        Q_np_list = []
        Q_p_list = []
        Q_star_val = norm.ppf(tau, loc=mu, scale=sigma)
        plr_np_list = []
        plr_p_list = []

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


            #PLR
            Y_obs = np.random.normal(loc=mu, scale=sigma) #simulating a random demand value for PLR evaluation
            R_star = nvp_formula(Q_star_val, Y_obs, c, p)
            R_np = nvp_formula(Q_np, Y_obs, c, p)
            R_p = nvp_formula(Q_p, Y_obs, c, p)

            plr_np_list.append(abs((R_star - R_np) / R_star))
            plr_p_list.append(abs((R_star - R_p) / R_star))


        #RMSE
        Q_np_array = np.array(Q_np_list)
        Q_p_array = np.array(Q_p_list)

        rmse_np = np.sqrt(np.mean((Q_np_array - Q_star_val)**2))
        rmse_p = np.sqrt(np.mean((Q_p_array - Q_star_val)**2))

        #PLR
        plr_np = np.mean(plr_np_list)
        plr_p = np.mean(plr_p_list)

        results.append({
            'n': n,
            'tau': tau,
            'RMSE (Nonparametric)': rmse_np,
            'RMSE (Parametric)': rmse_p,
            'PLR (Nonparametric)': plr_np,
            'PLR (Parametric)': plr_p,
            'RMSE ratio (Nonparametric / Parametric)': rmse_np / rmse_p,
            'PLR ratio (Nonparametric / Parametric)': plr_np / plr_p
        })

df = pd.DataFrame(results)
df.to_csv("./report/figures/task3/task3_simulation_results.csv", index=False)
df.to_excel("./report/figures/task3/task3_simulation_results.xlsx", index=False)