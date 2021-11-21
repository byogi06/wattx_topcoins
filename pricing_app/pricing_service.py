"""
Service Name : CoinPrice service gets data coinmarketcap.com
Description : Returns a list of all active cryptocurrencies with latest market data.
Max limit : 400 (Note that this limit is on CoinPrice service which can be be changed in pricing_config)
"""

from flask import Flask,jsonify
from flask_restful import Api, Resource, abort
import requests
import pricing_config
from requests.exceptions import ConnectionError, Timeout, RequestException

app=Flask(__name__)
api=Api(app)

class CoinPrices(Resource):
    def __init__(self):
        self.service_name='CoinRank'
        self.coin_price_list = []

    def get(self):
        session = requests.Session()
        session.headers.update(pricing_config.PRICE_HEADERS)
        try:
            with session as ses:
                response = ses.get(pricing_config.PRICE_API_URL, params=pricing_config.PRICE_PARAMETERS)
                if response.status_code == requests.codes.ok:
                    coin_price_data = response.json()['data']
                    if not coin_price_data:
                        abort(404, message='Data not found, please check parameters in config file of CoinPrice')
                    self.coin_price_list=[{'Symbol':coin['symbol'],'Price USD': coin['quote']['USD']['price']} for coin in coin_price_data ]
                else:
                    return {
                        "service": self.service_name,
                        "status": response.status_code,
                        "error": "Could not fetch, TopCoins data from coinmarketcap.com,verify the pricing_config for CoinPrices"
                    }
        except ConnectionError as ece:
            return {
                "service": self.service_name,
                "status": 503,
                "error": "A Connection error occurred,please check coinmarketcap.com api service is running correctly or not"
            }
        except Timeout as et:
            return {
                "service": self.service_name,
                "status": 504,
                "error": "The request timed out while trying to connect to the remote server"
            }
        except RequestException as e:
            return {
                "service": self.service_name,
                "status": 500,
                "error": "There was an ambiguous exception that occurred while handling your request"
            }
        return jsonify(self.coin_price_list)

api.add_resource(CoinPrices,'/')
if __name__=='__main__':
    app.run(host="0.0.0.0",port=5002,debug=True)