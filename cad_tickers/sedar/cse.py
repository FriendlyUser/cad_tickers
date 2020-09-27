import requests
from cad_tickers.exchanges.classes import CSESedarFilings, CSETicker
from typing import Union
from cad_tickers.util import make_cse_path


def get_cse_ticker_data(ticker, get_dict: bool = True) -> Union[CSETicker, dict]:
    """
    Parameters:
        ticker - stock ticker for the cse without exchange (ex, CMC)
        get_dict - flag to get dict
    Returns:
        cse_ticker - dict or python class containing ticker data
    """
    ticker_url = f"https://webapi.thecse.com/trading/listed/securities/{ticker}.json"
    r = requests.get(ticker_url)
    data = r.json()

    if get_dict == True:
        return data
    return CSETicker(**data)


def get_cse_sedar_docs(
    cse_data: Union[dict, CSETicker]
) -> Union[dict, CSESedarFilings]:
    """
    Parameters:
      cse_data - information for a ticker when it is loaded on the thecse website
    Returns:
      filings - class or dict with properties :class:`cad_tickers.exchanges.classes.CSESedarFilings`
    """
    if isinstance(cse_data, CSETicker) or isinstance(cse_data, dict):
        if isinstance(cse_data, CSETicker):
            metatdata = cse_data.metatdata
        else:
            if "metatdata" in cse_data.keys():
                metatdata = cse_data.get("metatdata")
        sedar_filings_url = metatdata.get("sedar_filings")
        r = requests.get(sedar_filings_url)
        sedar_filings = r.json()
        return sedar_filings
    else:
        raise Exception("data misformatted must be dict or cse ticker")


if __name__ == "__main__":
    import json
    import os

    cmc_path = os.path.join("tests", "sample_data", "CMC.json")
    cmc_json = {}
    try:
        with open(cmc_path) as f:
            cmc_json = json.load(f)
    except Exception as e:
        print(e)
    fillings = get_cse_sedar_docs(cmc_json)
    cmc = get_cse_ticker_data("CMC")
