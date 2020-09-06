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
