from scipy.stats import norm, gamma, expon, poisson
import numpy as np
import pandas as pd

np.random.seed(60)

# Newsvendor profit function
def nvp_formula(Q, Y, c, p):
    return p * min(Q, Y) - c * Q

# Parameters
n_list = [10, 50, 100, 200]
tau_list = [0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]
M = 1000  # Number of simulations
c_base = 1  # Base cost (adjusted per tau)
p = 1       # Selling price

# Adjust gamma parameters to match normal mean=115, var=100
gamma_shape = (115**2) / 100   # 132.25
gamma_scale = 100 / 115         # ~0.8696
exp_scale = 115                 # Mean=115, var=13225 (fixed)
poisson_lambda = 115            # Mean=115, var=115
norm_mu, norm_sigma = 115, 10   # Mean=115, var=100

all_results = []


# Gamma Distribution
for n in n_list:
    for tau in tau_list:
        c = c_base * (1 - tau)
        Q_star_gamma = gamma.ppf(tau, gamma_shape, scale=gamma_scale)

        Q_np_list = []
        Q_p_list = []
        plr_np_list = []
        plr_p_list = []

        for _ in range(M):
            demand_sample = np.random.gamma(shape=gamma_shape, scale=gamma_scale, size=n)
            mu_hat = np.mean(demand_sample)
            sigma_hat = np.std(demand_sample, ddof=1)

            # Nonparametric estimator
            sorted_sample = np.sort(demand_sample)
            Q_np = sorted_sample[int(np.ceil(tau * n)) - 1]
            Q_np_list.append(Q_np)

            # Parametric estimator (misspecified as normal)
            Q_p = norm.ppf(tau, loc=mu_hat, scale=sigma_hat)
            Q_p_list.append(Q_p)


            Y_obs = np.random.gamma(shape=gamma_shape, scale=gamma_scale)
            R_star = nvp_formula(Q_star_gamma, Y_obs, c, p)
            R_np = nvp_formula(Q_np, Y_obs, c, p)
            R_p = nvp_formula(Q_p, Y_obs, c, p)

            plr_np_list.append(abs((R_star - R_np) / R_star))
            plr_p_list.append(abs((R_star - R_p) / R_star))


        Q_np_array = np.array(Q_np_list)
        Q_p_array = np.array(Q_p_list)
        rmse_np = np.sqrt(np.mean((Q_np_array - Q_star_gamma) ** 2))
        rmse_p = np.sqrt(np.mean((Q_p_array - Q_star_gamma) ** 2))
        plr_np = np.mean(plr_np_list)
        plr_p = np.mean(plr_p_list)

        all_results.append({
            'Scenario': 'Gamma_fitted_Normal',
            'n': n, 'tau': tau,
            'RMSE_NP': rmse_np, 'RMSE_P': rmse_p,
            'PLR_NP': plr_np, 'PLR_P': plr_p,
            'RMSE_ratio': rmse_np / rmse_p,
            'PLR_ratio': plr_np / plr_p
        })

# Exponential Distribution
for n in n_list:
    for tau in tau_list:
        c = c_base * (1 - tau)
        Q_star_exp = expon.ppf(tau, scale=exp_scale)

        Q_np_list = []
        Q_p_list = []
        plr_np_list = []
        plr_p_list = []

        for _ in range(M):
            demand_sample = np.random.exponential(scale=1 / exp_scale, size=n)
            mu_hat = np.mean(demand_sample)
            sigma_hat = np.std(demand_sample, ddof=1)

            # Nonparametric estimator
            sorted_sample = np.sort(demand_sample)
            Q_np = sorted_sample[int(np.ceil(tau * n)) - 1]
            Q_np_list.append(Q_np)

            # Parametric estimator (misspecified as normal)
            Q_p = norm.ppf(tau, loc=mu_hat, scale=sigma_hat)
            Q_p_list.append(Q_p)


            Y_obs = np.random.exponential(scale=1 / exp_scale)
            R_star = nvp_formula(Q_star_exp, Y_obs, c, p)
            R_np = nvp_formula(Q_np, Y_obs, c, p)
            R_p = nvp_formula(Q_p, Y_obs, c, p)

            plr_np_list.append(abs((R_star - R_np) / R_star))
            plr_p_list.append(abs((R_star - R_p) / R_star))


        Q_np_array = np.array(Q_np_list)
        Q_p_array = np.array(Q_p_list)
        rmse_np = np.sqrt(np.mean((Q_np_array - Q_star_exp) ** 2))
        rmse_p = np.sqrt(np.mean((Q_p_array - Q_star_exp) ** 2))
        plr_np = np.mean(plr_np_list)
        plr_p = np.mean(plr_p_list)

        all_results.append({
            'Scenario': 'Exponential_fitted_Normal',
            'n': n, 'tau': tau,
            'RMSE_NP': rmse_np, 'RMSE_P': rmse_p,
            'PLR_NP': plr_np, 'PLR_P': plr_p,
            'RMSE_ratio': rmse_np / rmse_p,
            'PLR_ratio': plr_np / plr_p
        })

