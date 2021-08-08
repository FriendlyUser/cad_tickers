import requests
import json
from cad_tickers.exchanges.tsx.gql_data import GQL
from typing import Union


# TODO fix this later
# unlikely need this data, I think yahoo finance is good enough
# more consistent api
def get_ticker_data(symbol=str) -> Union[dict, None]:
    """
    Parameters:
        symbol - ticker symbol from tsx, no prefix
    Returns:
        dict - :ref:`Quote By Symbol <quote_by_symbol_query>`
    """
    payload = GQL.quote_by_symbol_payload
    payload["variables"]["symbol"] = symbol
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
    try:
        allData = r.json()
    except json.decoder.JSONDecodeError as error:
        print(error)
        print(f"Failed to decode data for {symbol}")
        print(r)
        return None
    # Check for errors
    try:
        data = allData["data"]["getQuoteBySymbol"]
        return data
    except KeyError as _e:
        print(_e, symbol)
        pass


if __name__ == "__main__":
    import pandas as pd

    data = get_ticker_data("art")
    series = pd.Series(data)
