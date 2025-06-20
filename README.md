# 📈 Stock Analysis Platform — Powered by YahooQuery

### 🔧 Backend-First Tool for Custom Financial Metric Extraction

As an amateur active investor, I often found myself needing deeper analysis than what free tools provide. Most platforms are either too expensive, or too limited. So I built this project to bridge that gap — a lightweight backend tool that lets you retrieve **custom financial metrics** from historical stock data, covering both **U.S. and Canadian tickers**.

---

## 🚀 Features

- 📊 Retrieve a wide range of metrics:
  - Geometric & arithmetic averages
  - Standard deviation, downside deviation
  - Sharpe, Sortino, and Treynor ratios
  - CAPM, Alpha, Beta
  - Value-at-Risk (VaR) and Conditional VaR
  - Positive period probability, drawdowns
  - Market cap, P/E ratios, dividend yield, and more
- 📦 Works with **daily, monthly, or annual frequencies**
- 🔍 Based on `yahooquery` (free & public Yahoo Finance API)
- ⚙️ Only computes the metrics you select — for **speed and efficiency**

---

## 🧠 Tech Stack

- Python 3.11+
- `yahooquery` for data retrieval
- `pandas` for time-series analysis
- Optional: `streamlit` for front-end prototyping (not included in repo)

---

## 🖥 Usage

```bash
# Clone the repo
git clone https://github.com/your-username/stock-analysis-platform.git
cd stock-analysis-platform

# Install dependencies
pip install -r requirements.txt

# Run analysis (example usage in app or script)
# Customize the attributes list as needed
```

# All the attributes available so far are the following:

```python
[
    "arith_avg", "geom_avg", "ema_avg", "stand_var", "sharpe", "sortino", "down_dev",
    "max_draw", "beta", "treynor", "capm", "alpha", "cvar_95", "cvar_975", "cvar_99",
    "var_95", "var_975", "var_99", "pos_prob", "min_return", "max_return",
    "market_cap", "trailing_pe", "forward_pe", "enterpriseValue", "sector", 
    "div_yield", "float_shares", "price_book", "real_start", "real_end"
    ]
```

### Example Usage

```python
from analysis import mainf

result = mainf(
    ticker="AAPL",
    attributes=["sharpe", "geom_avg", "market_cap"],
    start="2018-01-01",
    end="2023-01-01",
    freq="m"
)

print(result.head())

          AAPL
sharpe     0.2478
geom_avg   1.95%
market_cap 2.936T

```

---

## ⚡ Optional: Run the App with Streamlit

You can also explore the analysis tool through a local Streamlit interface.

### ▶️ Quick Start

```bash
# Install Streamlit if not already installed
pip install streamlit

# Run the Streamlit app (assuming you have a launch file)
streamlit run app/launch_app.py
```

## 🤝 Contributions Welcome
This project is still evolving, and contributions are highly appreciated!
I'm open to collaboration with:

- 🧠 Developers interested in expanding the metric library
- 🎨 Frontend/UI designers to build a tailored frontend app
- 🧪 Contributors who want to improve structure and robustness

Feel free to:

Fork the repo
Submit pull requests
Open issues or suggestions
