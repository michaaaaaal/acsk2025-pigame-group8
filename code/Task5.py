import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import gamma, norm
from scipy.optimize import minimize_scalar


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)


bakery_data = pd.read_excel('./data/BakeryData2025_Vilnius.xlsx')


print(bakery_data)


stores = [col for col in bakery_data.columns if col not in ['date', 'weekday']]


bakery_long = bakery_data.melt(
    id_vars=['date', 'weekday'],
    var_name='store',
    value_name='demand'
)


bakery_long = bakery_long.dropna(subset=['demand'])


weekday_map = {
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday',
    7: 'Sunday'
}
bakery_long['weekday_name'] = bakery_long['weekday'].map(weekday_map)


print("Overall statistics:")
print(bakery_long['demand'].describe())


print("\nStatistics by store:")
store_stats = bakery_long.groupby('store')['demand'].describe()
store_stats['variance'] = bakery_long.groupby('store')['demand'].var()
print(store_stats)


print("\nStatistics by weekday:")
print(bakery_long.groupby('weekday_name')['demand'].describe())


print("\nStatistics by store and weekday:")
store_weekday_stats = bakery_long.groupby(['store', 'weekday_name'])['demand'].describe()
store_weekday_stats['variance'] = bakery_long.groupby(['store', 'weekday_name'])['demand'].var()

store_weekday_stats = store_weekday_stats.reset_index()
store_weekday_stats['weekday_name'] = pd.Categorical(
    store_weekday_stats['weekday_name'],
    categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    ordered=True
)
store_weekday_stats = store_weekday_stats.sort_values(['store', 'weekday_name'])
print(store_weekday_stats)

plt.figure(figsize=(12, 6))


plt.subplot(1, 2, 1)
sns.boxplot(x='store', y='demand', data=bakery_long)
plt.title('Daily Demand by Store')
plt.xticks(rotation=45)


plt.subplot(1, 2, 2)
sns.boxplot(x='weekday_name', y='demand', data=bakery_long,
            order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.title('Daily Demand by Weekday')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


plt.figure(figsize=(12, 6))
for store in bakery_long['store'].unique():
    store_data = bakery_long[bakery_long['store'] == store]
    plt.plot(store_data['date'], store_data['demand'], label=store)

plt.title('Demand Over Time by Store')
plt.xlabel('Date')
plt.ylabel('Demand')
plt.legend()
plt.show()


for store in stores:
    plt.figure(figsize=(12, 5))


    plt.plot(bakery_data['date'], bakery_data[store],
             label='Daily Demand', color='steelblue', alpha=0.7)


    if len(bakery_data[store].dropna()) > 7:
        moving_avg = bakery_data[store].rolling(window=7).mean()
        plt.plot(bakery_data['date'], moving_avg,
                 label='7-Day Average', color='darkorange', linewidth=2)


    plt.title(f'{store} Demand with Trend Line\n', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Demand', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.show()

#Anthony I think you missed task b but im not sure maybe i didnt find it
#i added it below

for store in stores:
    plt.figure(figsize=(8, 4))
    sns.histplot(data=bakery_long[bakery_long['store'] == store], x='demand', bins=20, kde=True)
    plt.title(f'Demand Distribution for {store}')
    plt.xlabel('Demand')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

