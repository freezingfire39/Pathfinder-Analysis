
# timing
curl --location 'http://127.0.0.1:8000/api/v1/py/timing/' 

# default portfolio
curl --location 'http://127.0.0.1:8000/api/v1/py/default/portfolio/' 

# custom portfolio
curl --location 'http://127.0.0.1:8000/api/v1/py/custom/portfolio/' \
--header 'Content-Type: application/json' \
--data '{"weights":[{"symbol":"000001", "weight": 0.1}, {"symbol":"000003", "weight":0.9}],"amount": 1e6}'
