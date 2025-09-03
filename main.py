# main.py
from scrapers.stock_scraper import fetch_stock_data
from scrapers.market_scraper import get_all_market_symbols
from storage.json_storage import save_to_json
import time

# --- Configuration Section ---
# Modify the settings below to control what data is fetched.

# 1. FETCH ALL STOCKS (True/False)
#    Set to True to fetch all A-share and HK-share stocks automatically.
#    If False, the script will use the manual STOCKS_TO_FETCH list below.
#
#    ############################################################################
#    # WARNING: Setting this to True is a HEAVY operation.                      #
#    # - It will attempt to fetch data for over 7000 stocks.                    #
#    # - This process can take MANY HOURS to complete.                          #
#    # - You may be temporarily IP-BANNED by the data source for making too     #
#    #   many requests in a short period.                                       #
#    # - For full-market scraping, running this on a server with a stable       #
#    #   connection overnight is recommended.                                   #
#    ############################################################################
FETCH_ALL_STOCKS = False  # <-- Set to True for full market scraping.

# 2. Manual list of stocks to fetch (used if FETCH_ALL_STOCKS is False).
STOCKS_TO_FETCH = [
    "600519",  # Kweichow Moutai (A-Share)
    "000001",  # Ping An Bank (A-Share)
    "00700",   # Tencent Holdings (HK-Share)
    "09988",   # Alibaba (HK-Share)
]

# 3. Set the desired data granularity.
#    Options: 'daily', '60' (for 60-minute data)
PERIOD = "daily"

# 4. Set the date range for the data.
#    Format: 'YYYYMMDD'
START_DATE = "20230101"
END_DATE = "20231231"

# 5. Set the directory where the output JSON files will be saved.
OUTPUT_DIR = "stock_data"


def main():
    """
    Main function to run the stock data scraping and saving process.
    """
    print("--- Starting Stock Data Scraping Job ---")

    symbols_to_process = []
    if FETCH_ALL_STOCKS:
        print("Mode: Fetching all market stocks.")
        print("WARNING: This will take a very long time. Please be patient.")
        time.sleep(5) # Give user time to read the warning
        symbols_to_process = get_all_market_symbols()
        if not symbols_to_process:
            print("Error: Failed to retrieve the list of market symbols. Exiting.")
            return
    else:
        print("Mode: Fetching stocks from manual list.")
        symbols_to_process = STOCKS_TO_FETCH

    print(f"\nConfiguration: Period='{PERIOD}', Start='{START_DATE}', End='{END_DATE}'")

    total_stocks = len(symbols_to_process)
    if total_stocks == 0:
        print("Stock list is empty. Nothing to do. Exiting.")
        return

    print(f"Total number of stocks to process: {total_stocks}")
    successful_fetches = 0

    for i, symbol in enumerate(symbols_to_process):
        print("-" * 50)
        print(f"Processing symbol: {symbol} ({i + 1}/{total_stocks})")

        # Step 1: Fetch data using our scraper function
        stock_df = fetch_stock_data(
            symbol=symbol,
            period=PERIOD,
            start_date=START_DATE,
            end_date=END_DATE
        )

        # Step 2: If data is valid, save it using our storage function
        if stock_df is not None and not stock_df.empty:
            save_to_json(
                df=stock_df,
                symbol=symbol,
                period=PERIOD,
                start_date=START_DATE,
                end_date=END_DATE,
                output_dir=OUTPUT_DIR
            )
            successful_fetches += 1
        else:
            print(f"Skipping save for {symbol} due to fetch failure or empty data.")

        # Add a small delay to be polite to the data source API
        time.sleep(1)

    print("-" * 50)
    print("\n--- Stock Data Scraping Job Finished ---")
    print(f"Successfully processed and saved data for {successful_fetches}/{total_stocks} stocks.")
    print(f"Data saved in '{OUTPUT_DIR}' directory.")


if __name__ == "__main__":
    main()
