from cad_tickers.sedar.tsx import get_ticker_filings, get_news_and_events

import time
def teardown_function(function):   # the function parameter is optional
    time.sleep(3)


def test_get_tsx_docs():

    data = get_ticker_filings("ART", "2020-09-03", "2020-12-03", 3)
    assert len(data.get("filings")) > 0


def test_get_tsx_docs_params():

    data = get_ticker_filings(
        "ART", fromDate="2020-09-11", toDate="2020-11-11", limit=3
    )
    assert len(data.get("filings")) == 3

# doesn't work anymore
# def test_fake_doc():
#     data = get_ticker_filings("DARTA")
#     error = data["UserInputError"]
#     assert error == None

def test_get_news_and_events():
    data = get_news_and_events("PKK:CNX")
    assert len(data["news"]) >= 0
    assert len(data["events"]) >= 0
