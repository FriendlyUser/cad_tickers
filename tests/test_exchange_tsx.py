from cad_tickers.exchanges.tsx import get_mig_report, \
  dl_tsx_xlsx, grab_symbol_for_ticker, \
  company_description_by_ticker

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


def test_grab_cad_symbol_for_ticker():
  # tests to make sure file can be downloaded
  symbol = grab_cad_symbol_for_ticker('zmd')
  assert(symbol == 'ZMD.H')

def test_description_fetch():
  description = company_description_by_ticker('zmd')
  zoom_description = '''ZoomMed Inc is a Canada-based company that, together with its subsidiaries, is engaged in the development and marketing of computer applications designed for healthcare professionals. It builds and operates the e-Pic Communication Platform, a clinical interoperable information exchange network between physicians and the various other stakeholders of the healthcare sector, such as pharmacists, specialists, pharmaceutical corporations, laboratories, specialized clinics private insurers, employers, and others.'''
# Grab ticker data from strong