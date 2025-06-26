import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("C:/Users/Eigenaar/Downloads/BakeryData2025_Vilnius.xlsx")
def calculateDemandDrop(rP):
    exp= np.exp(6-(rP/10))
    t1=(1+exp)**-1
    rY= (t1 - 0.0025)*100
    return rY
def adjustDemand(vY0,rY,):
    df_adjusted= df.copy()
    demand_column = ["main street A", "main street B", "station A", "station B"]
    scalingFactor = 1-(rY/100)
    df_adjusted[demand_column]= df_adjusted[demand_column]*scalingFactor
    return df_adjusted
def computeCurrentProfit(df,Q, c0,p0,):
   store_columns= ["main street A", "main street B", "station A", "station B"]
   profit={}
   for store in store_columns:
       demand=df[store].dropna()
       n=len(demand)
       profit_array=np.zeros(n)
       for i in range(n):
           actualSales= min(Q, demand.iloc[i])
           profit_array[i]= p0[store]*actualSales - c0[store]*Q
       profit[store]= profit_array.mean()
   return (profit["main street A"], profit["main street B"],profit["station A"], profit["station B"])
def computeNewProfit(df_adjusted, Q,c1,p1):
    store_columns = ["main street A", "main street B", "station A", "station B"]
    adjusted_profit={}
    for store in store_columns:
        adjusted_demand= df_adjusted[store].dropna()
        n=len(adjusted_demand)
        adjusted_profit_array= np.zeros(n)
        for i in range(n):
            adjusted_sales= min(Q, adjusted_demand.iloc[i])
            adjusted_profit_array[i]= p1[store] * adjusted_sales - c1[store]*Q
        adjusted_profit[store] = adjusted_profit_array.mean()
    return (adjusted_profit["main street A"], adjusted_profit["main street B"], adjusted_profit["station A"], adjusted_profit["station B"])
def findOptimalPriceIncrease(Q, vY0, c0,p0, rp_range):
    current_profit= computeCurrentProfit(vY0, Q, c0, p0)
    start, stop, step = rp_range
    rp_values= np.arange(start, stop+step, step)
    best_rP = None
    min_diff= float("inf")
    for rP in rp_values:
        rY = calculateDemandDrop(rP)
        vY1 = adjustDemand(vY0,rY)
        c1={store: c0[store]*1.25 for store in c0.keys()}
        p1={store: p0[store]* (1+(rP/100)) for store in p0.keys()}
        new_profit = computeNewProfit(vY1,Q,c1,p1)
        diff = np.mean(np.abs(np.array(new_profit) - np.array(current_profit)))
        if diff < min_diff:
            min_diff = diff
            best_rP = rP
    return best_rP
def plotProfitVsPriceIncrease(rp_values, profits, current_profit):
    plt.figure(figsize=(10,6))
    store_columns = ["main street A", "main street B", "station A", "station B"]
    for i, store in enumerate(store_columns):
        store_profit= [p[i] for p in profits]
        label= "%s (Current_Profit: %2f" % (store, current_profit[i])
        plt.plot(rp_values, store_profit, label=label)
    avg_current = sum(current_profit) / 4
    label= "%s (Current Profit: %2f)" %(store, current_profit[i])
    plt.axhline(y=avg_current, color="r", linestyle="--", label="Baseline")
    plt.xlabel("Price Increase (%)")
    plt.ylabel("Expected Profit")
    plt.title("Profit vs Price Increase")
    plt.legend()
    plt.grid(True)
    plt.show()
if __name__== "__main__":
    Q = 50
    c0 = {'main street A': 3.85, 'main street B': 3.42, 'station A': 4.16, 'station B': 3.32}
    p0 = {'main street A': 4.64, 'main street B': 4.64, 'station A': 4.64, 'station B': 4.64}
    rp_range = (10.0, 50.0, 1.0)
    current_profits = computeCurrentProfit(df, Q, c0, p0)
    print("Current profits are:", ", ".join(["%.2f" % p for p in current_profits]))
    optimal_rp = findOptimalPriceIncrease(Q, df, c0, p0, rp_range)
    print("Optimal Price Increase: %.2f%%" % optimal_rp)
    all_profits = []
    for rp in np.arange(rp_range[0], rp_range[1] + rp_range[2], rp_range[2]):
        rY = calculateDemandDrop(rp)
        vY1 = adjustDemand(df, rY)
        c1 = {store: c0[store] * 1.25 for store in c0.keys()}
        p1 = {store: p0[store] * (1 + rp / 100) for store in p0.keys()}
        new_profits = computeNewProfit(vY1,Q, c1, p1)
        all_profits.append(new_profits)

    plotProfitVsPriceIncrease(np.arange(rp_range[0], rp_range[1] + rp_range[2], rp_range[2]), all_profits,
                              current_profits)


