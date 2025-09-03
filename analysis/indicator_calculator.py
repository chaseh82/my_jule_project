import pandas as pd
import pandas_ta as ta

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates a standard set of technical indicators for the given stock data
    using the pandas-ta library.

    Args:
        df (pd.DataFrame): A DataFrame with stock data. It is expected to contain
                           columns like '开盘', '最高', '最低', '收盘', '成交量'.
                           The column names in Chinese are mapped to English
                           standard names for processing.

    Returns:
        pd.DataFrame: The original DataFrame with new columns for each calculated
                      indicator. Returns the original DataFrame if it's empty or
                      if an error occurs.
    """
    if df.empty:
        print("Input DataFrame is empty, skipping indicator calculation.")
        return df

    # Create a copy to avoid modifying the original DataFrame unexpectedly
    df_processed = df.copy()

    # Standard column name mapping from Chinese to English for pandas-ta
    column_map = {
        '开盘': 'open',
        '最高': 'high',
        '最低': 'low',
        '收盘': 'close',
        '成交量': 'volume'
    }

    # Rename only the columns that exist in the DataFrame
    df_processed.rename(columns=column_map, inplace=True)

    # Define a standard strategy for calculating multiple indicators at once.
    # This can be easily configured or extended in the future.
    MyStrategy = ta.Strategy(
        name="Common Technical Indicators",
        description="A standard set of TA indicators including SMA, EMA, MACD, RSI, and Bollinger Bands.",
        ta=[
            {"kind": "sma", "length": 5},
            {"kind": "sma", "length": 10},
            {"kind": "sma", "length": 20},
            {"kind": "sma", "length": 60},
            {"kind": "ema", "length": 20},
            {"kind": "macd"},  # Uses default lengths: fast=12, slow=26, signal=9
            {"kind": "rsi"},   # Uses default length: 14
            {"kind": "bbands", "length": 20}, # Uses default std: 2
            {"kind": "obv"},
        ]
    )

    try:
        print("Calculating technical indicators...")
        # Apply the strategy. This appends new indicator columns to the DataFrame.
        df_processed.ta.strategy(MyStrategy)

        # The original DataFrame `df` has not been changed. We can merge the new
        # indicator columns back to it.
        # Identify new columns created by pandas-ta
        indicator_cols = [col for col in df_processed.columns if col not in df.columns and col not in column_map.values()]

        # Join the new indicator columns to the original DataFrame
        final_df = df.join(df_processed[indicator_cols])

        print(f"Successfully calculated and added {len(indicator_cols)} indicator columns.")
        return final_df

    except Exception as e:
        print(f"An error occurred during indicator calculation: {e}")
        # Return the original DataFrame if calculation fails
        return df
