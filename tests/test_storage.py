import json
import pandas as pd
from pathlib import Path

from storage.json_storage import save_to_json

def test_save_to_json(tmp_path: Path):
    """
    Tests the save_to_json function to ensure it correctly creates a JSON file
    with the expected content and naming convention.

    Args:
        tmp_path (Path): A pytest fixture that provides a temporary directory path.
    """
    # 1. Setup: Create sample data and define parameters
    data = {
        '日期': ['2023-01-01', '2023-01-02'],
        '开盘': [100.0, 102.0],
        '收盘': [101.0, 103.0]
    }
    sample_df = pd.DataFrame(data)

    symbol = "TEST01"
    period = "daily"
    start_date = "20230101"
    end_date = "20230102"

    # The function expects the output directory as a string
    output_dir = str(tmp_path)

    # 2. Action: Call the function we want to test
    save_to_json(
        df=sample_df,
        symbol=symbol,
        period=period,
        start_date=start_date,
        end_date=end_date,
        output_dir=output_dir
    )

    # 3. Assert: Check the results
    # a. Check if the file was created with the correct name
    expected_filename = f"{symbol}_{period}_{start_date}_to_{end_date}.json"
    file_path = tmp_path / expected_filename

    assert file_path.exists(), "The output JSON file was not created."
    assert file_path.is_file(), "The output path is not a file."

    # b. Check if the content of the file is correct
    with open(file_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)

    # Convert the original DataFrame to the same format for comparison
    expected_data = sample_df.to_dict(orient='records')

    assert saved_data == expected_data, "The data in the JSON file does not match the original DataFrame."
