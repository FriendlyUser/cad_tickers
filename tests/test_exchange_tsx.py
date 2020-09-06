from cad_tickers.exchanges.tsx import (
    get_all_tsx_tickers,
    get_tsx_tickers,
    get_ticker_data,
    get_all_tickers_data,
)
import os
import pandas as pd


def test_get_tsx_tickers_tsx():
    tsx_tickers = get_tsx_tickers("tsx")
    assert len(tsx_tickers) > 500


def test_get_tsx_tickers_tsxv():
    tsxv_tickers = get_tsx_tickers("tsxv")
    assert len(tsxv_tickers) > 500


def test_get_tsx_tickers_diff_ex():
    try:
        get_tsx_tickers("cse")
        assert False
    except Exception as e:
        assert True


def test_get_ticker_data_art():
    data = get_ticker_data("art")
    assert data.get("symbol") == "art"


def test_get_all_tickers_data():
    data = get_all_tickers_data()
    assert isinstance(data, pd.DataFrame)
    assert len(data) > 2000
    found = data[data["symbol"].str.contains("BB")]
    assert len(found) >= 1
