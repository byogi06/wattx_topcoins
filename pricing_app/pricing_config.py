#Pricing service config parameters
PRICE_API_KEY='d89b4907-42c9-49f6-8794-99f246b04f24'
PRICE_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
PRICE_TOPCOIN_URL = 'http://127.0.0.1:5002/coinprices'
PRICE_PARAMETERS = {
    'start': '1',
    'convert': 'USD',
    'limit': '400'
}
PRICE_HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': PRICE_API_KEY,
}