import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


bakery_data = pd.read_excel('./data/BakeryData2025_Vilnius.xlsx')
stores = [col for col in bakery_data.columns if col not in ['date', 'weekday']]
bakery_long = bakery_data.melt(id_vars=['date', 'weekday'], var_name='store', value_name='demand').dropna()
weekday_map = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
bakery_long['weekday_name'] = bakery_long['weekday'].map(weekday_map)


cost_data = {
    'main street A': {'c': 3.85, 'p': 4.64, 'c_S': 0.11, 'p_L': 0.15},
    'station B': {'c': 3.32, 'p': 4.64, 'c_S': 0.09, 'p_L': 0.15}
}

target_stores = ['main street A', 'station B']
target_days = ['Friday', 'Saturday', 'Sunday']
results = []


def normal_bootstrap_ci(data, cr, alpha=0.05, B=1000):
    n = len(data)
    mu, sigma = norm.fit(data)
    q_star = norm.ppf(cr, mu, sigma)

    bootstrap_estimates = []
    for _ in range(B):

        sample = norm.rvs(mu, sigma, size=n)

        mu_b, sigma_b = norm.fit(sample)
        q_b = norm.ppf(cr, mu_b, sigma_b)
        bootstrap_estimates.append(q_b)


    lower = np.quantile(bootstrap_estimates, alpha / 2)
    upper = np.quantile(bootstrap_estimates, 1 - alpha / 2)
    return q_star, (lower, upper)



for store in target_stores:
    for day in target_days:

        subset = bakery_long[
            (bakery_long['store'] == store) &
            (bakery_long['weekday_name'] == day)
            ]
        demand_data = subset['demand'].dropna()



        c = cost_data[store]['c']
        p = cost_data[store]['p']
        c_S = cost_data[store]['c_S']
        p_L = cost_data[store]['p_L']
        cr = (p - c) / (p - p_L + c_S)
        cr = np.clip(cr, 1e-5, 1 - 1e-5)


        q_star, ci = normal_bootstrap_ci(demand_data, cr)

        results.append({
            'store': store,
            'weekday': day,
            'critical_ratio': cr,
            'q_star': q_star,
            'ci_lower': ci[0],
            'ci_upper': ci[1]
        })


results_df = pd.DataFrame(results)
print(results_df[['store', 'weekday', 'critical_ratio', 'q_star', 'ci_lower', 'ci_upper']])



output_df = results_df[['store', 'weekday', 'critical_ratio', 'q_star', 'ci_lower', 'ci_upper']]

output_df['critical_ratio'] = output_df['critical_ratio'].round(4)
output_df['q_star'] = output_df['q_star'].round(3)
output_df['ci_lower'] = output_df['ci_lower'].round(3)
output_df['ci_upper'] = output_df['ci_upper'].round(3)

fig, ax = plt.subplots(figsize=(10, 4))

ax.axis('off')

table = ax.table(cellText=output_df.values,
                 colLabels=output_df.columns,
                 loc='center',
                 cellLoc='center')

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)

plt.tight_layout()

plt.savefig(
    'Figure_Normal.pdf',
    format='pdf',
    dpi=1200,
    facecolor='w'
)


main_street_results = results_df[results_df['store'] == 'main street A'].copy()

main_street_results['critical_ratio'] = main_street_results['critical_ratio'].round(4)
main_street_results['q_star'] = main_street_results['q_star'].round(3)
main_street_results['ci_lower'] = main_street_results['ci_lower'].round(3)
main_street_results['ci_upper'] = main_street_results['ci_upper'].round(3)

fig, ax = plt.subplots(figsize=(10, 3))

ax.axis('off')

table = ax.table(cellText=main_street_results[['weekday', 'critical_ratio', 'q_star', 'ci_lower', 'ci_upper']].values,
                 colLabels=['Weekday', 'Critical Ratio', 'Q*', 'CI Lower', 'CI Upper'],
                 loc='center',
                 cellLoc='center')

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)

plt.tight_layout()

plt.savefig(
    'Figure_Normal_MainStreetA.pdf',
    format='pdf',
    dpi=1200,
    facecolor='w'
)

plt.show()

print("\nResults for Main Street A:")
print(main_street_results[['weekday', 'critical_ratio', 'q_star', 'ci_lower', 'ci_upper']])
