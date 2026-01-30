#son makaleleri getir
import requests 

response = requests.get('https://data-api.coindesk.com/news/v1/article/list',
    params={"lang":"EN","limit":10,"categories":"BTC","api_key":"93d603c935bca3b99d7f77f1f6549097f6aa8ec8ef6dd2ecb4b6b76695620c01"},
    headers={"Content-type":"application/json; charset=UTF-8"}
)

json_response = response.json()

#makale arama kısmı sanırım


response = requests.get('https://data-api.coindesk.com/news/v1/search',
    params={"search_string":"bitcoin","lang":"EN","source_key":"coindesk","api_key":"93d603c935bca3b99d7f77f1f6549097f6aa8ec8ef6dd2ecb4b6b76695620c01"},
    headers={"Content-type":"application/json; charset=UTF-8"}
)

json_response = response.json()