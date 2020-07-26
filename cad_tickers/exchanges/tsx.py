import requests
import pandas as pd
import multiprocessing as mp
from json import loads
from bs4 import BeautifulSoup
from datetime import datetime

# importing the sys module 
import sys 
  
# the setrecursionlimit function is 
# used to modify the default recursion 
# limit set by python. Using this,  
# we can increase the recursion limit 
# to satisfy our needs 

sys.setrecursionlimit(10**6) 


def get_description_for_ticker(ticker): # change the body of the loop to function
  # grab ticker return desc
  # do on google colab
  # https://stackoverflow.com/questions/56987872/parallelize-pandas-column-update
  symbol = grab_symbol_for_ticker(ticker)
  if symbol is None:
    return ''
  return company_description_by_ticker(symbol)

def get_mig_report(filename='', exchange="TSX", return_df=False) -> str:
  """Gets excel spreadsheet from api.tsx using requests
  Input
    filename: Name of the file to be saved
    exchanges: TSX, TSXV
    return_df: Return a pandas dataframe
  Output:
    filePath returns path to file

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
  # To get all exchanges, leave blank
  # login_data = dict(report_type='excel', csrfmiddlewaretoken=client.cookies['csrftoken'])
  # Options are TSX, TSXV and nothing for all
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

# exchanges: TSXV
# marketcap: 
# hqregions: canada
# hqlocations: 
# sectors:
# //*[@id="root"]/div[4]/div[3]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]
def grab_symbol_for_ticker(ticker) -> str:
  """Grabs the first symbol from ticker data

  all symbols should lead to valid webpages for data scrapping

  TODO: If anyone wants to validate that, be my guest
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

def add_descriptions_to_df_pp(df) -> pd.DataFrame:
  df['description'] = ''
  tickers = df['Ticker'].tolist()
  with mp.Pool() as p:
    descriptions = p.map(get_description_for_ticker, tickers)
  df['description'] = descriptions
  df.to_csv('tsx_descriptions.csv')
  return df

# https://stackoverflow.com/questions/56987872/parallelize-pandas-column-update
def add_descriptions_to_df(df) -> pd.DataFrame:
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
  df.to_csv('tsx_descriptions.csv')
  return df

def company_description_by_ticker(ticker)-> str:
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

def lookup_symbol_by_ticker(ticker)-> list:
  """Returns search dictionary for ticker/
  sometimes the name of the ticker in the xlsx 
  sheet is off slightly and we need to find the "real ticker"

  Uses standard api to grab tickers
  TODO: make another function that uses the new graphql api instead
  in case this one gets depreciated
  Example searchpoint is https://app.quotemedia.com/lookup?callback=html&q=zmd&limit=5&webmasterId=101020

  See https://app-money.tmx.com/graphql and https://money.tmx.com/en/
    Ex: {"operationName":"findCompaniesByKeywords","variables":{"keywords":"zmd"},"query":"query findCompaniesByKeywords($keywords: String) {\n  findCompaniesByKeywords(keywords: $keywords) {\n    symbol\n    name\n    exchange\n    __typename\n  }\n}\n"}

  Input: Ticker as string

  Output: Dictionary
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
    print('Data missing, no response available')
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

def dl_tsx_xlsx(filename = None, **kwargs) -> str:
  """Gets excel spreadsheet from api.tsx using requests
  
  Replicates api calls in TSX discover tool

  Input
    filename: Name of the file to be saved
    options: 
      exchanges: TSX, TSXV
      marketcap: values from 0 to specified value
      sectors: cpc, clean-technology, closed-end-funds, technology
      # Other options depending on what is selected
  Output:
    filePath: returns path to file or pandas dataframe

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

  # To get all exchanges, leave blank
  # login_data = dict(report_type='excel', csrfmiddlewaretoken=client.cookies['csrftoken'])
  # Options are TSX, TSXV and nothing for all
  r = client.post(tsx_url, data=search_data, headers=dict(Referer=tsx_url))
  resp_headers = r.headers
  if "text/html" in resp_headers["Content-Type"]:
    return None
  elif resp_headers["Content-Type"] == "application/ms-excel":
    resp_data = r.content
    if filename is None:
      return pd.read_excel(resp_data)
    else:
      with open(filename, 'wb') as s:
        s.write(resp_data)
      return filename
  else:
    return None

# Add endpoint to query search parameters for tsx spreadsheets
if __name__ == "__main__":
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
  # df = add_descriptions_to_df(df)
  df = add_descriptions_to_df_pp(df)
  # print(df)
  len(df)
  end_time = datetime.now()
  print(end_time - start_time)
  # get_mig_report(args.file, args.exchange)
  # company_description_by_ticker('zmd')
