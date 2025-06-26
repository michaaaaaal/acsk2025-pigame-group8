import pandas as pd
import matplotlib.pyplot as plt

file_path = "./report/figures/task4/task4_tables_simulated1000times.xlsx"
xls = pd.ExcelFile(file_path)

taus = [0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]
errors = {}

for sheet in xls.sheet_names:
    df = xls.parse(sheet)
    df = df.set_index(df.columns[0])
    errors[sheet] = df.loc["Absolute Error"].values

plt.figure(figsize=(10, 6))
for label, error_values in errors.items():
    plt.plot(taus, error_values, marker='o', label=label)

plt.title("Average Absolute Error vs. Quantile (τ)")
plt.xlabel("Quantile (τ)")
plt.ylabel("Absolute Error")
plt.xticks(taus)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
