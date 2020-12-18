from dataclasses import asdict
from typing import Type
from cad_tickers.news.ceo import SearchParams

ceo_url = 'https://ceo.ca/api'

def params_to_dict(sp: Type[SearchParams]) -> dict:
    """utility function to get query parameters"""
    data = asdict(sp)
    data["filters[terms]"] = data.pop("filter_terms")
    data["filters[top]"] = data.pop("filter_top")
    return data