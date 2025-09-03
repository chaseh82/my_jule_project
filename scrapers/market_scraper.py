import akshare as ak
import pandas as pd
from typing import List

def get_all_market_symbols() -> List[str]:
    """
    Fetches the complete list of stock symbols for Chinese A-shares and Hong Kong shares.

    This function connects to the AKShare API to get real-time lists of all stocks
    from both markets and returns a combined list of their symbols.

    Returns:
        A list of all stock symbols as strings.
        Returns an empty list if the API calls fail.
    """
    print("Fetching all stock symbols for A-shares and HK-shares...")
    all_symbols: List[str] = []
    try:
        # 1. Fetch A-share symbols
        print("Fetching A-share list from data source...")
        ashare_df = ak.stock_zh_a_spot_em()
        if '代码' in ashare_df.columns:
            ashare_symbols = ashare_df['代码'].tolist()
            all_symbols.extend(ashare_symbols)
            print(f"Successfully fetched {len(ashare_symbols)} A-share stock symbols.")
        else:
            print("Warning: Could not find '代码' column in A-share data.")

        # 2. Fetch HK-share symbols
        print("Fetching HK-share list from data source...")
        hkshare_df = ak.stock_hk_spot_em()
        if '代码' in hkshare_df.columns:
            # The symbols are often returned correctly, but ensuring they are 5-digit strings is robust.
            hk_symbols = hkshare_df['代码'].astype(str).str.zfill(5).tolist()
            all_symbols.extend(hk_symbols)
            print(f"Successfully fetched {len(hk_symbols)} HK-share stock symbols.")
        else:
            print("Warning: Could not find '代码' column in HK-share data.")

        total_count = len(all_symbols)
        if total_count > 0:
            print(f"Total unique symbols fetched: {total_count}")
        else:
            print("Warning: Failed to fetch any stock symbols.")

        return all_symbols

    except Exception as e:
        print(f"An error occurred while fetching market symbol lists: {e}")
        return []
