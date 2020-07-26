import requests
from json import loads
from bs4 import BeautifulSoup

def get_mig_report(filename, exchange="TSX") -> str:
  """Gets excel spreadsheet from api.tsx using requests
  Input
    filename: Name of the file to be saved
    exchanges: TSX, TSXV
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
  resp_headers = r.headers
  if "text/html" in resp_headers["Content-Type"]:
    return None
  elif resp_headers["Content-Type"] == "application/ms-excel":
    print(f"Downloaded data from {tsx_url} for {exchange} to {filename}")
    resp_data = r.content
    with open(filename, 'wb') as s:
      s.write(resp_data)
    return filename
  else:
    return None

def get_company_description(ticker) -> str:
  """ Gets company description for ticker

  TMX is not very reliable at loading quotes 
  sometimes pages do not exist
  """
  url = f'https://web.tmxmoney.com/company.php?qm_symbol={ticker}'
# exchanges: TSXV
# marketcap: 
# hqregions: canada
# hqlocations: 
# sectors:
# //*[@id="root"]/div[4]/div[3]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]
def grab_symbol_for_ticker(ticker):
  """Grabs the first symbol from ticker data

  all symbols should lead to valid webpages for data scrapping

  TODO: If anyone wants to validate that, be my guest
  """
  ticker_data = lookup_symbol_by_ticker(ticker)
  return ticker_data[0].get('symbol')


def company_description_by_ticker(ticker):
  # get lookup symbol
  search_symbol = grab_symbol_for_ticker(ticker)
  params = {'qm_symbol': search_symbol}
  # // //*[@id="pane-news"]/div/div/div[1]/div/div[1]/div[2]/section[1]/p

  search_url = f'https://web.tmxmoney.com/company.php'
  r = requests.get(search_url, params=params)
  html_content = r.text
  # Parse the html content
  soup = BeautifulSoup(html_content, "lxml")
  # selector copied from chrome https://money.tmx.com/en/quote/ZMD.H
  description_selector = '#pane-news > div > div > div.col-md-9 > div > div:nth-child(1) > div.tmx-panel-body.pt-0 > section:nth-child(1) > p'
  description = soup.select(description_selector)[0]
  contents = description.contents[0]
  return contents

def lookup_symbol_by_ticker(ticker)-> dict:
  """Returns search dictionary for ticker/
  sometimes the name of the ticker in the xlsx 
  sheet is off slightly and we need to find the "real ticker"

  Uses standard api to grab tickers
  TODO: make another function that uses the new graphql api instead
  in case this one gets depreciated

  See https://app-money.tmx.com/graphql and https://money.tmx.com/en/
    Ex: {"operationName":"findCompaniesByKeywords","variables":{"keywords":"zmd"},"query":"query findCompaniesByKeywords($keywords: String) {\n  findCompaniesByKeywords(keywords: $keywords) {\n    symbol\n    name\n    exchange\n    __typename\n  }\n}\n"}

  Input: Ticker as string

  Output: Dictionary
  """
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
  e_idx = quote_data.find(')')
  # https://app.quotemedia.com/lookup?callback=html&q=zmd&limit=5&webmasterId=101020

  # All symbols returned all valid
  return loads(quote_data[s_idx + 1:e_idx])

def dl_tsx_xlsx(filename, **kwargs) -> str:
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
    filePath: returns path to file or None

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
    with open(filename, 'wb') as s:
      s.write(resp_data)
    return filename
  else:
    return None

# Add endpoint to query search parameters for tsx spreadsheets
if __name__ == "__main__":
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
  # get_mig_report(args.file, args.exchange)
  company_description_by_ticker('zmd')
