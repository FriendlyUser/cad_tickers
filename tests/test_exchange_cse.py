from cad_tickers.exchanges.cse import get_cse_files
from cad_tickers.util import make_cse_path
import os
def test_dl_cse():
  path = get_cse_files("cse.xlsx")
  assert(path == "cse.xlsx")
  assert (os.path.exists(path))

def test_dl_all():
  path = get_cse_files("cse.pdf", "pdf")
  assert(path == "cse.pdf")
  assert(os.path.exists(path))

def test_cse_listing_url():
  cse_path = make_cse_path('1933 Industries Inc.', 'Diversified Industries')
  assert(cse_path == 'https://thecse.com/en/listings/diversified-industries/1933-industries-inc')
