import requests
import json

#simple script to explore Twitch's response data structures

games_url = "https://api.twitch.tv/kraken/games/top?limit=100"
clientID = {"Client-ID": "hw4byyky0odf9lb3ew7jfcgjcnf1jv"}

data = requests.get(games_url,headers=clientID)
data = data.json()

print(data['top'][0]['game']['logo'])
