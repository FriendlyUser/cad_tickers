import requests
import cad_tickers.exchanges.tsx.gql_data as gql


def get_ticker_data(symbol=str) -> str:
    payload = gql.quote_by_symbol_payload
    payload["variables"]["symbol"] = symbol
    url = "https://app-money.tmx.com/graphql"
    r = requests.post(url, json=payload)
    allData = r.json()
    # Check for errors
    data = allData["data"]["getQuoteBySymbol"]
    return data


if __name__ == "__main__":
    import pandas as pd

    data = get_ticker_data("art")
    series = pd.Series(data)
