import pandas as pd
from pathlib import Path

def save_to_json(
    df: pd.DataFrame,
    symbol: str,
    period: str,
    start_date: str,
    end_date: str,
    output_dir: str = "stock_data"
) -> None:
    """
    Saves a DataFrame to a structured JSON file with a descriptive name.

    Args:
        df (pd.DataFrame): The DataFrame containing the stock data. It's expected
                           to have date-like columns as strings or datetime objects.
        symbol (str): The stock symbol (e.g., "600519").
        period (str): The data period (e.g., 'daily', '60').
        start_date (str): The start date used for fetching, in 'YYYYMMDD' format.
        end_date (str): The end date used for fetching, in 'YYYYMMDD' format.
        output_dir (str): The directory to save the JSON file in. Defaults to "stock_data".
    """
    try:
        # Ensure the output directory exists
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Construct a descriptive filename
        filename = f"{symbol}_{period}_{start_date}_to_{end_date}.json"
        filepath = output_path / filename

        print(f"Preparing to save data to: {filepath}")

        # For JSON serialization, it's safest to ensure datetime objects are strings.
        # AKShare often returns string dates, but this makes the function more robust.
        df_copy = df.copy()
        for col in df_copy.select_dtypes(include=['datetime64[ns]']).columns:
            df_copy[col] = df_copy[col].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Save to JSON using 'records' orientation for database-friendly format.
        # `force_ascii=False` ensures Chinese characters are saved correctly.
        df_copy.to_json(
            filepath,
            orient="records",
            indent=4,
            force_ascii=False
        )

        print(f"Successfully saved {len(df)} records to {filepath}")

    except Exception as e:
        print(f"An error occurred while saving data for {symbol} to JSON: {e}")
