import pandas as pd
import pytest
from unittest.mock import MagicMock

from scrapers.market_scraper import get_all_market_symbols
from scrapers.stock_scraper import fetch_stock_data, _is_hk_stock

# Test the helper function directly
def test_is_hk_stock():
    assert _is_hk_stock("00700") == True
    assert _is_hk_stock("99999") == True
    assert _is_hk_stock("600519") == False
    assert _is_hk_stock("000001") == False

# --- Tests for market_scraper.py ---

def test_get_all_market_symbols_success(mocker):
    """
    Tests get_all_market_symbols under normal conditions.
    """
    # 1. Setup: Create mock DataFrames
    mock_ashare_df = pd.DataFrame({'代码': ['600000', '000001']})
    mock_hkshare_df = pd.DataFrame({'代码': ['00700', '09988']})

    # 2. Mock: Patch the akshare functions
    mocker.patch('akshare.stock_zh_a_spot_em', return_value=mock_ashare_df)
    mocker.patch('akshare.stock_hk_spot_em', return_value=mock_hkshare_df)

    # 3. Action: Call the function
    symbols = get_all_market_symbols()

    # 4. Assert: Check if the returned list is correct
    expected_symbols = ['600000', '000001', '00700', '09988']
    assert symbols == expected_symbols

def test_get_all_market_symbols_api_error(mocker):
    """
    Tests get_all_market_symbols when an API call fails.
    """
    # Mock one of the functions to raise an error
    mocker.patch('akshare.stock_zh_a_spot_em', side_effect=Exception("API limit reached"))

    # Action & Assert
    assert get_all_market_symbols() == []


# --- Tests for stock_scraper.py ---

@pytest.fixture
def sample_stock_df():
    """A pytest fixture to provide a sample stock DataFrame for tests."""
    data = {'日期': ['2023-01-01'], '收盘': [100.0]}
    return pd.DataFrame(data)

def test_fetch_stock_data_daily_ashare(mocker, sample_stock_df):
    """Tests fetching daily data for an A-share stock."""
    mock_api = mocker.patch('akshare.stock_zh_a_hist', return_value=sample_stock_df)

    result_df = fetch_stock_data(symbol="600519", period="daily")

    mock_api.assert_called_once() # Check that the correct akshare function was called
    pd.testing.assert_frame_equal(result_df, sample_stock_df)

def test_fetch_stock_data_daily_hkshare(mocker, sample_stock_df):
    """Tests fetching daily data for an HK-share stock."""
    mock_api = mocker.patch('akshare.stock_hk_hist', return_value=sample_stock_df)

    result_df = fetch_stock_data(symbol="00700", period="daily")

    mock_api.assert_called_once()
    pd.testing.assert_frame_equal(result_df, sample_stock_df)

def test_fetch_stock_data_hourly_ashare(mocker, sample_stock_df):
    """Tests fetching hourly data for an A-share stock."""
    mock_api = mocker.patch('akshare.stock_zh_a_hist_min_em', return_value=sample_stock_df)

    result_df = fetch_stock_data(symbol="600519", period="60")

    mock_api.assert_called_once()
    pd.testing.assert_frame_equal(result_df, sample_stock_df)

def test_fetch_stock_data_api_error(mocker):
    """Tests that fetch_stock_data returns None when the API call fails."""
    mocker.patch('akshare.stock_zh_a_hist', side_effect=Exception("Network Error"))

    result = fetch_stock_data(symbol="600519", period="daily")

    assert result is None

def test_fetch_stock_data_empty_df(mocker):
    """Tests that fetch_stock_data returns None when the API returns an empty DataFrame."""
    empty_df = pd.DataFrame()
    mocker.patch('akshare.stock_zh_a_hist', return_value=empty_df)

    result = fetch_stock_data(symbol="600519", period="daily")

    assert result is None
