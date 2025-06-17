import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")

df = pd.read_csv("./report/figures/task3/task3_simulation_results.csv")

def plot_metric(df, y_col, title, filename, ylabel):
    plt.figure(figsize=(10, 6))
    for n_val in sorted(df["n"].unique()):
        subset = df[df["n"] == n_val]
        plt.plot(subset["tau"], subset[y_col], marker="o", label=f"n = {n_val}")
    plt.title(title)
    plt.xlabel("Service Level (τ)")
    plt.ylabel(ylabel)
    plt.legend(title="Sample Size")
    plt.tight_layout()
    plt.savefig(os.path.join("./report/figures/task3/", filename))
    plt.show()

# === Generate all requested plots ===
plot_metric(df, "RMSE (Parametric)", "RMSE (Parametric Estimator)", "rmse_parametric.png", "RMSE")
plot_metric(df, "RMSE (Nonparametric)", "RMSE (Nonparametric Estimator)", "rmse_nonparametric.png", "RMSE")
plot_metric(df, "RMSE ratio (Nonparametric / Parametric)", "RMSE Ratio (NP / P)", "rmse_ratio.png", "RMSE Ratio")
plot_metric(df, "PLR (Nonparametric)", "PLR (Nonparametric Estimator)", "plr_nonparametric.png", "PLR")
plot_metric(df, "PLR ratio (Nonparametric / Parametric)", "PLR Ratio (NP / P)", "plr_ratio.png", "PLR Ratio")


print("done")
