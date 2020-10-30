import requests
from datetime import datetime
from cad_tickers.exchanges.tsx.gql_data import GQL
from typing import Union


def get_ticker_filings(
    symbol: str,
    start_date: str = datetime.today().replace(day=1).strftime("%Y-%m-%d"),
    end_date: str = datetime.today().strftime("%Y-%m-%d"),
    limit: int = 100,
) -> Union[dict, None]:
    """
    Parameters:
        symbol - ticker symbol from tsx, no prefix
    Returns:
        dict - :ref:`Quote By Symbol <quote_by_symbol_query>`
    """
    payload = GQL.get_company_filings_payload
    payload["variables"]["symbol"] = symbol
    payload["variables"]["start_date"] = start_date
    payload["variables"]["end_date"] = end_date
    payload["variables"]["limit"] = limit
    url = "https://app-money.tmx.com/graphql"
    r = requests.post(
        url,
        json=payload,
        headers={
            "authority": "app-money.tmx.com",
            "referer": f"https://money.tmx.com/en/quote/{symbol.upper()}",
            "locale": "en",
        },
    )
    allData = r.json()
    try:
        data = allData["data"]
        return data
    except KeyError as _e:
        print(_e, symbol)
        pass


if __name__ == "__main__":
    import json
    import os

    cmc = get_ticker_filings("ART")
