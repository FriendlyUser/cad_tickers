import requests
from cad_tickers.exchanges.tsx.gql_data import GQL


def get_ticker_data(symbol=str) -> dict:
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
    allData = r.json()
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
