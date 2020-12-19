from cad_tickers.news.ceo import SearchParams
from cad_tickers.news.ceo.utils import news_link_from_spiel, params_to_dict
from dataclasses import replace
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
    
    url = news_link_from_spiel(sample_spiel())
    assert url == 'https://ceo.ca/@newswire/aphria-inc-recognized-for-executive-gender-diversity'

# move to test when done
def sample_spiel():
    return {
        'channel': 'newsroom',
        'spiel': "Aphria Inc. Recognized for Executive Gender Diversity by Globe and Mail's Women Lead Here Benchmark and Provides an Update on COVID-19 @newswire/aphria-inc-recognized-for-executive-gender-diversity $APHA-US $APHA #news/pharma #news/healthcare",
        'name': '@newswire',
        'timestamp': 1585310926647,
        'spiel_id': '0a6d390dc0ef',
        'color': '#666   ',
        'public_id': None, 
        'parent_id': '0a6d390dc0ef',
        'parent_channel': 'newsroom',
        'parent_timestamp': 1585310926647,
        'votes': None,
        'editable': False,
        'featured': None,
        'verified': False,
        'fake': False,
        'bot': None,
        'voted': False,
        'flagged': False,
        'own_spiel': False,
        'score': None, 
        'saved_id': None,
        'saved_timestamp': None
    }       
