from scipy.stats import poisson, expon, norm
from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


taus = [0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]
Q_errors_normal = []
Q_errors_poisson_10 = []
Q_errors_expon_10 = []
Q_errors_poisson_200 = []
Q_errors_expon_200 = []
Q_star_poisson_10 = []
Q_star_expon_10 = []
Q_star_poisson_200 = []
Q_star_expon_200 = []
Q_star_normal = []


for tau in taus:
    Q_hat = norm.ppf(tau, loc=25, scale=0.5)
    sample_norm = np.random.normal(loc=25, scale=0.5, size=200)     #n = 200 for normal test
    Q_star = np.sort(sample_norm)[int(np.ceil(tau * 200)) - 1]
    Q_errors_normal.append(abs(Q_hat - Q_star))
    Q_star_normal.append(Q_star)

n_list = [10, 200]

for n in n_list:
    for tau in taus:
        Q_hat = norm.ppf(tau, loc=25, scale=0.5)

        # Poisson
        sample_pois = np.random.poisson(25, size=n)
        Q_star_pois = np.sort(sample_pois)[int(np.ceil(tau * n)) - 1]
        
        # Exponential
        sample_exp = np.random.exponential(scale=25, size=n)
        Q_star_exp = np.sort(sample_exp)[int(np.ceil(tau * n)) - 1]
       
        if n == 10: 
            Q_errors_poisson_10.append(abs(Q_hat - Q_star_pois))
            Q_star_poisson_10.append(Q_star_pois)
            Q_errors_expon_10.append(abs(Q_hat - Q_star_exp))
            Q_star_expon_10.append(Q_star_exp)
        else:
            Q_errors_poisson_200.append(abs(Q_hat - Q_star_pois))
            Q_star_poisson_200.append(Q_star_pois)
            Q_errors_expon_200.append(abs(Q_hat - Q_star_exp))
            Q_star_expon_200.append(Q_star_exp)

Q_hat_values = [norm.ppf(tau, loc=25, scale=0.5) for tau in taus]

def build_table(Q_hat_list, Q_star_list, error_list):
    return pd.DataFrame(
        [Q_hat_list, Q_star_list, error_list],
        index=["Estimated (Q_hat)", "True (Q_star)", "Absolute Error"],
        columns=[f"{tau:.2f}" for tau in taus]
    )

tables = {
    "Normal (Correct)": build_table(Q_hat_values, Q_star_normal, Q_errors_normal),
    "Poisson n=10": build_table(Q_hat_values, Q_star_poisson_10, Q_errors_poisson_10),
    "Poisson n=200": build_table(Q_hat_values, Q_star_poisson_200, Q_errors_poisson_200),
    "Exponential n=10": build_table(Q_hat_values, Q_star_expon_10, Q_errors_expon_10),
    "Exponential n=200": build_table(Q_hat_values, Q_star_expon_200, Q_errors_expon_200),
}

with pd.ExcelWriter("./report/figures/task4/task4_tables.xlsx") as writer:
    for sheet_name, df in tables.items():
        df.to_excel(writer, sheet_name=sheet_name)