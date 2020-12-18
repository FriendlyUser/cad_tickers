from dataclasses import dataclass
from time import time

@dataclass
class SearchParams:
    '''Search Params for Ceo.ca intended to get spiels.'''
    channel: str = '@newswire'
    filter_terms: str = 'APHA'
    filter_top: int = 100
    load_more: str = 'top'
    original_scroll_height: str = 0
    # unix timestamp in millseconds
    until: int = int(time() * 1000) 

