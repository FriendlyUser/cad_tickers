from cad_tickers.sedar.tsx import get_ticker_filings


def test_get_tsx_docs():

    data = get_ticker_filings("ART")
    assert len(data.get("filings")) > 0
