import requests
from datetime import datetime
from cad_tickers.exchanges.tsx.gql_data import GQL
from typing import Union


def get_ticker_filings(
    symbol: str,
    fromDate: str = datetime.today().replace(day=1).strftime("%Y-%m-%d"),
    toDate: str = datetime.today().strftime("%Y-%m-%d"),
    limit: int = 100,
) -> Union[dict, None]:
    """
    Parameters:
        symbol - ticker symbol from tsx, no prefix
        fromDate - start date to grab documents
        toDate - end date to grab documents
        limit - max number of documents to retrieve
    Returns:
        dict - :ref:`Quote By Symbol <quote_by_symbol_query>`
    """
    payload = GQL.get_company_filings_payload
    payload["variables"]["symbol"] = symbol
    payload["variables"]["fromDate"] = fromDate
    payload["variables"]["toDate"] = toDate
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
    art = get_ticker_filings(
        "ART", start_date="2015-11-11", end_date="2020-11-11", limit=108
    )
    print(art)
