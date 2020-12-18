import requests
from cad_tickers.news.ceo import SearchParams, ceo_url, params_to_dict

# get spiels from 
def get_spiels(params: dict):
    fetch_url = f"{ceo_url}/get_spiels"
    r = requests.get(fetch_url, params=params)
    print(r.url)
    data = r.json() 
    print(data)


if __name__ == "__main__":

    default_sp = SearchParams(until=1593091936374)
    default_params = params_to_dict(default_sp)
    data = get_spiels(default_params)