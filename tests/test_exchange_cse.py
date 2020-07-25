from cad_tickers.exchanges.cse import get_cse_files
import os
def test_dl_cse():
  path = get_cse_files("cse.xlsx")
  assert(path == "cse.xlsx")
  assert (os.path.exists(path))

def test_dl_all():
  path = get_cse_files("cse.pdf", "pdf")
  assert(path == "cse.pdf")
  assert(os.path.exists(path))

