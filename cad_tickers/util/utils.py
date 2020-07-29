"""

Contains various utility classes
Converts xlsx to pandas
"""
import pandas as pd
def convert(file_path):
  df = pd.read_excel(file_path)
  return df

def transform_name_to_slug(raw_ticker):
  transformed = raw_ticker.lower().replace(".","").replace(' ', '-')
  return transformed


def make_cse_path(raw_ticker, raw_industry):
  """
    1933 Industries Inc.
  """
  # verify raw_industry is in industry
  cse_industries = ['Industry', 'Mining', 'Diversified Industries',
       'Life Sciences', 'Oil and Gas', 'Technology', 'CleanTech']
  # do later
  base_cse_url = 'https://thecse.com/en/listings'
  industry = raw_industry.lower().replace(' ', '-')
  ticker = transform_name_to_slug(raw_ticker)
  return f'{base_cse_url}/{industry}/{ticker}'