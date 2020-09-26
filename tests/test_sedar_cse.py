import json
import os
from cad_tickers.exchanges.classes import CSETicker, CSESedarFilings
from cad_tickers.sedar.cse import get_cse_sedar_docs, get_cse_ticker_data


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
    cse_filings = CSESedarFilings(filings.get("categories"), filings.get("list"))
    assert isinstance(cse_filings, CSESedarFilings)
    assert len(cse_filings.list) > 0


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
    cse_filings = CSESedarFilings(filings.get("categories"), filings.get("list"))
    assert isinstance(cse_filings, CSESedarFilings)
    assert len(cse_filings.list) > 0


def test_get_cse_ticker():
    cmc_dict = get_cse_ticker_data("CMC")
    assert isinstance(cmc_dict, dict)
    metatdata = cmc_dict.get("metatdata")
    assert isinstance(metatdata, dict)


def test_get_cse_ticker_class():
    cmc_obj = get_cse_ticker_data("CMC", False)
    assert isinstance(cmc_obj, CSETicker)
    assert isinstance(cmc_obj.metatdata, dict)
