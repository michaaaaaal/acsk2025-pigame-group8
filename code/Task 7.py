import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculateDemandDrop(rP):
    exp = np.exp(6 - (rP / 10))
    t1 = (1 + exp) ** -1
    rY = (t1 - 0.0025) * 100
    return rY
def adjustDemand(vY0, rY):
    df_adjusted = vY0.copy()
    demand_columns = ["main street A", "main street B", "station A", "station B"]
    scaling_factor = 1 - (rY / 100)
    df_adjusted[demand_columns] = df_adjusted[demand_columns] * scaling_factor
    return df_adjusted
def nonparametric_bootstrap_ci(data, cr, alpha=0.05, B=1000):
    q_star = np.quantile(data, cr)
    bootstrap_estimates = []
    n = len(data)
    for _ in range(B):
        sample = np.random.choice(data, size=n, replace=True)
        q_b = np.quantile(sample, cr)
        bootstrap_estimates.append(q_b)
    lower = np.quantile(bootstrap_estimates, alpha / 2)
    upper = np.quantile(bootstrap_estimates, 1 - alpha / 2)
    return q_star, (lower, upper)
def calculateOptimalOrderQuantity(df_adjusted, critical_ratio):
    demand_columns = ["main street A", "main street B", "station A", "station B"]
    Q = {}
    for store in demand_columns:
        adjusted_demand = df_adjusted[store].dropna()
        if len(adjusted_demand) > 0:
            q_star, _ = nonparametric_bootstrap_ci(adjusted_demand, critical_ratio)
            Q[store] = q_star
        else:
            Q[store] = 0
    return Q
def computeCurrentProfit(df, Q, c0, p0, pL, cS):
    store_columns = ["main street A", "main street B", "station A", "station B"]
    profit = {}
    for store in store_columns:
        demand = df[store].dropna()
        n = len(demand)
        profit_array = np.zeros(n)
        for i in range(n):
            actualSales = min(Q[store], demand.iloc[i])
            profit_array[i] = p0[store] * actualSales + (pL[store] - cS[store]) * max(Q[store] - demand.iloc[i], 0) - c0[store] * Q[store]
        profit[store] = profit_array.mean()
    return (profit["main street A"], profit["main street B"], profit["station A"], profit["station B"])
def computeNewProfit(df_adjusted, Q, c1, p1, pL, cS):
    store_columns = ["main street A", "main street B", "station A", "station B"]
    adjusted_profit = {}
    for store in store_columns:
        adjusted_demand = df_adjusted[store].dropna()
        n = len(adjusted_demand)
        adjusted_profit_array = np.zeros(n)
        for i in range(n):
            adjusted_sales = min(Q[store], adjusted_demand.iloc[i])
            adjusted_profit_array[i] = p1[store] * adjusted_sales + (pL[store] - cS[store]) * max(Q[store] - adjusted_demand.iloc[i], 0) - c1[store] * Q[store]
        adjusted_profit[store] = adjusted_profit_array.mean()
    return (adjusted_profit["main street A"], adjusted_profit["main street B"], adjusted_profit["station A"], adjusted_profit["station B"])
def findOptimalPriceIncrease(Q, vY0, c0, p0, rp_range, critical_ratio):
    current_profit = computeCurrentProfit(vY0, Q, c0, p0, pL, cS)
    start, stop, step = rp_range
    rp_values = np.arange(start, stop + step, step)
    best_rP_per_store = {}
    min_diff_per_store = {store: float("inf") for store in c0.keys()}
    for rP in rp_values:
        rY = calculateDemandDrop(rP)
        vY1 = adjustDemand(vY0, rY)
        c1 = {store: c0[store] * 1.25 for store in c0.keys()}
        p1 = {store: p0[store] * (1 + rP / 100) for store in p0.keys()}
        Q_new = calculateOptimalOrderQuantity(vY1, critical_ratio)
        new_profit = computeNewProfit(vY1, Q_new, c1, p1, pL, cS)
        for i, store in enumerate(c0.keys()):
            diff = abs(new_profit[i] - current_profit[i])
            if diff < min_diff_per_store[store]:
                min_diff_per_store[store] = diff
                best_rP_per_store[store] = rP
    return best_rP_per_store
def plotProfitVsPriceIncrease(rp_values, profits, current_profit, best_rP_per_store):
    plt.figure(figsize=(12, 8))  # Increased size for clarity with multiple lines
    store_columns = ["main street A", "main street B", "station A", "station B"]
    colors = ['b', 'g', 'r', 'c']  
    line_styles = ['--', '--', '--', '--']

    for i, store in enumerate(store_columns):
        store_profit = [p[i] for p in profits]
        optimal_rp = best_rP_per_store[store]
        label = "%s (Optimal rP: %.1f%%)" % (store, optimal_rp)
        plt.plot(rp_values, store_profit, label=label, color=colors[i])
        optimal_idx = np.abs(rp_values - optimal_rp).argmin()
        plt.plot(optimal_rp, store_profit[optimal_idx], 'ro', markersize=5) 
        plt.axhline(y=current_profit[i], color=colors[i], linestyle=line_styles[i],
                    label="%s (Current Profit: %.2f)" % (store, current_profit[i]))
    plt.xlabel("Price Increase (%)")
    plt.ylabel("Expected Profit")
    plt.title("Profit vs Price Increase")
    plt.legend()
    plt.grid(True)
    plt.show()
if __name__ == "__main__":
    df = pd.read_excel("C:/Users/Eigenaar/Downloads/BakeryData2025_Vilnius.xlsx")
    Q_values = {"main street A": 36.622, "main street B": 44.841, "station A": 59.399, "station B": 93.808}
    c0 = {'main street A': 3.85, 'main street B': 3.42, 'station A': 4.16, 'station B': 3.32}
    pL = {'main street A': 0.15, 'main street B': 0.15, 'station A': 0.15, 'station B': 0.15}
    cS = {'main street A': 0.11, 'main street B': 0.08, 'station A': 0.08, 'station B': 0.09}
    p0 = {'main street A': 4.64, 'main street B': 4.64, 'station A': 4.64, 'station B': 4.64}
    rp_range = (0, 65.0, 1.0)
    critical_ratio = {store: (p0[store] - c0[store]) / (p0[store] - pL[store] + cS[store]) for store in p0.keys()}
    current_profits = computeCurrentProfit(df, Q_values, c0, p0, pL, cS)
    print("Current profits are:", ", ".join(["%.2f" % p for p in current_profits]))
    optimal_rp = findOptimalPriceIncrease(Q_values, df, c0, p0, rp_range, next(iter(critical_ratio.values())))
    print("Optimal Price Increase per Store:", {k: f"{v:.2f}%" for k, v in optimal_rp.items()})
    all_profits = []
    for rp in np.arange(rp_range[0], rp_range[1] + rp_range[2], rp_range[2]):
        rY = calculateDemandDrop(rp)
        vY1 = adjustDemand(df, rY)
        c1 = {store: c0[store] * 1.25 for store in c0.keys()}
        p1 = {store: p0[store] * (1 + rp / 100) for store in p0.keys()}
        Q_new = calculateOptimalOrderQuantity(vY1, next(iter(critical_ratio.values())))
        new_profits = computeNewProfit(vY1, Q_new, c1, p1, pL, cS)
        all_profits.append(new_profits)
    plotProfitVsPriceIncrease(np.arange(rp_range[0], rp_range[1] + rp_range[2], rp_range[2]), all_profits, current_profits, optimal_rp)
