"""
Script to extract cryptocurrency data from CoinMarketCap API and load it into a DuckDB database.

This script implements an EL (Extract, Load) data pipeline that:
1. Extracts price data and market metrics for BTC, ETH, and LTC cryptocurrencies
2. Loads the data directly into a local DuckDB database

Requirements:
    - Python 3.9+
    - Libraries: dlt, logging, duckdb
    - CoinMarketCap API key (must be configured in .dlt/secrets.toml)

Author: Victor Antoniassi
Date: November 2024
"""

# Required libraries for API interaction, logging and database operations
import dlt
import logging
import duckdb
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.auth import APIKeyAuth


# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dlt.resource(name="latest_quotes_data")
def extract_and_load():
    """
    Main function that extracts data from CoinMarketCap API and prepares it for loading.
    
    This function:
    1. Authenticates with the API using a securely stored key
    2. Makes a request to get data for BTC, ETH, and LTC cryptocurrencies
    3. Loads the data directly into the database without transformations
    
    Yields:
        dict: Dictionary containing metrics for each cryptocurrency with the following keys:
            - symbol: Cryptocurrency symbol (e.g., BTC)
            - price: Current price in USD
            - volume_24h: Trading volume in the last 24 hours
            - market_cap: Market capitalization
            - last_updated: Last update timestamp
    """
    # Retrieve API key from dlt secrets configuration
    api_key = dlt.secrets["coinmarketcap.api_key"]
    
    # Set up authentication for CoinMarketCap API
    auth = APIKeyAuth(
        name="X-CMC_PRO_API_KEY",  # Header name required by CoinMarketCap
        api_key=api_key,           # API key from secrets
        location="header"          # Location to place the authentication
    )
    
    # Initialize REST client with API endpoint and auth settings
    client = RESTClient(
        base_url="https://pro-api.coinmarketcap.com/v1",
        auth=auth
    )

    # Make API request to get latest cryptocurrency quotes
    response = client.get(
        "/cryptocurrency/quotes/latest",
        params={
            "symbol": "BTC,ETH,LTC",  # Target cryptocurrencies
            "convert": "USD"           # Convert values to USD
        }
    )
    
    # Verify API response status
    if response.status_code != 200:
        logger.error(
            "API call error. Status: %s, Details: %s",
            response.status_code,
            response.text
        )
        response.raise_for_status()

    # Process each cryptocurrency in the API response
    for coin_data in response.json()["data"].values():
        # Extract USD quote data from the nested response structure
        quote = coin_data.get("quote", {}).get("USD", {})
        
        # Create data dictionary with required fields
        data = {
            "symbol": coin_data.get("symbol"),      # Cryptocurrency identifier
            "price": quote.get("price"),            # Current market price
            "volume_24h": quote.get("volume_24h"),  # 24-hour trading volume
            "market_cap": quote.get("market_cap"),  # Total market capitalization
            "last_updated": quote.get("last_updated")  # Last data update time
        }
        
        # Validate data before yielding
        if any(data.values()):
            yield data
        else:
            logger.warning(
                "Empty record ignored for: %s",
                coin_data.get("symbol")
            )


def run_pipeline():
    """
    Configure and execute the EL pipeline.
    
    This function:
    1. Creates a new dlt pipeline configured to use DuckDB
    2. Executes the pipeline with our extraction function
    3. Logs information about data loading
    """
    # Initialize pipeline with configuration parameters
    pipeline = dlt.pipeline(
        pipeline_name="crypto_quotes_pipeline",  # Unique identifier for the pipeline
        destination=dlt.destinations.duckdb(     # Configure DuckDB as the destination
            dlt.secrets["destination.duckdb_path"]
        ),
        dataset_name="quotes_data"              # Name of the target dataset
    )

    # Execute the pipeline and store loading results
    load_info = pipeline.run(extract_and_load)
    logger.info("Pipeline loading information: %s", load_info)


def query_data():
    """
    Function to query the data loaded in the DuckDB database.
    """
    # Connect to DuckDB and execute a sample query
    with duckdb.connect(dlt.secrets["destination.duckdb_path"]) as db:
        db.sql("SELECT * FROM quotes_data.latest_quotes_data").show()


if __name__ == "__main__":
    # Execute the pipeline and query the results
    run_pipeline()
    query_data()
