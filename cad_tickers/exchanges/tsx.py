"""
TSX Functions
---------------

Set of functions to scrap ticker data from the toronto stock exchange.

Will definitely split into smaller files once the graphql api becomes the main api.
"""


import requests
import pandas as pd
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
from json import loads
from bs4 import BeautifulSoup

# importing the sys module 
import sys 
  
# the setrecursionlimit function is 
# used to modify the default recursion 
# limit set by python. Using this,  
# we can increase the recursion limit 
# to satisfy our needs 

sys.setrecursionlimit(10**6) 


def get_description_for_ticker(ticker: str)-> str: # change the body of the loop to function
  """
    set of functionality
  """
  # grab ticker return desc
  # do on google colab
  # https://stackoverflow.com/questions/56987872/parallelize-pandas-column-update
  symbol = grab_symbol_for_ticker(ticker)
  if symbol is None:
    return ''
  return company_description_by_ticker(symbol)

def get_mig_report(filename: str='', exchange: str="TSX", return_df: bool =False) -> str:
  """
  Description:
    Gets excel spreadsheet from tsx api programatically.
    See for more flexibility :func:`dl_tsx_xlsx <cad_tickers.exchanges.tsx.dl_tsx_xlsx>`

  Parameters:
    filename: Name of the file to be saved
    exchanges: TSX, TSXV
    return_df: Return a pandas dataframe

  Returns:
    filePath: returns path to file or dataframe

  See ://stackoverflow.com/questions/13567507/passing-csrftoken-with-python-requests

  """
  tsx_url = 'https://api.tmxmoney.com/en/migreport/search'
  client = requests.session()
  # Retrieve the CSRF token first
  client.get(tsx_url)  # sets cookie
  if 'csrftoken' in client.cookies:
      # Django 1.6 and up
      csrftoken = client.cookies['csrftoken']
  else:
      # older versions
      csrftoken = client.cookies['csrf']
  login_data = dict(report_type='excel', csrfmiddlewaretoken=csrftoken)
  if exchange in ["TSX", "TSXV"]:
    login_data["exchanges"] = exchange

  r = client.post("https://api.tmxmoney.com/en/migreport/search", data=login_data, headers=dict(Referer=tsx_url))
  resp_data = r.content
  if return_df is True:
    return pd.read_excel(resp_data)
  else:
    resp_headers = r.headers
    if "text/html" in resp_headers["Content-Type"]:
      return None
    elif resp_headers["Content-Type"] == "application/ms-excel":
      print(f"Downloaded data from {tsx_url} for {exchange} to {filename}")
      with open(filename, 'wb') as s:
        s.write(resp_data)
      return filename
    else:
      return None

def grab_symbol_for_ticker(ticker: str) -> str:
  """
  Description:
    Grabs the first symbol from ticker data
    all symbols should lead to valid webpages for data scrapping.

  Parameters: 
    ticker: string representing the stock ticker

  Returns: 
    symbol: string - searchable string in the quotemedia api or empty string
  """

  if ticker is None or ticker is '':
    return ''

  ticker_data = lookup_symbol_by_ticker(ticker)
  if len(ticker_data) == 0:
    # splice name and try again
    # remove everything past dot
    clean_ticker = ticker.split(".", 1)[0]
    ticker_data = lookup_symbol_by_ticker(clean_ticker)
    
    # Ticker likely has no data
    # see NTY
    if len(ticker_data) == 0:
      return ''
  return ticker_data[0].get('symbol')


def add_descriptions_to_df_pp(df: pd.DataFrame, max_workers: int = 16) -> pd.DataFrame:
  """
  Description: fetch descriptions for tickers in parallel
  noticable speedup uses thread pool which should be faster

  Input:
    df: dataframe containing tickers
  Returns:
    df: updated dataframe with a descriptions if available
  """
  df['description'] = ''
  tickers = df['Ticker'].tolist()
  with ThreadPoolExecutor(max_workers=max_workers) as tpe:
    iterables = tpe.map(get_description_for_ticker, tickers)
    descriptions = list(iterables)
  df['description'] = descriptions
  return df

def add_descriptions_to_df_pp_legacy(df: pd.DataFrame) -> pd.DataFrame:
  """
  Description: fetch descriptions for tickers in parallel
  noticable speedup, keeping this to verify speed increase

  Input:
    df: dataframe containing tickers
  Returns:
    df: updated dataframe with a descriptions if available
  """
  df['description'] = ''
  tickers = df['Ticker'].tolist()
  with mp.Pool() as p:
    descriptions = p.map(get_description_for_ticker, tickers)
  df['description'] = descriptions
  return df

# https://stackoverflow.com/questions/56987872/parallelize-pandas-column-update
def add_descriptions_to_df(df) -> pd.DataFrame:
  """
  Description: single process solution to fetching descriptions

  Input:
    df: dataframe containing tickers
  Returns:
    df: updated dataframe with a descriptions if available
  """
  df['description'] = ''
  for index, row in df.iterrows():
    ticker = df.at[index, 'Ticker']
    # grab ticker return desc
    # do on google colab
    # https://stackoverflow.com/questions/56987872/parallelize-pandas-column-update
    symbol = grab_symbol_for_ticker(ticker)
    if symbol is None:
      pass
    description = company_description_by_ticker(symbol)
    df.at[index,'description'] = description
  return df

