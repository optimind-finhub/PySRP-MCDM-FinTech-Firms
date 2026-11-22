# =========================================================
# FETCH.PY
# Download last 2 years OHLCV data for Indian Fintech Stocks
# Saves clean CSV → Date,Open,High,Low,Close,Volume
# =========================================================

import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# ---------------------------------------------------------
# 1. USER INPUT SECTION
# ---------------------------------------------------------

# Give the END DATE here (YYYY-MM-DD)
END_DATE = "2025-12-31"

# 10 Indian Fintech / Financial Stocks (NSE)
STOCK_LIST = [
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "KOTAKBANK.NS",
    "AXISBANK.NS",
    "SBIN.NS",
    "BAJFINANCE.NS",
    "BAJAJFINSV.NS",
    "PAYTM.NS",
    "POLICYBZR.NS",
    "CHOLAFIN.NS"
]

# Output folder
OUTPUT_FOLDER = "all_stocks_data"


# ---------------------------------------------------------
# 2. CREATE OUTPUT FOLDER
# ---------------------------------------------------------

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


# ---------------------------------------------------------
# 3. CALCULATE START DATE (2 YEARS BACK)
# ---------------------------------------------------------

end_date_dt = datetime.strptime(END_DATE, "%Y-%m-%d")
start_date_dt = end_date_dt - timedelta(days=730)

START_DATE = start_date_dt.strftime("%Y-%m-%d")

print("Downloading data from:", START_DATE, "to", END_DATE)


# ---------------------------------------------------------
# 4. DOWNLOAD & CLEAN FUNCTION
# ---------------------------------------------------------

def download_stock_data(ticker):
    try:
        print(f"Downloading {ticker} ...")

        df = yf.download(
            ticker,
            start=START_DATE,
            end=END_DATE,
            progress=False,
            auto_adjust=False
        )

        if df.empty:
            print(f"No data found for {ticker}")
            return

        # 🔥 Remove multi-level column header from yfinance
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Convert index to Date column
        df.reset_index(inplace=True)

        # Keep only required columns
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]

        # Remove timezone and keep only date
        df["Date"] = pd.to_datetime(df["Date"]).dt.date

        # Remove missing values
        df.dropna(inplace=True)

        # Save cleaned CSV
        file_path = os.path.join(OUTPUT_FOLDER, f"{ticker}.csv")
        df.to_csv(file_path, index=False)

        print(f"✅ Saved → {file_path}")

    except Exception as e:
        print(f"❌ Error downloading {ticker}: {e}")


# ---------------------------------------------------------
# 5. DOWNLOAD ALL STOCKS
# ---------------------------------------------------------

for stock in STOCK_LIST:
    download_stock_data(stock)

print("\n🎉 All stocks downloaded successfully!")