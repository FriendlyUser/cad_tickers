# todo split into smaller files
import requests
import re
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from cad_tickers.util import (
    parse_description_tags,
    extract_recent_news_links,
    make_cse_path,
    cse_ticker_to_webmoney,
)


def get_all_cse_tickers(cse_df: pd.DataFrame) -> list:
    """
    Parameters:
        cse_df - cleaned cse dataframe
    Returns:
        webmoney_tickers - list of webmoney cse tickers
    """
    try:
        tickers = cse_df["Symbol"].values.tolist()
        webmoney_tickers = [cse_ticker_to_webmoney(ticker) for ticker in tickers]
        return webmoney_tickers
    except Exception as e:
        print("FAILED TO GRAB TICKER FROM CSE_DF")
        print(e)
        return []


def get_cse_files(filename: str = "cse.xlsx", filetype: str = "xlsx") -> str:
    """Gets excel spreadsheet from api.tsx using requests

    Parameters:
      filename: Name of the file to be saved
      filetype: Save as pdf or xlsx

    Returns:
      filePath returns path to file

    See ://stackoverflow.com/questions/13567507/passing-csrftoken-with-python-requests

    """
    # TODO force it to be pdf or xlsx
    # https://www.thecse.com/export-listings/xlsx?f={}
    # https://www.thecse.com/export-listings/pdf?f={}
    URL = f"https://www.thecse.com/export-listings/{filetype}?f=" + r"{}"
    r = requests.get(URL)
    responseHeaders = r.headers
    if "text/html" in responseHeaders["Content-Type"]:
        return None
    elif any(
        re.findall(
            r"application/vnd.ms-excel|application/pdf|xlsx",
            responseHeaders["Content-Type"],
            re.IGNORECASE,
        )
    ):
        respData = r.content
        filepath = f"{filename}"
        with open(filepath, "wb") as s:
            s.write(respData)
        return filepath
    else:
        return None


