from cad_tickers.exchanges.cse import get_cse_tickers_df, get_all_cse_tickers
from cad_tickers.exchanges.tsx import get_all_tsx_tickers, get_all_tickers_data
import pandas as pd


def mk_full_tickers() -> pd.DataFrame:
    """
      gets all tickers from the cse and tsx/tsxv using
      webmoney as a proxy

    Returns: full ticker df

    """
    cse_df = get_cse_tickers_df()
    cse_tickers = get_all_cse_tickers(cse_df)
    # tsx and tsxv tickers
    tsx_tickers = get_all_tsx_tickers()

    full_tickers = [
        *tsx_tickers,
        *cse_tickers,
    ]
    full_df = get_all_tickers_data(tickers=full_tickers)
    return full_df


if __name__ == "__main__":
    full_df = mk_full_tickers()
    full_df.to_csv("testing.csv")
