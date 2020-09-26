import json
import os
from cad_tickers.exchanges.classes import CSETicker, CSESedarFilings
from cad_tickers.sedar.cse import get_cse_sedar_docs


def test_get_sedar_docs_json():
    cmc_path = os.path.join("tests", "sample_data", "CMC.json")
    cmc_json = {}
    try:
        with open(cmc_path) as f:
            cmc_json = json.load(f)
    except Exception as e:
        print(e)
    # ensure that it can be imported into the filings object
    filings = get_cse_sedar_docs(cmc_json)
    cse_filings = CSESedarFilings(**filings)
    assert isinstance(cse_filings, CSESedarFilings)


def test_get_sedar_docs_json():
    cmc_path = os.path.join("tests", "sample_data", "CMC.json")
    cmc_json = {}
    try:
        with open(cmc_path) as f:
            cmc_json = json.load(f)
    except Exception as e:
        print(e)
    cse_ticker = CSETicker(**cmc_json)
    # ensure that it can be imported into the filings object
    filings = get_cse_sedar_docs(cse_ticker)
    cse_filings = CSESedarFilings(**filings)
    assert isinstance(cse_filings, CSESedarFilings)
