import pandas as pd
from cad_tickers.util.utils import convert, tickers_to_ytickers
def test_convert():
    excel_df = convert('All.xlsx')
    assert(isinstance(excel_df, pd.DataFrame))

def test_parse_description_tags():
    pass

# Needs specific format for csvs
def test_tickers():
    pass 
    # ytickers = tickers_to_ytickers("TSXV.xlsx", "cse.xlsx")
    # assert len(ytickers) > 100
