import requests
import time
from cad_tickers.news.ceo import SearchParams, ceo_url, \
    news_link_from_spiel, \
    params_to_dict

from cad_tickers.news.ceo.utils import art_pixel_height, earlier_timestamp, module_logger
from typing import Tuple, List
from dataclasses import replace
# get spiels from 
def get_spiels(params: dict)-> dict:
    """Simple function to get ceo.ca spiels"""
    fetch_url = f"{ceo_url}/api/get_spiels"
    r = requests.get(fetch_url, params=params)
    # print(r.url)
    data = r.json() 
    return data

def extract_urls(spiels: List[dict])-> Tuple[list, str]:
    """Valid List Items from ceo"""
    spiels_list = []
    if len(spiels) == 0:
        return [], ''
    for spiel in spiels:
        url = news_link_from_spiel(spiel)
        if url != None:
            spiels_list.append(url)
        else:
            raise Exception('URL SHOULD NOT BE NULL')
    # using list comprehension 
    # to remove None values in list 
    # spiels_list = [i for i in spiels_list if i] 
    return spiels_list, spiels[0].get('timestamp')

def get_new_items(ticker: str, channel='@newswire', max_iterations = 60, until = 0):
    """Gets news items from ceo using ticker

        Parameters:
            ticker - stock ticker, for example APHA
            channel - can be @newswire, @thenewswire 
            max_iterations - max number of requests to ceo.ca
    """
    sp = SearchParams(channel=channel, filter_terms=ticker)
    scroll_height = 0
    data_urls = []
    blank_fetchs = 0
    for i in range(max_iterations):
        if until != 0:
            # update object with new timestamp
            sp = replace(sp, **{
                'until': until, 
                'original_scroll_height': scroll_height
            })
            module_logger.warning(f'Update timestamp: {until}')
        params = params_to_dict(sp)
        data = get_spiels(params)
        # standard delay to not get blocked
        time.sleep(0.5)
        spiels: list = data.get('spiels', [])
        urls, new_timestamp = extract_urls(spiels)
        if len(urls) == 0:
            # push back timestamp by 2 months
            until = earlier_timestamp(until, 60)
            blank_fetchs = blank_fetchs + 1
            # nothing new for about a year
            # stop fetching data
            if blank_fetchs >= 7:
                break
            continue
        else:
            blank_fetchs = 0
            until = new_timestamp
        scroll_height += art_pixel_height * len(urls)
        data_urls = [*data_urls, *urls]
    return data_urls


# Function that selectors any article class and then returns all the text, alternatively can use sumpy for a well
# formed pages like ceo.ca
if __name__ == "__main__":
    data_urls = get_new_items('APHA', until=1609217267394)