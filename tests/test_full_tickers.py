from cad_tickers.exchanges.all_tickers import mk_full_tickers


def test_source():
    tickers = mk_full_tickers()
    # fix this later
    assert len(tickers) > 80
