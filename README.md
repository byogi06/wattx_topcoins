# wattx_topcoins
### Description of the problem and solution ###

Problem :  Access the crypto top coins (top coins based on market cap) with the help of available api from 2 different vendors( coinmarketcap.com and cryptocompare.com)

solution : 
As mentioned in challange the service should expose a HTTP endpoint, which when fetched, displays an up-to-date list of top assets and their current prices in USD.
Hence I created 3 services 
 1. Ranking service
 2. Pricing service 
 3. Top coins service
 
 Ranking service and Pricing service are independent services as they internally fetching data/making api calls to two different vendors cryptocompare.com and coinmarketcap.com respectively.
 Ranking service fetches data fields - Symbol of coin and its price
 Pricing service fetches data fields - Symbol of coin and its rank
 
 Top coins service making calls to Ranking service and Pricing service fetching data and combining them using pandas dataframe. 
 Hnece Top coins will have data fields - Rank, symbol and price (in USD)
 
 **Special Note : As Top coins service will only fetch top 100 coins because cryptocompare.com vendor api itself has limit of top 100 coins hence even if you pass limit more than 100 it will only top 100 coins.**

### Technical Details ###
Reasoning behind your technical choices. Trade-offs you might have made, anything you left out, or what you might do differently if you were to spend additional time on the project :

As its python challange , I have used flask framework to implement these api's. There are other frameworks too like FastAPI However I was more comfortable using flask hence I chose the same.

Few things left out or or what you might do differently if you were to spend additional time on the project : 
  1. I could have implemented the logging for each services which is very much necessary for debuging and understanding. 
  2. Login and authentication 
  3. SQLAlchemy ORM implementatation.
                    
 SQLAlchemy ORM implementatation is somewhat depends on requirement. If our api call rates are high then We could pre-fetch and cache the api data in our application's local database every certain period of times.

## How run the top coin service ###
1. Use the docker-compose.yml to create docker images and containers for all the 3 services.
  >docker-compose up
2. Create the network for communication between these services
  >docker network create coins-network
3. Add all the three containers names to the network.
  >docker network connect coins-network rank_app_con
  
  >docker network connect coins-network price_app_con
  
  >docker network connect coins-network top_coins_app_con
  
4. Run the top coin service using curl or browser
   Browser : http://localhost:5000/
            if you want to add the limit http://localhost:5000/?limit=20
   You can use curl command as well. 
   **Special Note **: As Top coins service will only fetch top 100 coins because cryptocompare.com vendor api itself has limit of top 100 coins hence even if you pass limit more than 100 it will only top 100 coins.
   
 
            
   
