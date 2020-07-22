from cad_tickers.exchanges.tsx import get_mig_report
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

def pytest_sessionfinish(session, exitstatus):
  """ whole test run finishes. """
  os.remove('All.xlsx')
  os.remove('TSXV.xlsx')
  os.remove('All.xlsx')