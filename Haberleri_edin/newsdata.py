# Haberleri_edin/newsdata api kullanımı
import requests

url = "https://newsdata.io/api/1/crypto?apikey=pub_3fd2cd41f3d24a289d2230761e65156c&q=btc,bitcoin&image=1&coin=btc&sort=relevancy&excludefield=ai_tag&size=10"
response = requests.get(url)
data = response.json()
print(data)