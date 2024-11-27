# CoinMarketCap API to DuckDB Pipeline

An Extract-Load (EL) pipeline that fetches cryptocurrency market data from CoinMarketCap's API and stores it in a [DuckDB](https://github.com/duckdb/duckdb) database using [dlt](https://github.com/dlt-hub/dlt).

![](https://cdn.some.pics/antoniassi/674796b3e5e93.png)

## 🎯 Features

- Extracts market data for cryptocurrencies (currently set to BTC, ETH, and LTC)
- Easily configurable to track any cryptocurrency available on CoinMarketCap
- Loads data directly into DuckDB 
- Includes error handling and logging
- Uses Python best practices
- Manages API keys securely with dlt secrets

## 🛠️ Technical Stack

- Python (3.9+)
- dlt
- DuckDB
- CoinMarketCap API

## 📊 Data Points

The pipeline collects these metrics for each cryptocurrency:
- Current price (USD)
- 24-hour trading volume
- Market capitalization
- Last update timestamp

## 🚀 Getting Started

### Prerequisites

1. Python 3.9 or higher
2. CoinMarketCap API key ([Get it here](https://coinmarketcap.com/api/))
3. Basic Python and database knowledge

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/coinmarketcap_api_to_duckdb.git
   cd coinmarketcap_api_to_duckdb
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up API credentials:
   - Create a `.dlt/secrets.toml` file
   - Add your API key:
     ```toml
     coinmarketcap.api_key = "your-api-key-here"
     destination.duckdb_path = "path/to/your/database.db"
     ```

### Usage

1. Run the pipeline as is:
   ```bash
   python dlt_to_duckdb.py
   ```

2. Or modify the cryptocurrency list in `dlt_to_duckdb.py`:
   ```python
   response = client.get(
       "/cryptocurrency/quotes/latest",
       params={
           "symbol": "BTC,ETH,LTC",  # Add or change cryptocurrencies here
           "convert": "USD"
       }
   )
   ```

The script will:
1. Connect to CoinMarketCap API
2. Get current market data
3. Save the data to DuckDB
4. Show the saved data

## 📁 Project Structure

```
coinmarketcap_api_to_duckdb/
├── .dlt/
│   └── secrets.toml          # API credentials
├── dlt_to_duckdb.py         # Main script
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

## 🔄 How It Works

1. **Auth**: Uses API key from `.dlt/secrets.toml`
2. **Extract**: Gets cryptocurrency data from API
3. **Validate**: Checks data quality
4. **Load**: Saves to DuckDB
5. **Verify**: Runs a test query

---

*Last updated: November 2024*
