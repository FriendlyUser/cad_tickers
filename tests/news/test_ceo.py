from cad_tickers.news.ceo import SearchParams, ceo_url, params_to_dict

def test_create_sp():
    default_sp = SearchParams()
    y = params_to_dict(default_sp)
    x = {'channel': '@newswire', 'load_more': 'top', 'original_scroll_height': 0, 'until': 1608318681, 'filter[terms]': 'APHA', 'filter[top]': 100}
    shared_items = {k: x[k] for k in x if k in y and x[k] == [k]}
    assert len(shared_items) == 6
