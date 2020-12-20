from cad_tickers.news.ceo import SearchParams, get_new_items
from cad_tickers.news.ceo.utils import news_link_from_spiel, params_to_dict, earlier_timestamp 
from cad_tickers.news.ceo.scrap import extract_article, save_bs4_tag
from dataclasses import replace
from tests.news.sample_data import ref_text, sample_spiel

def test_create_sp():
    default_sp = SearchParams(until=1608318681)
    y = params_to_dict(default_sp)
    x = {'channel': '@newswire', 'load_more': 'top', 'original_scroll_height': 0, 'until': 1608318681, 'filters[terms]': 'APHA', 'filters[top]': 100}
    assert y == x

def test_create_sp_update():
    default_sp = SearchParams(until=1608318681)
    y = replace(default_sp, **{'channel': '@cad_tickers'})
    y = params_to_dict(y)
    x = {'channel': '@cad_tickers', 'load_more': 'top', 'original_scroll_height': 0, 'until': 1608318681, 'filters[terms]': 'APHA', 'filters[top]': 100}
    assert y == x

def test_get_url():
    
    url = news_link_from_spiel(sample_spiel)
    assert url == 'https://ceo.ca/@newswire/aphria-inc-recognized-for-executive-gender-diversity'


def test_get_new_items():
    assert len(get_new_items('APHA', until=1609217267394)) == 109

def test_earlier_timestamp():
    assert earlier_timestamp(1609414235276, days=90) == 1601638235276
   
def test_article_scrap():
    sample_url = 'https://ceo.ca/@thenewswire/ecolomondo-releases-its-interim-financial-statements-4f559'
    article = extract_article(sample_url)
    save_bs4_tag(article, 'index.html')

    old_text = article.text

    assert ref_text == old_text

def test_article_scrap_old():
    sample_url = 'https://ceo.ca/@newsfile/peak-cloture-un-placement-prive-de-4m-et-confirme-son-partenariat-chinois'
    article = extract_article(sample_url)
    assert True
