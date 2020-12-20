"""

Although some articles are returned from the url https://ceo.ca/@newswire?filters[terms]=APHA&filters[top]=100,

it is adequate to scrap with the api with terms https://ceo.ca/api/get_spiels?channel=%40newswire&until=1593091936374&load_more=top&filters%5Bterms%5D=APHA&filters%5Btop%5D=100&original_scroll_height=1045

best to estimate height difference via scroll height somewhat randomly based on number of entries

469

To scrap.

Call api with terms of interest usually a all caps ticker with name

Then extract the spiels for each and output raw data with cleaned data.

The spiel contain the @newswire just find anything with a @ symbol, should be basic regex.

1. request to ceo.ca with query params including search term, randomized approach
2. use pagination to chain requests - stop after 10 calls and/or timestamp does not change
3. Modify data and return the urls back in an easy to use format, like an list and/or raw data
4. Use external package to analyze articles.
""" 

# 

from cad_tickers.news.ceo.spiel_class import SearchParams
from cad_tickers.news.ceo.utils import params_to_dict, ceo_url, \
 news_link_from_spiel, art_pixel_height

from cad_tickers.news.ceo.main import extract_urls, get_new_items
from cad_tickers.news.ceo.scrap import extract_article, save_bs4_tag
