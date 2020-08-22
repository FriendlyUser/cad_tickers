from cad_tickers.news.iiroc_halts import get_halts_resumption
from cad_tickers.news.stock_news import scrap_news_for_ticker, find_news_source, find_news_link_and_text
import os
import bs4
# TODO determine if I want to test the inner logic, have raw html
def test_get_halts_resumption():
  halts_df = get_halts_resumption()
  assert(len(halts_df) > 20)


def test_stock_news():
  news_data = scrap_news_for_ticker('IP.CN')
  assert(len(news_data) > 0)


sample_ip_news_item = """
<div class="Ov(h) Pend(44px) Pstart(25px)" data-reactid="10"><div class="C(#959595) Fz(11px) D(ib) Mb(6px)" data-reactid="11">CNW Group</div><h3 class="Mb(5px)" data-reactid="12"><a class="Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled" data-reactid="13" href="/news/r-e-p-e-t-130000181.html"><u class="StretchedBox" 
data-reactid="14"></u>ImagineAR and The Pittsburgh Gateways Corporation Sign MOU To Integrate Augmented Reality Into the Energy Innovation Center</a></h3><p class="Fz(14px) Lh(19px) Fz(13px)--sm1024 Lh(17px)--sm1024 LineClamp(2,38px) LineClamp(2,34px)--sm1024 M(0)" data-reactid="16">VANCOUVER, BC and ERIE Pa., Aug.</p></div>
"""
def test_source():
  news_content = bs4.BeautifulSoup(sample_ip_news_item, "lxml")
  source = find_news_source(news_content)
  assert (source == 'CNW Group')

def test_link_text():
  news_content = bs4.BeautifulSoup(sample_ip_news_item, "lxml")
  link_href, link_text = find_news_link_and_text(news_content)
  expected_text = """VANCOUVER, BC, July 30, 2020 /CNW/ - ImagineAR (CSE: IP) (OTCQB: IPNFF) an Augmented Reality Company that enables sports
teams, brands and businesses to instantly create their own mobile phone AR campaigns, is pleased to announce that Mike Anderson has joined the Company as an Advisor to the CEO for the purposes of launching ImagineAR platform sales in the UK and Europe.  Mr. Anderson is the former managing director of the The Sun and News of the World publications, and founder of the 
mobile app UK development company -The Chelsea Apps factory.  ImagineAR believes Mr. Anderson will significantly accelerate the Company's presence and sales throughout the UK and Europe.""".strip()
  assert (link_href == '/news/r-e-p-e-t-130000181.html')
  assert (link_text == expected_text)