# Poisson Distribution
for n in n_list:
    for tau in tau_list:
        c = c_base * (1 - tau)
        Q_star_poisson = poisson.ppf(tau, poisson_lambda)

        Q_np_list = []
        Q_p_list = []
        plr_np_list = []
        plr_p_list = []

        for _ in range(M):
            demand_sample = np.random.poisson(lam=poisson_lambda, size=n)
            mu_hat = np.mean(demand_sample)
            sigma_hat = np.std(demand_sample, ddof=1)

            # Nonparametric estimator
            sorted_sample = np.sort(demand_sample)
            Q_np = sorted_sample[int(np.ceil(tau * n)) - 1]
            Q_np_list.append(Q_np)

            # Parametric estimator (misspecified as normal)
            Q_p = norm.ppf(tau, loc=mu_hat, scale=sigma_hat)
            Q_p = round(Q_p)  # Round to nearest integer
            Q_p_list.append(Q_p)


            Y_obs = np.random.poisson(lam=poisson_lambda)
            R_star = nvp_formula(Q_star_poisson, Y_obs, c, p)
            R_np = nvp_formula(Q_np, Y_obs, c, p)
            R_p = nvp_formula(Q_p, Y_obs, c, p)

            if R_star != 0:
                plr_np_list.append(abs((R_star - R_np) / R_star))
                plr_p_list.append(abs((R_star - R_p) / R_star))
            else:
                plr_np_list.append(abs(R_star - R_np))
                plr_p_list.append(abs(R_star - R_p))


        Q_np_array = np.array(Q_np_list)
        Q_p_array = np.array(Q_p_list)
        rmse_np = np.sqrt(np.mean((Q_np_array - Q_star_poisson) ** 2))
        rmse_p = np.sqrt(np.mean((Q_p_array - Q_star_poisson) ** 2))
        plr_np = np.mean(plr_np_list)
        plr_p = np.mean(plr_p_list)

        all_results.append({
            'Scenario': 'Poisson_fitted_Normal',
            'n': n, 'tau': tau,
            'RMSE_NP': rmse_np, 'RMSE_P': rmse_p,
            'PLR_NP': plr_np, 'PLR_P': plr_p,
            'RMSE_ratio': rmse_np / rmse_p,
            'PLR_ratio': plr_np / plr_p
        })

# Normal Distribution (Control)
for n in n_list:
    for tau in tau_list:
        Q_star_val = norm.ppf(tau, loc=norm_mu, scale=norm_sigma)

        Q_np_list = []
        Q_p_list = []
        plr_np_list = []
        plr_p_list = []

        for _ in range(M):
            demand_sample = np.random.normal(loc=norm_mu, scale=norm_sigma, size=n)
            mu_hat = np.mean(demand_sample)
            sigma_hat = np.std(demand_sample, ddof=1)

            # Nonparametric estimator
            sorted_sample = np.sort(demand_sample)
            Q_np = sorted_sample[int(np.ceil(tau * n)) - 1]
            Q_np_list.append(Q_np)

            # Parametric estimator (correctly specified)
            Q_p = norm.ppf(tau, loc=mu_hat, scale=sigma_hat)
            Q_p_list.append(Q_p)


            Y_obs = np.random.normal(loc=norm_mu, scale=norm_sigma)
            R_star = nvp_formula(Q_star_val, Y_obs, c, p)
            R_np = nvp_formula(Q_np, Y_obs, c, p)
            R_p = nvp_formula(Q_p, Y_obs, c, p)

            plr_np_list.append(abs((R_star - R_np) / R_star))
            plr_p_list.append(abs((R_star - R_p) / R_star))


        Q_np_array = np.array(Q_np_list)
        Q_p_array = np.array(Q_p_list)
        rmse_np = np.sqrt(np.mean((Q_np_array - Q_star_val) ** 2))
        rmse_p = np.sqrt(np.mean((Q_p_array - Q_star_val) ** 2))
        plr_np = np.mean(plr_np_list)
        plr_p = np.mean(plr_p_list)

        all_results.append({
            'Scenario': 'Normal_fitted_Normal',
            'n': n, 'tau': tau,
            'RMSE_NP': rmse_np, 'RMSE_P': rmse_p,
            'PLR_NP': plr_np, 'PLR_P': plr_p,
            'RMSE_ratio': rmse_np / rmse_p,
            'PLR_ratio': plr_np / plr_p
        })


df_results = pd.DataFrame(all_results)
df_results.to_csv("task4_distribution_misspecification_TESTING2.1.csv", index=False)




# Count scenarios where nonparametric performs better
better_performance = df_results.groupby('Scenario').apply(lambda x: pd.Series({
    'RMSE_NP_wins': (x['RMSE_ratio'] < 1).sum(),
    'PLR_NP_wins': (x['PLR_ratio'] < 1).sum(),
    'Total_scenarios': len(x),
    'RMSE_win_pct': (x['RMSE_ratio'] < 1).mean() * 100,
    'PLR_win_pct': (x['PLR_ratio'] < 1).mean() * 100
}))


print("\nPercentage of scenarios where nonparametric estimator wins:")
print("-" * 55)
for scenario in better_performance.index:
    rmse_pct = better_performance.loc[scenario, 'RMSE_win_pct']
    plr_pct = better_performance.loc[scenario, 'PLR_win_pct']
    print(f"{scenario}:")
    print(f"  RMSE: {rmse_pct:.1f}% ({better_performance.loc[scenario, 'RMSE_NP_wins']}/{better_performance.loc[scenario, 'Total_scenarios']})")
    print(f"  PLR:  {plr_pct:.1f}% ({better_performance.loc[scenario, 'PLR_NP_wins']}/{better_performance.loc[scenario, 'Total_scenarios']})")