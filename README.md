# Simple script for querying cryptocurrency prices using the dlt library

This repository contains a Python script that demonstrates the use of the [dlt](https://github.com/dlt-hub/dlt) library, a library for data extraction and loading processes.
![](https://cdn.some.pics/antoniassi/674780c16f5e4.png)

## About the Script

The `dlt_to_duckdb.py` script implements an EL (Extract, Load) data pipeline that:

1. Extracts price and market metric data for the cryptocurrencies BTC, ETH, and LTC from the CoinMarketCap API.
2. Transforms the data into a structured format.
3. Loads the data into a local DuckDB database.

It uses the following Python libraries:

- `dlt`: The data load tool library, which provides abstractions for building data pipelines.
- `duckdb`: The DuckDB database, used as the destination for the data.
- `logging`: For configuring a logging system during script execution.

## Prerequisites for running the script

1. **Python 3.9+**
2. **Python Libraries**: `dlt`, `logging`, `duckdb`
3. [CoinMarketCap API Key](https://coinmarketcap.com/api/): Must be configured in the `secrets.toml` file of the DLT.

## Repository Structure

```
├── .dlt
│   └── secrets.toml
├── dlt_to_duckdb.py
└── requirements.txt
```

## Possible Improvements

- Explore other features of the dlt library, such as support for additional data sources and destinations.
- Add more advanced error handling and monitoring.
- Integrate the pipeline with dbt and workflow orchestration tools.
