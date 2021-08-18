from cad_tickers.exchanges.cse import get_recent_docs_from_url
ip_url = "https://www.thecse.com/en/listings/diversified-industries/1933-industries-inc"
sample_urls = get_recent_docs_from_url(ip_url)
print(sample_urls)
exit(1)
