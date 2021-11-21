"""
Service Name : CoinRank service gets data from cryptocompare.com
Description : Get a number of top coins by their market cap.
Max limit : 100 (this limit is on source service - cryptocompare.com
               hence CoinRank service cannot return Top coins more than 100)
"""

from flask import Flask,jsonify
from flask_restful import Api, Resource, abort
import requests
import ranking_config
from requests.exceptions import ConnectionError, Timeout, RequestException

app=Flask(__name__)
api=Api(app)

class CoinRank(Resource):

    def __init__(self):
        self.service_name='CoinRank'
        self.coin_list = []

    def get(self):
        session = requests.Session()
        session.headers.update(ranking_config.RANK_HEADERS)
        try:
            with session as ses:
                response = ses.get(ranking_config.RANK_API_URL, params=ranking_config.RANK_PARAMETERS)
                if response.status_code== requests.codes.ok:
                    coin_ranks_data = response.json()['Data']
                    if not coin_ranks_data:
                        abort(404, error='Data not found, please check parameters in config file of CoinRank')
                    rank = 1
                    for coin in coin_ranks_data:
                        self.coin_list.append({'Rank': rank, 'Symbol': coin['CoinInfo']['Name']})
                        rank += 1
                else:
                    return {
                    "service":self.service_name,
                    "status":response.status_code,
                    "error":"Could not fetch, TopCoins data from cryptocompare.com"
                            }
        except ConnectionError as ece:
            return {
                "service":self.service_name,
                "status": 503,
                "error":"A Connection error occurred, please check cryptocompare.com api service is running correctly or not"
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
        return jsonify(self.coin_list)

api.add_resource(CoinRank,'/')
if __name__=='__main__':
    app.run(host="0.0.0.0",port=5001,debug=True)