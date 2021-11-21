
#Ranking service config parameters
RANK_API_URL = 'https://min-api.cryptocompare.com/data/top/mktcapfull'
RANK_API_KEY='953fc0382ad107304c06ab910f99a5c615a808ce192f212de169877c251a094e'
RANK_TOPCOIN_URL = 'http://127.0.0.1:5001/coinranks'
RANK_PARAMETERS = {
    'tsym': 'USD',
    'limit':'100'
}
RANK_HEADERS = {
    'Accepts': 'application/json',
    'authorization':RANK_API_KEY
          }

