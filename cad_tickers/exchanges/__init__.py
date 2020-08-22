"""
Exchanges
----------

Downloading and cleaning data from the cse and tsx exchanges
"""

from cad_tickers.exchanges.cse import *
from cad_tickers.exchanges.tsx import *

# Example graphql endpoint data
# for the tsx output
# Ex: {"operationName":"findCompaniesByKeywords","variables":{"keywords":"zmd"},"query":"query findCompaniesByKeywords($keywords: String) {\n  findCompaniesByKeywords(keywords: $keywords) {\n    symbol\n    name\n    exchange\n    __typename\n  }\n}\n"}`