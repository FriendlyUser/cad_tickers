from cad_tickers.sedar.tsx import get_ticker_filings, get_news_and_events


data = get_ticker_filings(
    "PKK:CSX", fromDate="2020-09-11", toDate="2020-11-11", limit=3
)