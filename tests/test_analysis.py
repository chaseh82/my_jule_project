import pandas as pd
import pytest
import numpy as np

from analysis.indicator_calculator import calculate_indicators

@pytest.fixture
def sample_raw_stock_df():
    """
    Provides a sample raw stock DataFrame with enough data points for
    indicator calculation.
    """
    # Need enough data for a 60-period SMA, so at least 60 data points.
    data = {
        '开盘': np.random.uniform(95, 105, size=70),
        '最高': np.random.uniform(100, 110, size=70),
        '最低': np.random.uniform(90, 100, size=70),
        '收盘': np.random.uniform(98, 108, size=70),
        '成交量': np.random.uniform(10000, 50000, size=70),
    }
    df = pd.DataFrame(data)
    # Ensure high > low
    df['最高'] = df[['最高', '开盘', '收盘']].max(axis=1)
    df['最低'] = df[['最低', '开盘', '收盘']].min(axis=1)
    return df

def test_calculate_indicators(sample_raw_stock_df):
    """
    Tests the calculate_indicators function to ensure it adds indicator columns.
    """
    # 1. Action
    augmented_df = calculate_indicators(sample_raw_stock_df)

    # 2. Assertions
    # a. Check that the original DataFrame is not modified (since we work on a copy)
    assert len(sample_raw_stock_df.columns) == 5

    # b. Check that new columns have been added
    assert len(augmented_df.columns) > 5

    # c. Check for the presence of some expected indicator columns
    expected_cols = ['SMA_5', 'SMA_60', 'MACD_12_26_9', 'RSI_14', 'BBL_20_2.0']
    for col in expected_cols:
        assert col in augmented_df.columns, f"Expected column '{col}' not found in DataFrame."

    # d. Check that initial values for long-period indicators are NaN
    assert pd.isna(augmented_df['SMA_60'].iloc[58]), "SMA_60 should be NaN at row 58"
    assert not pd.isna(augmented_df['SMA_60'].iloc[59]), "SMA_60 should not be NaN at row 59"

    # e. Check that the original columns are still present
    for col in sample_raw_stock_df.columns:
        assert col in augmented_df.columns

def test_calculate_indicators_empty_df():
    """
    Tests that the function handles an empty DataFrame gracefully.
    """
    empty_df = pd.DataFrame()
    result_df = calculate_indicators(empty_df)
    assert result_df.empty
    assert len(result_df.columns) == 0
