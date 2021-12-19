from cad_tickers.exchanges.tsx import (
    get_all_tsx_tickers,
    get_tsx_tickers,
    get_ticker_data,
    get_all_tickers_data,
)
from cad_tickers.exchanges.cse import get_all_cse_tickers
import os
import pandas as pd
from io import StringIO

import time
def teardown_function(function):   # the function parameter is optional
    time.sleep(3)


def test_get_tsx_tickers_tsx():
    tsx_tickers = get_tsx_tickers("tsx")
    assert len(tsx_tickers) > 500


def test_get_all_tsx_tickers():
    tsx_tickers = get_all_tsx_tickers()
    assert len(tsx_tickers) > 1000


def test_get_tsx_tickers_tsxv():
    tsxv_tickers = get_tsx_tickers("tsxv")
    assert len(tsxv_tickers) > 500


def test_get_tsx_tickers_diff_ex():
    try:
        get_tsx_tickers("cse")
        assert False
    except Exception as e:
        assert True


# def test_get_ticker_data_art():
#     data = get_ticker_data("art")
#     assert data.get("symbol") == "ART"


# def test_get_ticker_data_cmc():
#     data = get_ticker_data("IP:CNX")
#     assert data.get("symbol") == "IP:CNX"
#     print(data)


# def test_get_ticker_data_NA():
#     try:
#         data = get_ticker_data("NA")
#     except Exception as e:
#         assert True


def test_get_all_tickers_data():
    data = get_all_tickers_data()
    assert isinstance(data, pd.DataFrame)
    assert len(data) > 1000
    found = data[data["symbol"].str.contains("BB")]
    assert len(found) >= 1


def test_webmoney_cse_tickers():
    raw_values = StringIO(
        """Company,Symbol,Industry,Identifier,Indices,Currency,Trading,urls
1933 Industries Inc.,TGIF,Diversified Industries,US Cannabis,CSE Composite,CAD,16-Jun-17,https://thecse.com/en/listings/diversified-industries/1933-industries-inc
Abattis Bioceuticals Corp.,ATT,Life Sciences,Cannabis,,CAD,01-Sep-15,https://thecse.com/en/listings/life-sciences/abattis-bioceuticals-corp
"Acreage Holdings, Inc.",ACRG.U,Life Sciences,US Cannabis,,USD,15-Nov-18,"https://thecse.com/en/listings/life-sciences/acreage-holdings,-inc"
Adastra Labs Holdings Ltd.,XTRX,Life Sciences,Cannabis,CSE Composite,CAD,06-Jan-20,https://thecse.com/en/listings/life-sciences/adastra-labs-holdings-ltd
    """
    )
    expected_list = ["TGIF:CNX", "ATT:CNX", "ACRG.U:CNX", "XTRX:CNX"]
    cse_df = pd.read_csv(raw_values)
    tickers = get_all_cse_tickers(cse_df)
    assert tickers == expected_list


def test_webmoney_cse_tickers_fail():
    raw_values = StringIO(
        """Company,Ticker,Industry,Identifier,Indices,Currency,Trading,urls
1933 Industries Inc.,TGIF,Diversified Industries,US Cannabis,CSE Composite,CAD,16-Jun-17,https://thecse.com/en/listings/diversified-industries/1933-industries-inc
Abattis Bioceuticals Corp.,ATT,Life Sciences,Cannabis,,CAD,01-Sep-15,https://thecse.com/en/listings/life-sciences/abattis-bioceuticals-corp
"Acreage Holdings, Inc.",ACRG.U,Life Sciences,US Cannabis,,USD,15-Nov-18,"https://thecse.com/en/listings/life-sciences/acreage-holdings,-inc"
Adastra Labs Holdings Ltd.,XTRX,Life Sciences,Cannabis,CSE Composite,CAD,06-Jan-20,https://thecse.com/en/listings/life-sciences/adastra-labs-holdings-ltd
    """
    )
    cse_df = pd.read_csv(raw_values)
    tickers = get_all_cse_tickers(cse_df)
    assert len(tickers) == 0
