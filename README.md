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
