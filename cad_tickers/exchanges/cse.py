"""

Canadian Securities Exchange
----------------------------

Functions to download tickers from the cse

"""

import requests
import re
import pandas as pd
def get_cse_files(filename='cse.xlsx': str, filetype="xlsx": str) -> str:
  """Gets excel spreadsheet from api.tsx using requests

  Parameters:
    filename: Name of the file to be saved
    filetype: Save as pdf or xlsx
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

def clean_cse_data(raw_df: pd.DataFrame)->pd.DataFrame:
  # drop all nans
  df = raw_df
  df = df.dropna(axis=0, how='all')
  # drop empty column
  df = df.drop(df.columns[6], axis=1)
  # grab logically column names from first row
  column_labels = df.iloc[1, :].values.tolist()
  df.columns = column_labels
  # dropping title row and titles row
  df = df.drop([df.index[0], df.index[1]])
  df = df.reset_index(drop=True)
  return df

def get_cse_tickers_df()-> pd.DataFrame:
  URL = f'https://www.thecse.com/export-listings/xlsx?f=' + r'{}'
  r = requests.get(URL)
  responseHeaders = r.headers
  if "text/html" in responseHeaders["Content-Type"]:
    return None
  elif any(re.findall(r'application/vnd.ms-excel|application/pdf|xlsx',
      responseHeaders["Content-Type"],
      re.IGNORECASE)
    ):
    respData = r.content
    df = pd.read_excel(respData)
    clean_df = clean_cse_data(df)
    return clean_df
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
  # get_cse_files(args.file, args.type)
  df = get_cse_tickers_df()
  print(df)
