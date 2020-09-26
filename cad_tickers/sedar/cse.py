import requests
from cad_tickers.exchanges.classes import CSESedarFilings, CSETicker
from typing import Union


def get_cse_sedar_docs(cse_data: Union[dict, CSETicker]) -> CSESedarFilings:
    if isinstance(cse_data, CSETicker) or isinstance(cse_data, dict):
        if isinstance(cse_data, CSETicker):
            metatdata = cse_data.metatdata
        else:
            if "metatdata" in cse_data.keys():
                metatdata = cse_data.get("metatdata")
        sedar_filings_url = metatdata.get("sedar_filings")
        r = requests.get(sedar_filings_url)
        sedar_filings = r.json()
        filings = CSESedarFilings(**sedar_filings)
        return filings
    else:
        raise Exception("data misformatted")


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
