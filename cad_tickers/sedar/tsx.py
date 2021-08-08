import requests
import json
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
        data=json.dumps(payload),
        headers={
            "authority": "app-money.tmx.com",
            "referer": f"https://money.tmx.com/en/quote/{symbol.upper()}",
            "locale": "en",
            "Content-Type": "application/json"
        },
    )
    try:
        if r.status_code == 403:
            print(r.text)
            return {}
        else:
            allData = r.json()
            print(allData)
            data = allData["data"]
            return data
    except KeyError as _e:
        print(_e, symbol)
        pass

# TODO rename this later
def get_news_and_events(
    symbol: str,
    page: int = 1,
    limit: int = 100,
    locale: str = "en",
) -> Union[dict, None]:
    """
    Parameters:
        symbol - ticker symbol from tsx, no prefix
        page - start date to grab documents
        limit - max number of documents to retrieve
        locale - language
    Returns:
        dict - :ref:`Quote By Symbol <quote_by_symbol_query>`
    """
    payload = GQL.get_company_news_events_payload
    payload["variables"]["symbol"] = symbol
    payload["variables"]["page"] = page
    payload["variables"]["limit"] = limit
    payload["variables"]["locale"] = locale
    url = "https://app-money.tmx.com/graphql"
    r = requests.post(
        url,
        data=json.dumps(payload),
        headers={
            "authority": "app-money.tmx.com",
            "referer": f"https://money.tmx.com/en/quote/{symbol.upper()}",
            "locale": "en",
            "Content-Type": "application/json"
        },
    )
    try:
        # check headings
        if r.status_code == 403:
            print(r.text)
            return {}
        else:
            allData = r.json()
            data = allData["data"]
            return data
    except KeyError as _e:
        return {}

if __name__ == "__main__":
    art = get_news_and_events(
        "PKK.CN", 1, 108
    )
    print(art)
