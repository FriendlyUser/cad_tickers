import requests
# Not going to download massive amounts of files
# instead get all the stocks tickers throught the tsx api
# 2366 stocks total, sounds about right
# then use graphql to hit each element with yield
# or multiprocessing same as before
# and output a massive csv

payload2 = {
    "operationName": "findCompaniesByKeywords",
    "variables": {"keywords": "a"},
    "query": """query findCompaniesByKeywords($keywords: String) {
	findCompaniesByKeywords(keywords: $keywords) {
		symbol
		name
		exchange
		__typename
	}
}""",
}

# Sample URL
query = """query getStockListSymbolsWithQuote($stockListId: String!, $locale: String) {
	stockList: getStockListSymbolsWithQuote(
		stockListId: $stockListId
		locale: $locale
	) {
		stockListId
		name
		description
		longDescription
		metricTitle
		listItems {
			symbol
			longName
			rank
			metric
			price
			priceChange
			percentChange
			volume
			__typename
		}
		totalPriceChange
		totalPercentChange
		createdAt
		updatedAt
		__typename
	}
}
"""

payload = {
    "operationName": "getStockListSymbolsWithQuote",
    "query": query,
    "variables": {"locale": "en", "stockListId": "ALL"},
}

url = "https://app-money.tmx.com/graphql"
r = requests.post(url, json=payload)
print(r.status_code)
print(r.text)