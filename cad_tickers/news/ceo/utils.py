from dataclasses import asdict, replace
from typing import Type, Union
from cad_tickers.news.ceo import SearchParams
import re

ceo_url = "https://ceo.ca"

def params_to_dict(sp: Type[SearchParams]) -> dict:
    """utility function to get query parameters"""
    data = asdict(sp)
    data["filters[terms]"] = data.pop("filter_terms")
    data["filters[top]"] = data.pop("filter_top")
    return data

def news_link_from_spiel(spiel: dict)-> Union[str, None]:
    spiel = spiel.get('spiel')
    try:
        found = re.search('@[a-zA-Z0-9/-]+', spiel)
        return f"{ceo_url}/{found.group(0)}"
    except AttributeError as e:
        print(e)
        return None