import requests
import pandas as pd
from datetime import datetime
from cad_tickers.exchanges.tsx.get_ticker_data import get_ticker_data
from concurrent.futures import ThreadPoolExecutor

# since tsx lacks documentation
# unlikely that I can figure out what the other endpoints do
tsx_json_url = "https://www.tsx.com/json/company-directory/search"


def get_all_tsx_tickers() -> list:
    tsx_tickers = get_tsx_tickers()
    tsxv_tickers = get_tsx_tickers("tsxv")
    all_tsx = [*tsx_tickers, *tsxv_tickers]
    return all_tsx


def get_tsx_tickers(exchange="tsx") -> dict:
    """
    Function to get tsx tickers using the given json endpoint
    """
    if exchange not in ["tsxv", "tsx"]:
        raise Exception(f"Expect {exchange} as tsxv or tsx.")
    # get all tickers from endpoint
    endpoint = f"{tsx_json_url}/{exchange}/.*"
    r = requests.get(endpoint)
    data = r.json()
    results = data.get("results", [])
    # error out so I can fix the errors
    assert len(results) > 0
    symbol_list = []
    for result in results:
        symbol = result.get("symbol")
        symbol_list.append(symbol)
    num_results = data.get("length")
    assert num_results == len(symbol_list)
    return symbol_list


def get_all_tickers_data(max_workers: int = 16):
    tickers = get_all_tsx_tickers()
    ticker_data = []
    with ThreadPoolExecutor(max_workers=max_workers) as tpe:
        iterables = tpe.map(get_ticker_data, tickers)
        ticker_data = list(iterables)

    ticker_df = pd.DataFrame(ticker_data)
    return ticker_df


if __name__ == "__main__":
    startTime = datetime.now()
    data = get_all_tickers_data()
    data.to_csv("tsx_data.csv")
    print(data)
    print(datetime.now() - startTime)