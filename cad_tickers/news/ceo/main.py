import requests
from cad_tickers.news.ceo import SearchParams, ceo_url, params_to_dict
from typing import Tuple, List

# get spiels from 
def get_spiels(params: dict)-> dict:
    """Simple function to get ceo.ca spiels"""
    fetch_url = f"{ceo_url}/api/get_spiels"
    r = requests.get(fetch_url, params=params)
    data = r.json() 
    return data

def extract_urls(data: List[dict])-> Tuple[list, dict]:
    spiels = data.get('spiels')
    spiels_text = [spiel.get('spiel') for spiel in spiels]
    return "", ""

def get_new_items(ticker: str, max_iterations = 10):
    """Gets news items from ceo using ticker

        Parameters:
            ticker - stock ticker, for example APHA
            max_iterations - max number of requests to ceo.ca
    """
    sp = SearchParams(filter_terms=ticker)
    latest_timestamp = None
    data_urls = []
    pass


# Function that selectors any article class and then returns all the text, alternatively can use sumpy for a well
# formed pages like ceo.ca
if __name__ == "__main__":

    # default_sp = SearchParams(until=1593091936374)
    # default_params = params_to_dict(default_sp)
    # data = get_spiels(default_params)
    # extract_urls(data)
    pass