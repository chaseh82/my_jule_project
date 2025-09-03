# Stock Data Scraper & Analyzer

This project is a Python-based tool for scraping historical stock data for Chinese A-shares and Hong Kong stocks. It can fetch raw price data (Open, High, Low, Close, Volume) and automatically calculate a suite of common technical indicators, saving the enriched data to local JSON files.

## Key Features

- **Multi-Market Scraping**: Supports both Chinese A-shares (沪深A股) and Hong Kong stocks (港股).
- **Comprehensive Data**: Fetches historical price data and calculates over a dozen common technical indicators (MA, MACD, RSI, Bollinger Bands, etc.).
- **Flexible Scope**: Can be configured to fetch a small, manual list of stocks or the entire A-share and HK-share markets (over 7000+ stocks).
- **Configurable Timeframe**: Allows users to specify the exact start and end dates for historical data, as well as the granularity (daily or hourly).
- **Database-Friendly Output**: Saves data in a structured JSON format (`list of records`), ideal for importing into databases like MongoDB or for data analysis with pandas.
- **Test Suite**: Includes a suite of `pytest` unit tests to ensure the reliability and correctness of the core logic.

## Project Structure

```
.
├── analysis/               # Modules for calculating technical indicators
│   └── indicator_calculator.py
├── scrapers/               # Modules for scraping data
│   ├── market_scraper.py   # Scrapes the list of all stocks
│   └── stock_scraper.py    # Scrapes historical data for a single stock
├── storage/                # Modules for saving data
│   └── json_storage.py
├── tests/                  # Pytest unit tests
│   ├── test_analysis.py
│   ├── test_scrapers.py
│   └── test_storage.py
├── main.py                 # Main entry point and configuration script
├── requirements.txt        # Project dependencies
├── .gitignore              # Git ignore file
└── README.md               # This documentation file
```

## Setup & Installation

1.  **Prerequisites**: Ensure you have Python 3.8+ installed.
2.  **Install Dependencies**: Navigate to the project root directory and run the following command to install all required libraries:
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

All configuration is done by editing the variables in the **Configuration Section** at the top of the `main.py` file.

### Configuration Options in `main.py`

- `FETCH_ALL_STOCKS` (bool):
  - `True`: The script will ignore the manual list and attempt to fetch data for all A-share and HK-share stocks. **WARNING**: This is a very long process (potentially hours) and may get your IP address temporarily banned by the data source.
  - `False`: The script will only fetch data for the stocks listed in `STOCKS_TO_FETCH`. (Default)
- `STOCKS_TO_FETCH` (list): A manual list of stock symbols to process if `FETCH_ALL_STOCKS` is `False`.
- `PERIOD` (str): The data granularity. Use `'daily'` for daily data or `'60'` for 60-minute data.
- `START_DATE` / `END_DATE` (str): The date range for the data, in `'YYYYMMDD'` format.
- `CALCULATE_INDICATORS` (bool):
  - `True`: The script will calculate a standard set of technical indicators and add them to the data before saving. (Default)
  - `False`: The script will only save the raw OHLCV data.
- `OUTPUT_DIR` (str): The directory where the output JSON files will be saved. Defaults to `stock_data`.

### Running the Scraper

Once configured, run the script from the project's root directory:
```bash
python3 main.py
```
The script will print its progress to the console and save the output files in the directory specified by `OUTPUT_DIR`.

## How to Test

This project includes a suite of unit tests to verify the core logic.

### Running the Tests

To run the tests, navigate to the project's root directory and execute:
```bash
python3 -m pytest
```

**Note**: In some sandboxed or unusual environments, `pytest` may have trouble discovering the local modules. We have encountered this during development, resulting in `ModuleNotFoundError`. The standard solutions (`pytest.ini` and `sys.path` manipulation) were implemented to make the tests runnable in most standard environments.

## Output Data Format

The output data is saved in JSON files, with one file per stock. The format is a list of records (or objects), where each record represents a time period (e.g., a day). This format is highly compatible with data analysis tools and databases.

**Example record (with indicators):**
```json
{
    "日期": 1703808000000,
    "股票代码": "600519",
    "开盘": 1637.64,
    "收盘": 1643.64,
    "最高": 1667.22,
    "最低": 1637.64,
    "成交量": 27539,
    "SMA_5": 1629.5,
    "MACD_12_26_9": -5.3,
    "RSI_14": 45.8
    // ... and many other indicator columns
}
```
