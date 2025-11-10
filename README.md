# 💼 Crypto Portfolio Tracker

A Python-based cryptocurrency portfolio tracker with real-time prices from CoinGecko API.

## ✨ Features

- 📊 Track multiple cryptocurrencies
- 💰 Real-time price updates via CoinGecko API
- 📈 Calculate portfolio value & profit/loss
- 🎨 Beautiful CLI interface with colors
- 💾 Persistent storage (JSON file)
- ➕ Add/remove holdings
- 📉 View detailed portfolio stats
- 🔍 Search for coins by name or symbol

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/Ventolus/crypto-portfolio-tracker.git
cd crypto-portfolio-tracker
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Usage

Run the tracker:
```bash
python crypto_portfolio.py
```

### Menu Options:
1. **View Portfolio** - Display all holdings with current values
2. **Add Holding** - Search and add new cryptocurrency holdings
3. **Remove Holding** - Remove a holding from your portfolio
4. **Search Coin** - Search for cryptocurrencies
5. **Exit** - Close the application

## 📊 Example Output

```
====================================================================================================
💼 CRYPTO PORTFOLIO TRACKER
====================================================================================================

#   Symbol   Amount          Buy Price    Current      Value        P/L             24h       
----------------------------------------------------------------------------------------------------
1   BTC      0.5000          $45000.00    $67000.00    $33500.00    🟢 $11000.00 ( 32.84%)  📈  2.45%
2   ETH      10.0000         $2500.00     $3200.00     $32000.00    🟢  $7000.00 ( 28.00%)  📈  1.87%
3   SOL      50.0000         $100.00      $145.00      $7250.00     🟢  $2250.00 ( 45.00%)  📉 -0.52%
----------------------------------------------------------------------------------------------------

TOTAL PORTFOLIO VALUE:                   $72,750.00
Total Invested:                          $52,500.00
Total Profit/Loss:                       🟢 $20,250.00 (38.57%)
====================================================================================================
```

## 💾 Data Storage

Portfolio data is stored in `portfolio.json` in the same directory. This file contains:
- Your holdings (coin, amount, buy price)
- Transaction history
- Timestamps for each entry

## 🔧 Requirements

- Python 3.7+
- requests library

## 📝 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## ⚠️ Disclaimer

This tool is for tracking purposes only. Not financial advice. Always do your own research before investing.
