from cad_tickers.news.iiroc_halts import get_halts_resumption
from cad_tickers.news.stock_news import scrap_news_for_ticker, find_news_source, find_news_link_and_text
import os
import bs4

def test_get_halts_resumption():
  halts_df = get_halts_resumption()
  assert(len(halts_df) > 20)

def test_stock_news_works():
  news_data = scrap_news_for_ticker('IP.CN')
  assert(len(news_data) > 0)

def test_stock_news_data_valid():
  news_items = scrap_news_for_ticker('IP.CN')
  for news_item in news_items:
    source = news_item.get('source')
    link_href = news_item.get('link_href')
    link_text = news_item.get('link_text')
    ticker = news_item.get('ticker')
    assert (bool(source))
    assert (bool(link_href))
    assert (bool(link_text))
    assert (bool(ticker))

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
  expected_text = "ImagineAR and The Pittsburgh Gateways Corporation Sign MOU To Integrate Augmented Reality Into the Energy Innovation Center"
  assert (link_href == '/news/r-e-p-e-t-130000181.html')
  assert (link_text == expected_text)