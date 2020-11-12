from cad_tickers.sedar.tsx import get_ticker_filings


def test_get_tsx_docs():

    data = get_ticker_filings("ART")
    assert len(data.get("filings")) > 0


def test_get_tsx_docs_params():

    data = get_ticker_filings(
        "ART", fromDate="2015-11-11", toDate="2020-11-11", limit=3
    )
    assert len(data.get("filings")) == 3


def test_fake_doc():
    data = get_ticker_filings("DART")
    error = data["UserInputError"]
    assert error == None