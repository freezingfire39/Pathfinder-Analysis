## exmample requests



# analysis
curl --location 'http://127.0.0.1:8000/api/v1/py/analysis/' \
--header 'Content-Type: application/json' \
--data '{"symbols" : ["000001"],"method": "max_sharpe_ratio","amount": 1e6}'

# timing
curl --location 'http://127.0.0.1:8000/api/v1/py/timing/' \
--header 'Content-Type: application/json' 

# default portfolio
curl --location 'http://127.0.0.1:8000/api/v1/py/default/portfolio/' \
--header 'Content-Type: application/json' 

# custom portfolio
curl --location 'http://127.0.0.1:8000/api/v1/py/custom/portfolio/' \
--header 'Content-Type: application/json' \
--data '{"weights":[{"symbol":"000001", "weight": 0.1}, {"symbol":"000003", "weight":0.9}],"amount": 1e6}'

# rank ???
curl --location --request GET 'http://127.0.0.1:8000/api/v1/py/rank/?metric=vol' \
--header 'Content-Type: application/json' 