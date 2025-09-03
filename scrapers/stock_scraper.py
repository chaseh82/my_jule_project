import akshare as ak
import pandas as pd
from typing import Literal

def _is_hk_stock(symbol: str) -> bool:
    """
    A simple helper to check if the stock symbol is for the Hong Kong market.
    HK stock codes are 5 digits long. A-share codes are 6 digits.
    """
    return len(symbol) == 5

def fetch_stock_data(
    symbol: str,
    period: Literal["daily", "60"] = "daily",
    start_date: str = "20200101",
    end_date: str = "20240101",
) -> pd.DataFrame | None:
    """
    Fetches historical stock data for a given stock symbol from AKShare.

    This function can fetch daily or 60-minute data for both A-shares and HK stocks.

    Args:
        symbol (str): The stock symbol.
                      e.g., "600519" for an A-share, "00700" for an HK stock.
        period (str): The data period. Supports 'daily' or '60' (for 60-minute).
                      Defaults to 'daily'.
        start_date (str): The start date in 'YYYYMMDD' format.
        end_date (str): The end date in 'YYYYMMDD' format.

    Returns:
        A pandas DataFrame with the stock data, or None if fetching fails.
    """
    print(f"Attempting to fetch data for symbol: {symbol}, period: {period}...")
    try:
        # We use 'qfq' for forward-adjusted prices, which is standard for historical analysis.
        adjust = "qfq"
        data_df = pd.DataFrame()

        if period == 'daily':
            if _is_hk_stock(symbol):
                data_df = ak.stock_hk_hist(symbol=symbol, period=period, start_date=start_date, end_date=end_date, adjust=adjust)
            else:
                data_df = ak.stock_zh_a_hist(symbol=symbol, period=period, start_date=start_date, end_date=end_date, adjust=adjust)

        elif period == '60':
            if _is_hk_stock(symbol):
                # Note: AKShare's HK minute data is for recent periods and doesn't support date ranges.
                print(f"Warning: HK 60-min data from AKShare is for recent periods and ignores date ranges.")
                data_df = ak.stock_hk_hist_min_em(symbol=symbol, period=period)
            else:
                # The minute-level API from Eastmoney requires a different date format.
                start_date_fmt = f"{start_date[:4]}-{start_date[4:6]}-{start_date[6:]}"
                end_date_fmt = f"{end_date[:4]}-{end_date[4:6]}-{end_date[6:]}"
                data_df = ak.stock_zh_a_hist_min_em(symbol=symbol, start_date=start_date_fmt, end_date=end_date_fmt, period=period, adjust=adjust)

        else:
            print(f"Error: Unsupported period '{period}'. Please use 'daily' or '60'.")
            return None

        if data_df.empty:
            print(f"Warning: No data returned for symbol {symbol} with period {period}. The symbol may be invalid or no data exists for the given dates.")
            return None

        print(f"Successfully fetched {len(data_df)} records for {symbol}.")
        return data_df

    except Exception as e:
        print(f"An error occurred while fetching data for {symbol}: {e}")
        return None
