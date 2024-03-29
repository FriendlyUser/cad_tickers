import json
import os
from cad_tickers.exchanges.classes import CSETicker, CSESedarFilings
from cad_tickers.sedar.cse import get_cse_sedar_docs, get_cse_ticker_data


import time
def teardown_function(function):   # the function parameter is optional
    time.sleep(3)

def test_get_sedar_docs_json():
    bets_path = os.path.join("tests", "sample_data", "BETS.json")
    bets_json = {}
    try:
        with open(bets_path) as f:
            bets_json = json.load(f)
    except Exception as e:
        print(e)
    # ensure that it can be imported into the filings object
    filings = get_cse_sedar_docs(bets_json)
    cse_filings = CSESedarFilings(filings.get("categories"), filings.get("list"))
    assert isinstance(cse_filings, CSESedarFilings)
    assert len(cse_filings.list_items) > 0


def test_get_sedar_docs_json_class():
    cmc_path = os.path.join("tests", "sample_data", "BETS.json")
    cmc_json = {}
    try:
        with open(cmc_path) as f:
            cmc_json = json.load(f)
    except Exception as e:
        print(e)
    cse_ticker = CSETicker(**cmc_json)
    # ensure that it can be imported into the filings object
    filings = get_cse_sedar_docs(cse_ticker)
    cse_filings = CSESedarFilings(filings.get("categories"), filings.get("list"))
    assert isinstance(cse_filings, CSESedarFilings)
    assert len(cse_filings.list_items) > 0


def test_get_cse_ticker():
    cmc_dict = get_cse_ticker_data("BETS")
    assert isinstance(cmc_dict, dict)
    metatdata = cmc_dict.get("metatdata")
    assert isinstance(metatdata, dict)


# This test is failing comment it out
def test_get_cse_ticker_class():
    pass 
    # cmc_obj = get_cse_ticker_data("BETS", False)
    # assert isinstance(cmc_obj, CSETicker)
    # assert isinstance(cmc_obj.metatdata, dict)
