import requests
import json

url = "https://api.twitch.tv/kraken/games/top"
clientID = {"Client-ID": "XXXXX"}

r = requests.get(url,headers=clientID)
data = r.json()

print(data['top'][0]['game']['name'])
