from cad_tickers.news.iiroc_halts import get_halts_resumption

import os
def test_get_halts_resumption():
  halts_df = get_halts_resumption()
  assert(len(halts_df) > 20)