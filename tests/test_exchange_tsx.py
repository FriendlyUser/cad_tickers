from cad_tickers.exchanges.tsx import get_mig_report, dl_tsx_xlsx
import os
def test_dl_tsx():
  path = get_mig_report("All.xlsx")
  assert(path == "All.xlsx")
  assert (os.path.exists(path))

def test_dl_tsxv():
  path = get_mig_report("TSXV.xlsx", "TSXV")
  assert(path == "TSXV.xlsx")
  assert(os.path.exists(path))

def test_dl_all():
  path = get_mig_report("All.xlsx", None)
  assert(path == "All.xlsx")
  assert(os.path.exists(path))

def test_dl_all_options():
  # tests to make sure file can be downloaded
  path = dl_tsx_xlsx("full_time.xlsx", exchanges='TSX', marketcap='0-50')
  assert(path == "full_time.xlsx")
  assert(os.path.exists(path))