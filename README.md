<div align="center">

# PySRP

### An open-source Python implementation and interactive web application of the Simple Ranking Process (SRP) for Multi-Criteria Decision-Making

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg)](LICENSE)

[Overview](#overview) •
[Features](#features) •
[Installation](#installation) •
[Quick start](#quick-start) •
[Input format](#input-format) •
[Python API](#python-api) •
[Case study](#case-study-indian-financial-stocks) •
[License](#license)

</div>

---

## Overview

**PySRP** implements the **Simple Ranking Process (SRP)**, a multi-criteria decision-making (MCDM) method that ranks alternatives by their rank positions on each criterion rather than by their raw values. Because it works on ranks, the method is not affected by differences in units or scale between criteria.

PySRP also includes the **MPSI** (variance-based) objective weighting method, so criterion weights can be derived from the data instead of being set by hand.

The software has two parts:

| Component | Description |
|---|---|
| **SRP-MCDM web app** (`SRP_STREAMLIT/`) | An interactive Streamlit application: upload a decision matrix, choose weights, and get rankings, audit tables, downloads and charts. No programming needed. |
| **Python modules** (`srp.py`, `mpsi.py`) | A small, dependency-light API (NumPy and pandas only) for use in scripts and notebooks. |

A worked case study is also included. It ranks ten Indian financial-sector stocks (NSE) on twelve engineered criteria, using `fetch.py` and `features.py`.

---

## Features

- **SRP ranking** with benefit and cost criteria
- **MPSI objective weights**: min-max normalisation, variance-based, with cost criteria inverted
- **Manual weights** as an alternative to MPSI
- **Tie handling** by competition ranking, so tied alternatives share the best rank of the group and no arbitrary tie-breaking is applied
- **Full audit trail**: ranking matrix (R), weighted ranking matrix (θ), total rank score (TRS) and final score (S) are all shown
- **CSV or Excel input** (`.csv`, `.xlsx`)
- **Export** of the final result, ranking matrix, weighted matrix and weights as CSV
- **Interactive charts** (Plotly) in five tabs: Ranking, SRP Scores, Heatmaps, Alternative Analysis and Criterion Comparison
- **Reproducible data pipeline** for the case study

---

## Method at a glance

For `m` alternatives and `n` criteria with weights `W_j`:

1. **Weights** `W_j` are supplied manually or computed by MPSI. Weights that already sum to 1 (within a tolerance of 1e-3) are used as given, and otherwise they are normalised.
2. **Ranking matrix** `R_ij`: rank 1 is the best. Benefit criteria are ranked descending and cost criteria ascending.
3. **Weighted ranking matrix** `θ_ij = W_j × R_ij`
4. **Total rank score** `TRS_i = Σ_j θ_ij`
5. **Final score** `S_i = m − TRS_i`
6. **Final rank**: alternatives are ordered by `S` descending, so the highest `S` gets rank 1.

<details>
<summary><b>MPSI weights (click to expand)</b></summary>

Each criterion column is min-max normalised, with cost criteria inverted so that higher is always better. Then:

- `P_j` = sum of squared deviations of the normalised column from its mean
- `W_j = P_j / Σ_k P_k`

A constant column gets zero variance. If all columns are constant, equal weights are used. `compute_mpsi` returns the weights at full precision (`Weight`) and rounded to 4 decimal places (`Weight_4dp`).

</details>

---

## Installation

**Requirements:** Python 3.11 or newer (the code was developed and tested with Python 3.11).

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/PySRP.git
cd PySRP

# 2. (Recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

| Package | Used for |
|---|---|
| `streamlit`, `plotly` | Web application and interactive charts |
| `pandas`, `numpy` | Core computation |
| `yfinance` | Downloading stock data (case study only) |
| `openpyxl`, `xlsxwriter` | Reading `.xlsx` input and writing Excel reports |

---

## Quick start

### Run the web application

```bash
cd SRP_STREAMLIT
streamlit run srp_streamlit.py
```

The app opens at `http://localhost:8501`. Run it from inside `SRP_STREAMLIT/` so that the custom theme in `.streamlit/config.toml` is picked up.

### Workflow in the app

| Step | Section | What you do |
|---|---|---|
| 1 | Upload Decision Matrix | Upload a `.csv` or `.xlsx` file |
| 2 | Decision Matrix | Check the parsed data |
| 3 | Criteria Settings | Set how many of the first columns are benefit criteria |
| 4 | MPSI Weight Calculation | View data-driven weights |
| 5 | Weight Selection | Use MPSI weights or enter your own |
| 6 | SRP Calculation | Run the ranking |
| 7–9 | R, θ and Final Ranking | Inspect each stage of the calculation |
| 10 | Calculation Audit | Verify the calculation |
| 11 | Download Results | Export results as CSV |
| 12 | Interactive Visualizations | Explore results in five tabs |

---

## Input format

A single table where:

- the **first column** holds the alternative names,
- the **remaining columns** are numerical criteria,
- **benefit criteria come first**, followed by **cost criteria** (set the number of benefit columns in step 3).

All criterion columns must be numeric, and the file needs at least two columns.

---

## Python API

The core classes can be used without the web interface.

```python
import sys
sys.path.append("SRP_STREAMLIT")

import pandas as pd
from srp import SRP
from mpsi import compute_mpsi

df = pd.DataFrame({
    "Alternative": ["A1", "A2", "A3", "A4"],
    "Profit":  [80, 65, 90, 70],
    "Quality": [7, 9, 6, 8],
    "Cost":    [200, 150, 260, 180],
}).set_index("Alternative")

directions = [1, 1, 0]                       # 1 = benefit, 0 = cost
weights = compute_mpsi(df, directions)       # MPSI weights

result = SRP(
    df.values,
    weights["Weight"].values,
    alternatives=list(df.index),
    n_benefit=2,                             # first 2 columns are benefit criteria
).rank()

print(result)
```

Output:

```
  Alternative     TRS       S  Rank
1          A2  2.0531  1.9469     1
3          A4  2.3510  1.6490     2
0          A1  2.6490  1.3510     3
2          A3  2.9469  1.0531     4
```

| Function / class | Purpose |
|---|---|
| `SRP(matrix, weights, alternatives=None, n_benefit=1)` | SRP ranking object. `.rank()` returns a DataFrame with `Alternative`, `TRS`, `S` and `Rank`. After `.rank()`, the ranking matrix `.R` and weighted matrix `.Theta` are also available. |
| `compute_mpsi(data, directions)` | Returns a DataFrame with `Criterion`, `Pj`, `Weight` and `Weight_4dp`. |
| `generate_excel_report(df_rank, R, Theta)` | Returns an Excel workbook (bytes) with the final ranking, ranking matrix and weighted matrix. |

---

## Case study: Indian financial stocks

The repository includes a reproducible pipeline that ranks ten NSE-listed financial stocks.

**Stocks:** HDFCBANK, ICICIBANK, KOTAKBANK, AXISBANK, SBIN, BAJFINANCE, BAJAJFINSV, PAYTM, POLICYBZR, CHOLAFIN

```
fetch.py  ──►  all_stocks_data/*.csv  ──►  features.py  ──►  all_stocks_features/stock_features.csv  ──►  SRP-MCDM app
```

```bash
# From the repository root
python fetch.py       # downloads daily OHLCV data from Yahoo Finance (internet required)
python features.py    # computes the 12 criteria
```

The generated data are already included, so the app can be tried without re-running these scripts. To change the stock list or dates, edit `STOCK_LIST` and `END_DATE` in `fetch.py` and `ANALYSIS_DATE` in `features.py`.

### The 12 criteria

Upload `all_stocks_features/stock_features.csv` to the app and set the number of benefit criteria to **10**.

<details>
<summary><b>Benefit criteria (higher is better)</b></summary>

| Code | Criterion |
|---|---|
| `ATS_%` | Annual Trend Strength: 1-year price return |
| `QRM_%` | Quarterly Return Momentum: 3-month return |
| `ADR_Rs` | Average Daily Range (High − Low) |
| `AUR_%` | Average Up Move: mean gain on up days |
| `VEM_Volume` | Volume Expansion Momentum: last-10-day volume vs 3-month average |
| `HHF_Count` | Higher High Frequency |
| `UGD_%` | Up Gap Dominance: total positive overnight gaps |
| `RVS_Rs` | Recovery Velocity Score: average recovery after drops of more than 3% |
| `TSP_Score` | Trend Stability Premium: Sharpe-like ratio of daily returns |
| `PHS_Days` | Price Holding Strength: days closing in the top 30% of the day's range |

</details>

<details>
<summary><b>Cost criteria (lower is better)</b></summary>

| Code | Criterion |
|---|---|
| `DDR_RISK_%` | Downside Damage Risk: mean loss on down days |
| `GDR_RISK_%` | Gap Down Risk: total negative overnight gaps |

</details>

---

## Repository structure

```
PySRP/
├── SRP_STREAMLIT/
│   ├── srp_streamlit.py    # Streamlit web application
│   ├── srp.py              # SRP algorithm
│   ├── mpsi.py             # MPSI weighting
│   ├── srp_export.py       # Excel report helper
│   └── .streamlit/
│       └── config.toml     # App theme
├── all_stocks_data/        # OHLCV CSVs (generated by fetch.py)
├── all_stocks_features/    # Criteria matrix (generated by features.py)
├── fetch.py                # Data download script
├── features.py             # Feature engineering script
├── requirements.txt
├── .gitignore
└── README.md
```

---

## License

This project is released under the **Creative Commons Zero v1.0 Universal (CC0 1.0)** license, which dedicates it to the public domain. See [`LICENSE`](LICENSE) for details.

---

<div align="center">
<sub>Data in the case study are downloaded from Yahoo Finance for research and demonstration purposes only and do not constitute financial advice.</sub>
</div>
