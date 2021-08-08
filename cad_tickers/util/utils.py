import pandas as pd
import bs4
from typing import List


def transform_name_to_slug(raw_ticker: str) -> str:
    """
    Parameters:
      raw_ticker - cse ticker to be converted to slug
    Returns:
      transformed - raw_ticker
    """
    transformed = raw_ticker.lower().replace(".", "").replace(" ", "-")
    return transformed


def parse_description_tags(description_tags: List[bs4.element.Tag]) -> str:
    """
    Parameters:
      description_tags - html tags from webpage, usually p tag containing description
    Returns:
      description - description for ticker
    """
    if len(description_tags) > 0:
        description_tag = description_tags[0]
        # grab contents from desscription tag
        if len(description_tag.contents) == 0:
            return ""
        else:
            return description_tag.contents[0]
    # company does not have profile
    else:
        return ""


def extract_recent_news_links(modal_tags: List[bs4.element.Tag]) -> List[str]:
  """extracts new release modal from cse
  """
  urls = []
  for tag in modal_tags:
    attrs = tag.attrs
    data = attrs["href"]
    urls.append(data)
  return urls


def make_cse_path(raw_ticker: str, raw_industry: str) -> str:
    """makes slug for ticker for the cse

    Parameters:
      raw_ticker - cse ticker from xlsx sheet
      raw_industry - verbatim industry from ticker, not slugified
    Returns:
      description - url for cse files for download
    """
    if pd.isna(raw_industry):
        return ""
    # verify raw_industry is in industry do later
    cse_industries = [
        "Industry",
        "Mining",
        "Diversified Industries",
        "Life Sciences",
        "Oil and Gas",
        "Technology",
        "CleanTech",
    ]

    base_cse_url = "https://thecse.com/en/listings"
    industry = raw_industry.lower().replace(" ", "-")
    ticker = transform_name_to_slug(raw_ticker)
    url = f"{base_cse_url}/{industry}/{ticker}"
    return url


def read_df_from_file(file_path: str) -> pd.DataFrame:
    """
    Parameters:
      file_path - path to data
    Returns:
      df - excel sheet dataframe
    """
    try:
        df = pd.read_excel(file_path)
    except Exception:
        df = pd.read_csv(file_path)
    return df


def tickers_to_ytickers(tsx_path: str, cse_path: str) -> List[str]:
    """
    Parameters:
      tsx_path - path to clean tsx file
      cse_path - path to clean cse file
    Returns:
      ytickers - list of tickers
    """
    # grab tsx data
    tsx_df = read_df_from_file(tsx_path)
    tsx_df = tsx_df[["Ex.", "Ticker"]]
    ytickers_series = tsx_df.apply(tsx_ticker_to_yahoo, axis=1)
    ytickers_series = ytickers_series.drop_duplicates(keep="last")
    tsx_tickers = ytickers_series.tolist()

    cse_df = read_df_from_file(cse_path)
    cse_df = cse_df[["Symbol"]]
    ytickers_series = cse_df.apply(cse_ticker_to_yahoo, axis=1)
    ytickers_series = ytickers_series.drop_duplicates(keep="last")
    cse_tickers = ytickers_series.tolist()

    ytickers = [*tsx_tickers, *cse_tickers]
    return ytickers


def cse_ticker_to_yahoo(row: pd.Series) -> str:
    """
    Parameters:
      row - series from cse dataframe
    Returns:
      ticker - yahoo ticker for cse
    """
    ticker = row["Symbol"]
    return f"{ticker}.CN"


def tsx_ticker_to_yahoo(row: pd.Series) -> str:
    """
    Parameters:
      row - pd.Series
        * Ticker - ticker from pandas dataframe from cad_tickers
        * Ex. - what exchange the ticker is for
    Returns:
      yticker - yahoo finance ticker for tsx
    """
    ticker = row["Ticker"]
    exchange = row["Ex."]
    # 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly
    switcher = {"TSXV": "V", "TSX": "TO"}
    yahoo_ex = switcher.get(exchange, "TSXV")
    return f"{ticker}.{yahoo_ex}"


def cse_ticker_to_webmoney(cse_ticker: str):
    """
    Parameters:
      cse_ticker - cse ticker name
    Returns:
      webmoney_ticker - ticker that can be looked up in webmoney
    """
    return f"{cse_ticker}:CNX"


# make request with query params
