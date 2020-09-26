import pandas as pd
import os
import sys
from datetime import datetime

start_time = datetime.now()
sys.path.insert(0, "../cad_tickers")
from cad_tickers.exchanges import (
    get_all_cse_tickers,
    get_all_tsx_tickers,
    get_all_tickers_data,
)

if os.path.exists("cse.csv") == False:
    print("MISSING CSE.csv - call cad_tickers/exchanges/cse.py")
    exit(1)


# read tickers from cse.csv
cse_df = pd.read_csv("cse.csv")
cse_tickers = get_all_cse_tickers(cse_df)
# tsx and tsxv tickeres
tsx_tickers = get_all_tsx_tickers()

full_tickers = [
    *tsx_tickers,
    *cse_tickers,
]

full_df = get_all_tickers_data(tickers=full_tickers)
# remove duplicate tickers
# before duplicate removal around 2969
full_df.drop_duplicates(subset="symbol", keep="first", inplace=True)
full_df.to_csv("full_csv.csv", index=False)

end_time = datetime.now()
print(end_time - start_time)
