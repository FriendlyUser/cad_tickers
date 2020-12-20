import re
import datetime
import logging
from dataclasses import asdict
from typing import Type, Union
from cad_tickers.news.ceo import SearchParams

# create logger
module_logger = logging.getLogger(__name__) 

ceo_url = "https://ceo.ca"
art_pixel_height = 96
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
        logging.warning(e)
        return None

def earlier_timestamp(timestamp: int, days: int=90)-> int:
    """Update timestamp and return timestamp in millseconds"""
    timestamp = float(timestamp * 0.001)
    orig = datetime.datetime.fromtimestamp(timestamp)
    new = orig - datetime.timedelta(days=days)
    return int(new.timestamp() * 1000)

