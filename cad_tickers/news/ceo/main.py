import requests
from cad_tickers.news.ceo import SearchParams, ceo_url, params_to_dict

# get spiels from 
def get_spiels(params: dict):
    fetch_url = f"{ceo_url}/get_spiels"
    r = requests.get(fetch_url, params=params)
    print(r.url)


if __name__ == "__main__":

    default_sp = SearchParams(until=1608318681)
    default_params = params_to_dict(default_sp)
    y = params_to_dict(default_sp)
    x = {'channel': '@newswire', 'load_more': 'top', 'original_scroll_height': 0, 'until': 1608318681, 'filter[terms]': 'APHA', 'filter[top]': 100}
    assert y == x