"""

Canadian Securities Exchange
----------------------------

Functions to download tickers from the cse

"""

import requests
import re
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from cad_tickers.util import parse_description_tags, make_cse_path

def get_cse_files(filename: str ='cse.xlsx', filetype: str ="xlsx") -> str:
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

def clean_cse_data(raw_df: pd.DataFrame)-> pd.DataFrame:
  """Removes bad data from cse dataframe.

  Parameters:
    raw_df: data from cse, read in from xlsx sheet so it is messy.
  Returns:
    df: clean df with no empty rows, proper column titles and removed needed rows.
  """
  # drop all nans
  df = raw_df
  df = df.dropna(axis=0, how='all')
  # drop empty column
  df = df.drop(df.columns[6], axis=1)
  # grab logically column names from first row
  column_labels = df.iloc[1, :].values.tolist()
  df.columns = column_labels
  # dropping title row and column titles row 
  df = df.drop([df.index[0], df.index[1]])
  df = df.reset_index(drop=True)
  return df

def get_cse_tickers_df()-> pd.DataFrame:
  """Grab cse dataframe from exported xlsx sheet

    Returns:
      clean_df: cleaned dataframe with urls to download more data on ticker.
  """
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
    # add urls
    clean_df['urls'] = clean_df.apply(lambda x: make_cse_path(x['Company'], x['Industry']), axis=1)
    return clean_df
  else:
    return None

def get_description_for_url(url: str)-> str:
  """
    Parameters:
      url - link to ticker can be empty string
    Returns:
      description - details of what the ticker does, can be empty string
  """
  if url is '':
    return ''
  r = requests.get(url)
  html_content = r.text
  soup = BeautifulSoup(html_content, "lxml")
  description_selector = '#block-system-main div.company-description > p'
  description_tags = soup.select(description_selector)
  return parse_description_tags(description_tags)

def add_descriptions_to_df(df: pd.DataFrame, max_workers: int =16) -> pd.DataFrame:
  """
    Parameters:
      df - dataframe with urls to stock listings
      max_workers - maximum number of thread workers to have
    Returns:
      df: updated dataframe with descriptions in a column

  """
  urls = df['urls'].tolist()
  with ThreadPoolExecutor(max_workers=max_workers) as tpe:
    iterables = tpe.map(get_description_for_url, urls)
    descriptions = list(iterables)
  df['description'] = descriptions
  return df

if __name__ == "__main__":
  from datetime import datetime
  import argparse
  start_time = datetime.now()
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
  cse_df = get_cse_tickers_df()
  df = add_descriptions_to_df(cse_df)
  end_time = datetime.now()
  # get_cse_files(args.file, args.type)
  # print(df)
