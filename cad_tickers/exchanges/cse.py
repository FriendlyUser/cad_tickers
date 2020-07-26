"""

Canadian Securities Exchange
----------------------------

Functions to download tickers from the cse

"""

import requests
import re
def get_cse_files(filename='cse.xlsx', filetype="xlsx") -> str:
  """Gets excel spreadsheet from api.tsx using requests

  Parameters:
    filename: Name of the file to be saved
    exchanges: TSX, TSXV
  Returns:
    filePath returns path to file

  See ://stackoverflow.com/questions/13567507/passing-csrftoken-with-python-requests

  """
  # TODO force it to be pdf or xlsx
  # https://www.thecse.com/export-listings/xlsx?f={}
  # https://www.thecse.com/export-listings/pdf?f={}
  URL = f'https://www.thecse.com/export-listings/{filetype}?f=' + r'{}'
  r = requests.get(URL)
  responseHeaders = r.headers
  if "text/html" in responseHeaders["Content-Type"]:
    return None
  elif any(re.findall(r'application/vnd.ms-excel|application/pdf|xlsx',
      responseHeaders["Content-Type"],
      re.IGNORECASE)
    ):
    respData = r.content
    filepath = f'{filename}'
    with open(filepath, 'wb') as s:
      s.write(respData)
    return filepath
  else:
    return None

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", 
                        "--file", 
                        help="file name (default: %(default)s)'", 
                        default="cse.xlsx") 
  parser.add_argument('-t',
                    "--type",
                    default='xlsx',
                    const='xlsx',
                    nargs='?',
                    choices=('xlsx','pdf'),
                    help='xlsx or pdf (default: %(default)s)') 
  args = parser.parse_args()
  get_cse_files(args.file, args.type)
