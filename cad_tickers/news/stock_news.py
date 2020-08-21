"""
Downloads stock ticker news from yahoo 

https://ca.finance.yahoo.com/quote/IP.CN/
 
Aim to extract date, group title description

get all news from cnw with a function
"""
import requests
from typing import List
def scrap_new_for_ticker(ticker: str)-> List[dict]:
  yahoo_base_qurl = 'https://finance.yahoo.com/quote'
  yahoo_qurl = f'{yahoo_base_qurl}/{ticker}?p={ticker}'
  r = requests.get(yahoo_qurl)
  return []