from scipy.stats import poisson, expon, norm
import numpy as np
import pandas as pd

taus = [0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]
Q_hat_values = [norm.ppf(tau, loc=25, scale=0.5) for tau in taus]
M = 1000

Q_errors_normal_10 = [[] for _ in taus]
Q_errors_normal_200 = [[] for _ in taus]
Q_errors_poisson_10 = [[] for _ in taus]
Q_errors_poisson_200 = [[] for _ in taus]
Q_errors_expon_10 = [[] for _ in taus]
Q_errors_expon_200 = [[] for _ in taus]

for n in [10, 200]:
    for i, tau in enumerate(taus):
        Q_hat = norm.ppf(tau, loc=25, scale=0.5)

        for _ in range(M):
            norm_sample = np.random.normal(25, 0.5, size=n)
            pois_sample = np.random.poisson(25, size=n)
            exp_sample = np.random.exponential(scale=25, size=n)

            mu_hat = np.mean(norm_sample)
            sigma_hat = np.std(norm_sample, ddof=1)
            Q_hat = norm.ppf(tau, loc=mu_hat, scale=sigma_hat)

            Q_star_norm = norm.ppf(tau, loc=25, scale=0.5)
            Q_star_pois = poisson.ppf(tau, mu=25)
            Q_star_exp = expon.ppf(tau, scale=25)

            if n == 10:
                Q_errors_normal_10[i].append(abs(Q_hat - Q_star_norm))
                Q_errors_poisson_10[i].append(abs(Q_hat - Q_star_pois))
                Q_errors_expon_10[i].append(abs(Q_hat - Q_star_exp))
            else:
                Q_errors_normal_200[i].append(abs(Q_hat - Q_star_norm))
                Q_errors_poisson_200[i].append(abs(Q_hat - Q_star_pois))
                Q_errors_expon_200[i].append(abs(Q_hat - Q_star_exp))

# Build tables
def build_table(Q_hat_values, grouped_errors):
    return pd.DataFrame(
        [Q_hat_values, Q_hat_values, [np.mean(errors) for errors in grouped_errors]],
        index=["Estimated (Q_hat)", "True (Q_star)", "Absolute Error"],
        columns=[f"{tau:.2f}" for tau in taus]
    )

tables = {
    "Normal n=10": build_table(Q_hat_values, Q_errors_normal_10),
    "Normal n=200": build_table(Q_hat_values, Q_errors_normal_200),
    "Poisson n=10": build_table(Q_hat_values, Q_errors_poisson_10),
    "Poisson n=200": build_table(Q_hat_values, Q_errors_poisson_200),
    "Exponential n=10": build_table(Q_hat_values, Q_errors_expon_10),
    "Exponential n=200": build_table(Q_hat_values, Q_errors_expon_200),
}

with pd.ExcelWriter("./report/figures/task4/task4_tables_simulated1000times.xlsx") as writer:
    for sheet_name, df in tables.items():
        df.to_excel(writer, sheet_name=sheet_name)
