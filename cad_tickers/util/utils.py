"""

Contains various utility classes
Converts xlsx to pandas
"""
import pandas as pd
import bs4
from typing import List
def convert(file_path: str) -> pd.DataFrame:
  df = pd.read_excel(file_path)
  return df

def transform_name_to_slug(raw_ticker: str):
  transformed = raw_ticker.lower().replace(".","").replace(' ', '-')
  return transformed

def parse_description_tags(description_tags: List[bs4.element.Tag])-> str:
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

def make_cse_path(raw_ticker: str, raw_industry: str)-> str:
  """
    1933 Industries Inc.
  """
  if pd.isna(raw_industry):
    return ''
  # verify raw_industry is in industry
  cse_industries = ['Industry', 'Mining', 'Diversified Industries',
      'Life Sciences', 'Oil and Gas', 'Technology', 'CleanTech']
  # do later
  base_cse_url = 'https://thecse.com/en/listings'
  industry = raw_industry.lower().replace(' ', '-')
  ticker = transform_name_to_slug(raw_ticker)
  url = f'{base_cse_url}/{industry}/{ticker}'
  return url