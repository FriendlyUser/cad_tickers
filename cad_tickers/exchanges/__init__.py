"""
Exchanges
----------

Downloading and cleaning data from the cse and tsx exchanges
"""

from cad_tickers.exchanges.cse import (
    get_cse_files,
    get_cse_tickers_df,
    get_description_for_url,
)
from cad_tickers.exchanges.tsx import (
    get_all_tickers_data,
    get_all_tsx_tickers,
    get_ticker_data,
    get_tickers,
    get_tsx_tickers,
    gql_data,
)
from cad_tickers.exchanges.classes import CSETicker, CSESedarFilings

# Example graphql endpoint data
# for the tsx output
# Ex: {"operationName":"findCompaniesByKeywords","variables":{"keywords":"zmd"},"query":"query findCompaniesByKeywords($keywords: String) {\n  findCompaniesByKeywords(keywords: $keywords) {\n    symbol\n    name\n    exchange\n    __typename\n  }\n}\n"}`