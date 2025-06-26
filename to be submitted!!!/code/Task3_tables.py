import pandas as pd

df = pd.read_csv("./report/figures/task3/task3_simulation_results.csv")

rmse_pivot_p = df.pivot(index="n", columns="tau", values="RMSE (Parametric)")
rmse_pivot_np = df.pivot(index="n", columns="tau", values="RMSE (Nonparametric)")
rmse_pivot_ratio = df.pivot(index="n", columns="tau", values="RMSE ratio (Nonparametric / Parametric)")
plr_pivot_np = df.pivot(index="n", columns="tau", values="PLR (Nonparametric)")
plr_pivot_ratio = df.pivot(index="n", columns="tau", values="PLR ratio (Nonparametric / Parametric)")


output_path = "./report/figures/task3/task3_tables.xlsx"
with pd.ExcelWriter(output_path) as writer:
    rmse_pivot_p.to_excel(writer, sheet_name="RMSE Parametric")
    rmse_pivot_np.to_excel(writer, sheet_name="RMSE Nonparametric")
    rmse_pivot_ratio.to_excel(writer, sheet_name="RMSE Ratio")
    plr_pivot_np.to_excel(writer, sheet_name="PLR Nonparametric")
    plr_pivot_ratio.to_excel(writer, sheet_name="PLR Ratio")