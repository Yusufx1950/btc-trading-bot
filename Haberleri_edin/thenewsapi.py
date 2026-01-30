# the news api 
# import requests
# query = "https://api.thenewsapi.net/crypto?apikey=9D376B09E52DF7A56ABE055633D20385&q=(btc AND bitcoin)&within=24h&sentiments=positive,neutral,negative&categories=price-analysis,NFT,markets,altcoin,policy,legal,business,DeFi,finance,gaming,technology,blockchain,opinion,metaverse,mining,security,interview,review,AI,investigation,web3,stablecoins,news&page=1&size=10"
# response = requests.get(query)
# data = response.json()
# print(data)

# import requests

# url = "https://trade-bloom-finance.p.rapidapi.com/news/list"

# querystring = {"id":"top-news"}

# headers = {
# 	"x-rapidapi-key": "0c33e7d064mshb060dcc2ec61e5ap1aa7b1jsn021cb226cc88",
# 	"x-rapidapi-host": "trade-bloom-finance.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

# print(response.json())
import requests

# url = "https://cryptocurrency-news2.p.rapidapi.com/v1/bitcoinist"

# headers = {
# 	"x-rapidapi-key": "0c33e7d064mshb060dcc2ec61e5ap1aa7b1jsn021cb226cc88",
# 	"x-rapidapi-host": "cryptocurrency-news2.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers)

# print(response.json())
# response = requests.get("https://coinmarketcap.com/currencies/bitcoin/#News")
# print(response.text)
# print("bitti")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome driver başlat
driver = webdriver.Chrome()

# İstediğin sayfayı aç
driver.get("https://coinmarketcap.com/currencies/bitcoin/")

wait = WebDriverWait(driver, 100)
element = wait.until(EC.presence_of_element_located((By.ID, "searchBox")))

print(driver.title)  # Sayfa başlığını yazdır