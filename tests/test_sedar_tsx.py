from cad_tickers.sedar.tsx import get_ticker_filings, get_news_and_events


def test_get_tsx_docs():

    data = get_ticker_filings("ART", "2018-03-03", "2020-12-03", 108)
    print(data)
    assert len(data.get("filings")) > 0


def test_get_tsx_docs_params():

    data = get_ticker_filings(
        "ART", fromDate="2015-11-11", toDate="2020-11-11", limit=3
    )
    assert len(data.get("filings")) == 3

# doesn't work anymore
# def test_fake_doc():
#     data = get_ticker_filings("DARTA")
#     error = data["UserInputError"]
#     assert error == None

def test_get_news_and_events():
    data = get_news_and_events("PKK.CN")
    print(data)
    assert len(data["data"]["news"]) > 0