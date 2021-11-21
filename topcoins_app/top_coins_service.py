"""
Service Name : TopCoins service gets data from CoinRank and CoinPrice
Description : Get a number of top coins by their market cap.
Service Output format : Json -
                 [{"Rank":<Rank of of crypto coin by its market cap> ,
                   "Symbol":<symbol or short notation of coin> ,
                   "Price USD": <Price in USD>
                   }]
Max limit : 100 (this limit is on source service - cryptocompare.com
               hence TopCoin service cannot return Top coins more than 100)

"""


from flask import Flask,request
from flask_restful import Api, Resource, abort
from requests.exceptions import ConnectionError, Timeout, RequestException
import requests
from topcoins_config import RANK_TOPCOIN_URL,PRICE_TOPCOIN_URL
import json
import pandas as pd

app=Flask(__name__)
api=Api(app)


class TopCoins(Resource):
    def __init__(self):
        self.service_name='TopCoins'

    def get(self):
        try:
            limit = request.args.get('limit')
            session = requests.Session()
            with session as ses:
                ranks_obj  = ses.get(RANK_TOPCOIN_URL).json()
                price_obj = ses.get(PRICE_TOPCOIN_URL).json()
        except ConnectionError:
            return {
                "service": self.service_name,
                "error"  : "A Connection error occurred, please check CoinRank or CoinPrice services are running"
                    },503
        except Timeout:
            return {
                "service": self.service_name,
                "error": "The request timed out while trying to connect to the remote server"
            },504
        except RequestException:
            return {
                "service": self.service_name,
                "error": "There was an ambiguous exception that occurred while handling your request"
            },500

        if isinstance(ranks_obj,dict) and ranks_obj.get('error'):
            abort(ranks_obj.get('status') if ranks_obj.get('status') else 404, service=ranks_obj.get('service'),error=ranks_obj.get('error'))
        elif isinstance(ranks_obj,dict) and price_obj.get('message'):
            abort(price_obj.get('status') if price_obj.get('status') else 404,service=ranks_obj.get('service'), error=price_obj.get('error'))
        top_coins_json=self.get_top_coins(ranks_obj,price_obj,limit)

        top_coins =app.response_class(
            response=json.dumps(json.loads(top_coins_json)),
            mimetype='application/json'
        )
        return top_coins

    def get_top_coins(self,ranks_obj,price_obj,limit):
        """
        :param ranks_obj: Json object returned by CoinRanks service
        :param price_obj: Json object returned CoinPrice service
        :param limit: Number of top coins to be returned by TopCoin service
        :return: Json obect of Top <limit> coins
        """
        rank_df=pd.json_normalize(ranks_obj)
        price_df =pd.json_normalize(price_obj)
        top_coins_merge_df = pd.merge(rank_df, price_df, on="Symbol", how="left")
        if limit:
            top_coins_merge_df = top_coins_merge_df[top_coins_merge_df.Rank <= int(limit)]
        top_coins_json=top_coins_merge_df.to_json(orient="records", indent=3)
        return top_coins_json

api.add_resource(TopCoins,'/')
if __name__=='__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)