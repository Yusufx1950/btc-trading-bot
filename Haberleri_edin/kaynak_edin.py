# api adresleri
# https://newsdata.io/search-dashboard
# CG-2xF2KV3kMxYnTtqnTJPTTdbZ https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin&x_cg_demo_api_key=CG-2xF2KV3kMxYnTtqnTJPTTdbZ /search/trending/*
import datetime
import os

import requests


 

url = "http://www.coingecko.com/api"
headers = {
    "Content-Type": "application/json"
}

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print(data)
else :
    print(f" verisi alınamadı. Hata kodu: {response.status_code}")