def clean_cse_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Removes bad data from cse dataframe.

    Parameters:
      raw_df
        Dataframe with mostly unnamed columns from pandas df import

        =============  ====================================================================
        CSE Listings   Label for Company data
        Unnamed: 1     Listing symbol from the cse exchange needs a mapper to yahoo finance
        Unnamed: 2     Enum of industry including Mining
        Unnamed: 3     Enum such as CSE Composite
        Unnamed: 4     Enum such as CSE Composite
        Unnamed: 5     Usually CAD
        Unnamed: 6     empty (pandas import error, dropped)
        Unnamed: 7     Date when trading started
        =============  ====================================================================

    Returns:
      clean_df
        Dataframe with bad data removed

        ==========  ====================================================================
        Company     Full name of the company
        Symbol      Listing symbol from the cse exchange needs a mapper to yahoo finance
        Industry    Enum of industry including Mining
        Identifier  Broad category (US Cannabis)
        Indices     Enum such as CSE Composite
        Currency    Usually CAD
        Trading     Date when trading started
        urls        url to listing on cse website
        ==========  ====================================================================
    """
    # drop all nans
    df = raw_df
    df = df.dropna(axis=0, how="all")
    # drop empty column
    df = df.drop(df.columns[6], axis=1)
    # grab logically column names from first row
    column_labels = df.iloc[1, :].values.tolist()
    df.columns = column_labels
    # dropping title row and column titles row
    df = df.drop([df.index[0], df.index[1]])
    df = df.reset_index(drop=True)
    return df


def get_cse_tickers_df() -> pd.DataFrame:
    """Grab cse dataframe from exported xlsx sheet

    Returns:
      clean_df
        Dataframe with with randomly selected values. Data columns are as follows:

        ==========  ====================================================================
        Company     Full name of the company
        Symbol      Listing symbol from the cse exchange needs a mapper to yahoo finance
        Industry    Enum of industry including Mining
        Identifier  Broad category (US Cannabis)
        Indices     Enum such as CSE Composite
        Currency    Usually CAD
        Trading     Date when trading started
        urls        url to listing on cse website
        ==========  ====================================================================
    """
    URL = "https://www.thecse.com/export-listings/xlsx?f=" + r"{}"
    r = requests.get(URL)
    responseHeaders = r.headers
    if "text/html" in responseHeaders["Content-Type"]:
        return None
    elif any(
        re.findall(
            r"application/vnd.ms-excel|application/pdf|xlsx",
            responseHeaders["Content-Type"],
            re.IGNORECASE,
        )
    ):
        respData = r.content
        df = pd.read_excel(respData)
        clean_df = clean_cse_data(df)
        # add urls
        clean_df["urls"] = clean_df.apply(
            lambda x: make_cse_path(x["Company"], x["Industry"]), axis=1
        )
        return clean_df
    else:
        return None


def get_description_for_url(url: str) -> str:
    """
    Parameters:
      url - link to ticker can be empty string
    Returns:
      description - details of what the ticker does, can be empty string
    """
    if url == "":
        return ""
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, "lxml")
    description_selector = "#block-system-main div.company-description > p"
    description_tags = soup.select(description_selector)
    return parse_description_tags(description_tags)


def add_descriptions_to_df(df: pd.DataFrame, max_workers: int = 16) -> pd.DataFrame:
    """
    Parameters:
      clean_df
        Dataframe with with randomly selected values. Data columns are as follows:

        ==========  ====================================================================
        Company     Full name of the company
        Symbol      Listing symbol from the cse exchange needs a mapper to yahoo finance
        Industry    Enum of industry including Mining
        Identifier  Broad category (US Cannabis)
        Indices     Enum such as CSE Composite
        Currency    Usually CAD
        Trading     Date when trading started
        urls        url to listing on cse website
        ==========  ====================================================================

      max_workers
        maximum number of thread workers to have

    Returns:
      df
        Dataframe descriptions in every column if valid

        ===========  ====================================================================
        Company      Full name of the company
        Symbol       Listing symbol from the cse exchange needs a mapper to yahoo finance
        Industry     Enum of industry including Mining
        Identifier   Broad category (US Cannabis)
        Indices      Enum such as CSE Composite
        Currency     Usually CAD
        Trading      Date when trading started
        urls         url to listing on cse website
        description  cse description scrapped from website
        ===========  ====================================================================

    """
    urls = df["urls"].tolist()
    with ThreadPoolExecutor(max_workers=max_workers) as tpe:
        iterables = tpe.map(get_description_for_url, urls)
        descriptions = list(iterables)

    # use loop to set index values
    # df['description] = ''
    # for index, description in enumerate(descriptions):
    #   df.loc[index, 'description'] = description
    df["description"] = descriptions
    return df

def get_recent_docs_from_url(url: str) -> list:
    """
    Parameters:
      url - link to ticker can be empty string
    Returns:
      list - list of document urls with title
    """
    if url == "":
        return ""
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, "lxml")
    news_model = "group-cse-filings-content > view-listing-views item-link > a"
    description_tags = soup.select(news_model)
    return extract_recent_news_links(description_tags)


if __name__ == "__main__":
    from datetime import datetime
    import argparse

    start_time = datetime.now()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", help="file name (default: %(default)s)'", default="cse.xlsx"
    )
    parser.add_argument(
        "-t",
        "--type",
        default="xlsx",
        const="xlsx",
        nargs="?",
        choices=("xlsx", "pdf"),
        help="xlsx or pdf (default: %(default)s)",
    )
    cse_df = get_cse_tickers_df()
    cse_df.to_csv("cse.csv")
    # args = parser.parse_args()
    # cse_df = get_cse_tickers_df()
    # df = add_descriptions_to_df(cse_df)
    # end_time = datetime.now()
    # get_cse_files(args.file, args.type)
    # print(df)
