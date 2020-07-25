import requests
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

# exchanges: TSXV
# marketcap: 
# hqregions: canada
# hqlocations: 
# sectors:
def dl_tsx_xlsx(filename, **kwargs) -> str:
  """Gets excel spreadsheet from api.tsx using requests
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
  get_mig_report(args.file, args.exchange)
