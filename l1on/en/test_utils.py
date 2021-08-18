import pandas as pd
import os
from cad_tickers.util.utils import (
    read_df_from_file,
    tickers_to_ytickers,
    cse_ticker_to_yahoo,
    tsx_ticker_to_yahoo,
)


def test_read_df_from_file():
    csv_file = os.path.join("tests", "sample_data", "references.csv")
    excel_df = read_df_from_file(csv_file)
    assert isinstance(excel_df, pd.DataFrame)


def test_parse_description_tags():
    pass


# Needs specific format for csvs
def test_tickers():
    ytickers = tickers_to_ytickers(
        "tests/sample_data/tsx.csv", "tests/sample_data/cse.csv"
    )
    assert len(ytickers) == 7


def test_cse_to_ticker():
    ser = pd.Series(["IP"], index=["Symbol"])
    cn_ticker = cse_ticker_to_yahoo(ser)
    assert cn_ticker == "IP.CN"


def test_tsx_to_ticker():
    ser = pd.Series(["TSX", "BB"], index=["Ex.", "Ticker"])
    cn_ticker = tsx_ticker_to_yahoo(ser)
    assert cn_ticker == "BB.TO"
