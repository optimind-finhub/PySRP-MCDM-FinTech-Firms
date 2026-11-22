# =========================================================
# FEATURES.PY
# Creates 12 innovative stock parameters from OHLCV data
# Output → all_stocks_features/stock_features.csv
# =========================================================

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------
DATA_FOLDER = "all_stocks_data"
OUTPUT_FOLDER = "all_stocks_features"
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "stock_features.csv")

ANALYSIS_DATE = "2025-12-31"   # Change anytime


# ---------------------------------------------------------
# CREATE OUTPUT FOLDER
# ---------------------------------------------------------
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


# ---------------------------------------------------------
# DATE WINDOWS
# ---------------------------------------------------------
end_date = datetime.strptime(ANALYSIS_DATE, "%Y-%m-%d")
start_3m = end_date - timedelta(days=90)
start_1y = end_date - timedelta(days=365)


# ---------------------------------------------------------
# LOAD STOCK FILE
# ---------------------------------------------------------
def load_stock(file):
    df = pd.read_csv(file)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df[df["Date"] <= end_date]
    return df.sort_values("Date")


# ---------------------------------------------------------
# CALCULATE 12 FEATURES
# ---------------------------------------------------------
def calculate_parameters(stock_name, df):

    df_3m = df[df["Date"] >= start_3m].copy()
    df_1y = df[df["Date"] >= start_1y].copy()

    # Need enough data
    if len(df_3m) < 40 or len(df_1y) < 200:
        return None

    df_3m["ret"] = df_3m["Close"].pct_change()
    df_3m["gap"] = (df_3m["Open"] - df_3m["Close"].shift(1)) / df_3m["Close"].shift(1)

    # =====================================================
    #  10 BUY-FAVOURABLE FEATURES (Higher = Good)
    # =====================================================

    #  Annual Trend Strength (CAGR %)
    ATS = ((df_1y["Close"].iloc[-1] / df_1y["Close"].iloc[0]) - 1) * 100

    #  Quarterly Return Momentum (%)
    QRM = ((df_3m["Close"].iloc[-1] / df_3m["Close"].iloc[0]) - 1) * 100

    #  Average Daily Range (₹ move per day)
    ADR = np.mean(df_3m["High"] - df_3m["Low"])

    #  Average Up Move (% gain on green days)
    green = df_3m[df_3m["Close"] > df_3m["Open"]]
    AUR = ((green["Close"] - green["Open"]) / green["Open"]).mean() * 100

    #  Volume Expansion Momentum (recent vs avg volume)
    VEM = df_3m["Volume"].iloc[-10:].mean() - df_3m["Volume"].mean()

    #  Higher High Frequency (count)
    HHF = (df_3m["High"].diff() > 0).sum()

    #  Up Gap Dominance (% total positive gap)
    UGD = df_3m[df_3m["gap"] > 0]["gap"].sum() * 100

    #  Recovery Velocity Score (₹ recovery after drops)
    close = df_3m["Close"].values
    recoveries = []
    for i in range(1, len(close)):
        if close[i] < 0.97 * close[i-1]:
            for j in range(i+1, len(close)):
                if close[j] >= close[i-1]:
                    recoveries.append(close[j] - close[i])
                    break
    RVS = np.mean(recoveries) if recoveries else 0

    #  Trend Stability Premium (Sharpe-like score)
    TSP = df_3m["ret"].mean() / (df_3m["ret"].std() + 1e-9) * 100

    # Price Holding Strength (days closing near high)
    PHS = (df_3m["Close"] > df_3m["Low"] +
          0.7*(df_3m["High"]-df_3m["Low"])).sum()

    # =====================================================
    #  2 RISK FEATURES (Higher = Bad)
    # =====================================================
    red = df_3m[df_3m["Close"] < df_3m["Open"]]

    #  Downside Damage Risk (% loss on red days)
    DDR = ((red["Open"] - red["Close"]) / red["Open"]).mean() * 100

    #  Gap Down Risk (% total negative gap)
    GDR = abs(df_3m[df_3m["gap"] < 0]["gap"].sum() * 100)

    return [stock_name, ATS, QRM, ADR, AUR, VEM, HHF, UGD, RVS, TSP, PHS, DDR, GDR]


# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
rows = []

for file in os.listdir(DATA_FOLDER):
    if file.endswith(".csv"):
        stock_name = file.replace(".csv", "")
        df = load_stock(os.path.join(DATA_FOLDER, file))
        result = calculate_parameters(stock_name, df)
        if result:
            rows.append(result)

columns = [
    "Stock",
    "ATS_%","QRM_%","ADR_Rs","AUR_%","VEM_Volume",
    "HHF_Count","UGD_%","RVS_Rs","TSP_Score","PHS_Days",
    "DDR_RISK_%","GDR_RISK_%"
]

final_df = pd.DataFrame(rows, columns=columns)
final_df.to_csv(OUTPUT_FILE, index=False)

print("\n Feature file created →", OUTPUT_FILE)
print(final_df)