def company_description_by_ticker(ticker)-> str:
  """
  
  Description: Grabs searchable ticker from quotemedia using tmx ticker

  Input:
    ticker: string 
  Returns:
    df:  updated dataframe with a descriptions if available
  """
  # get lookup symbol
  search_symbol = grab_symbol_for_ticker(ticker)
  if search_symbol is '':
    return ''
  params = {'qm_symbol': search_symbol}
  # // //*[@id="pane-news"]/div/div/div[1]/div/div[1]/div[2]/section[1]/p

  search_url = f'https://web.tmxmoney.com/company.php'
  r = requests.get(search_url, params=params)
  html_content = r.text
  # Parse the html content
  soup = BeautifulSoup(html_content, "lxml")
  # selector copied from chrome https://money.tmx.com/en/quote/ZMD.H
  description_selector = '#pane-news > div > div > div.col-md-9 > div > div:nth-child(1) > div.tmx-panel-body.pt-0 > section:nth-child(1) > p'
  description_tags = soup.select(description_selector)
  if len(description_tags) > 0:
    description_tag = description_tags[0]
    # grab contents from desscription tag
    if len(description_tag.contents) == 0:
      return ''
    else:
      return description_tag.contents[0]
  # company does not have profile
  else: 
    return ''

def lookup_symbol_by_ticker(ticker: str)-> list:
  """
  
  Description: Returns search array dictionary for tickers
  
  .. note::

    sometimes the name of the ticker in the xlsx 
    sheet is off slightly and we need to find the "real ticker".
    Uses standard api (not graphql) to grab tickers

    Example searchpoint is https://app.quotemedia.com/lookup?callback=tmxtickers&q=zmd&limit=5&webmasterId=101020

  See `Tmx Graphql <https://app-money.tmx.com/graphql>`_  and the new `tmx site <https://money.tmx.com/en/>`_

  Input:
    ticker: tmx ticker

  Output:
    quote_data: list of ticker metadata
  """
  if ticker is None:
    return []
  callback = 'tmxtickers'
  # Theses values can be hardcoded
  params = {
    'callback': callback,
    'limit': 5,
    'webmasterId': 101020,
    'q': ticker
  }
  quote_lookup_url = 'https://app.quotemedia.com/lookup'
  r = requests.get(quote_lookup_url, params=params)
  quote_data = r.text

  if quote_data is None:
     raise Exception('No data returned, check if api is depreciated or contact author for help.')
  s_idx = quote_data.find('(')
  e_idx = quote_data.rfind(')')

  if quote_data == f"{callback}();":
    return []
  # All symbols returned all valid
  try:
    data = loads(quote_data[s_idx + 1:e_idx])
    return data
  except Exception as e:
    print(ticker)
    print('fail to run')
    print(e)
    exit(1)

def dl_tsx_xlsx(filename: str = '', **kwargs) -> str:
  """
  Description: Gets excel spreadsheet from the tsx api using programatically

  .. note::

    Replicates api calls in TSX discover tool with all parameters.
    See `migreport search <https://api.tmxmoney.com/en/migreport/search>`_
    Note that not all parameters are documented and/or limited validation

  Parameters:
    filename: Name of the file to be saved

  Kwargs:
    * exchanges (string): TSX, TSXV
    * marketcap (string): values from 0 to specified value
    * sectors (string): cpc, clean-technology, closed-end-funds, technology

  Returns:
    data - returns path to file or pandas dataframe

    pd.DataFrame 
    
    ===========   =====================================================================
    Ex.           Exchange ticker in TSXV, TSX 
    Name          Full name of ticker 
    Ticker        Symbol usually 4 characters or less
    QMV($)        Quoted Market Value, I assume this is based on the "currency".
    HQ Region     Headquarters region usually a country (need to double check)
    HQ Location   Usually a province or state
    Sector        Main sector, technology
    Sub Sector    Sub Sector
    ===========   =====================================================================
    Ex.,Name,Ticker,QMV($),HQ Region,HQ Location,Sector,Sub Sector

  .. note
     if this package gets popular enough, I will add more documentation

  See `passing csrftoken <https://stackoverflow.com/questions/13567507/passing-csrftoken-with-python-requests>`_
  """

  tsx_url = 'https://api.tmxmoney.com/en/migreport/search'
  client = requests.session()
  # Retrieve the CSRF token first
  client.get(tsx_url)  # sets cookie
  if 'csrftoken' in client.cookies:
      # Django 1.6 and up
      csrftoken = client.cookies['csrftoken']
  else:
      # older versions
      csrftoken = client.cookies['csrf']
  search_data = dict(report_type='excel', csrfmiddlewaretoken=csrftoken)

  for k, v in kwargs.items():
    if k == 'exchanges':
      if k in ["TSX", "TSXV"]:
        search_data["exchanges"] = k
    elif k == 'marketcap':
      if k in ["0-50", "50-250", "250-500", "500-1000", '1000-9999999999999999999999']:
        search_data["marketcap"] = k
    else:
      search_data[k] = v

  r = client.post(tsx_url, data=search_data, headers=dict(Referer=tsx_url))
  resp_headers = r.headers
  if "text/html" in resp_headers["Content-Type"]:
    return None
  elif resp_headers["Content-Type"] == "application/ms-excel":
    resp_data = r.content
    if filename is '':
      return pd.read_excel(resp_data)
    else:
      with open(filename, 'wb') as f_:
        f_.write(resp_data)
      return filename
  else:
    return None

# Add endpoint to query search parameters for tsx spreadsheets
if __name__ == "__main__":
  from datetime import datetime
  start_time = datetime.now()
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", 
                        "--file", 
                        help="file name (default: %(default)s)'", 
                        default="tsx.xlsx") 
  parser.add_argument('-e',
                    "--exchange",
                    default='TSX',
                    const='TSX',
                    nargs='?',
                    choices=('TSX', 'TSXV', 'None', 'All'),
                    help='TSX, TSXV, All (default: %(default)s)') 
  args = parser.parse_args()
  df = dl_tsx_xlsx(sectors='technology')
  df = add_descriptions_to_df_pp(df)
  print(df)
  end_time = datetime.now()
  print(end_time - start_time)
