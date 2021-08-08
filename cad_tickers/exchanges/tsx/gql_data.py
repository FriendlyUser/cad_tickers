class GQL:
    """
    quote_by_symbol_query:

    .. _quote_by_symbol_query:

    graphql properties for `getQuoteBySymbol` are
      * symbol
      *  name
      *  price
      *  priceChange
      *  percentChange
      *  exchangeName
      *  exShortName
      *  exchangeCode
      *  marketPlace
      *  sector
      *  industry
      *  volume
      *  openPrice
      *  dayHigh
      *  dayLow
      *  MarketCap
      *  MarketCapAllClasses
      *  peRatio
      *  prevClose
      *  dividendFrequency
      *  dividendYield
      *  dividendAmount
      *  dividendCurrency
      *  beta
      *  eps
      *  exDividendDate
      *  shortDescription
      *  longDescription
      *  website
      *  email
      *  phoneNumber
      *  fullAddress
      *  employees
      *  shareOutStanding
      *  totalDebtToEquity
      *  totalSharesOutStanding
      *  sharesESCROW
      *  vwap
      *  dividendPayDate
      *  weeks52high
      *  weeks52low
      *  alpha
      *  averageVolume10D
      *  averageVolume30D
      *  averageVolume50D
      *  priceToBook
      *  priceToCashFlow
      *  returnOnEquity
      *  returnOnAssets
      *  day21MovingAvg
      *  day50MovingAvg
      *  day200MovingAvg
      *  dividend3Years
      *  dividend5Years
      *  datatype
      *  __typename
    """

    quote_by_symbol_query = """query getQuoteBySymbol($symbol: String, $locale: String) {
      getQuoteBySymbol(symbol: $symbol, locale: $locale) {
        symbol
        name
        price
        priceChange
        percentChange
        exchangeName
        exShortName
        exchangeCode
        marketPlace
        sector
        industry
        volume
        openPrice
        dayHigh
        dayLow
        MarketCap
        MarketCapAllClasses
        peRatio
        prevClose
        dividendFrequency
        dividendYield
        dividendAmount
        dividendCurrency
        beta
        eps
        exDividendDate
        shortDescription
        longDescription
        website
        email
        phoneNumber
        fullAddress
        employees
        shareOutStanding
        totalDebtToEquity
        totalSharesOutStanding
        sharesESCROW
        vwap
        dividendPayDate
        weeks52high
        weeks52low
        alpha
        averageVolume10D
        averageVolume30D
        averageVolume50D
        priceToBook
        priceToCashFlow
        returnOnEquity
        returnOnAssets
        day21MovingAvg
        day50MovingAvg
        day200MovingAvg
        dividend3Years
        dividend5Years
        datatype
        __typename
      }
    }
  """

    quote_by_symbol_payload = {
        "operationName": "getQuoteBySymbol",
        "variables": {"locale": "en"},
        "query": quote_by_symbol_query,
    }

    get_company_news_events_query = """query getNewsAndEvents(
      $symbol: String!,
      $page: Int!,
      $limit: Int!,
      $locale: String!
    ) { 
      news: getNewsForSymbol(
        symbol: $symbol,
        page: $page,
        limit: $limit,
        locale: $locale
      ) {
        headline
        datetime
        source
        newsid
        summary
        __typename
      }
      events: getUpComingEventsForSymbol(symbol: $symbol, locale: $locale) {
        title
        date
        status
        type
        __typename
        }
      }
    """

    get_company_news_events_payload = {
        "operationName": "getNewsAndEvents",
        "variables": {
            "symbol": "ART",
            "page": 1,
            "limit": 100,
            "locale": "en"
        },
        "query": get_company_news_events_query,
    }

    get_company_filings_query = """query getCompanyFilings(
      $symbol: String!
      $fromDate: String
      $toDate: String
      $limit: Int
    ) {
      filings: getCompanyFilings(
        symbol: $symbol
        fromDate: $fromDate
        toDate: $toDate
        limit: $limit
      ) {
        size
        filingDate
        description
        name
        urlToPdf
        __typename
      }
    }"""

    # Replace the fromDate and toDate variables, or default them to
    # the current month
    get_company_filings_payload = {
        "operationName": "getCompanyFilings",
        "variables": {
            "symbol": "ART",
            "fromDate": "2020-09-01",
            "toDate": "2020-09-30",
            "limit": 100,
        },
        "query": get_company_filings_query,
    }
