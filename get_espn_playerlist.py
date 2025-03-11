import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('URL')

COUNT = 2000

payload = {}
headersDict = {
  "players": {
    "limit": COUNT,
    "sortDraftRanks": {
      "sortPriority": 100,
      "sortAsc": True, 
      "value": "STANDARD"
    }
  }
}

headersDump = json.dumps(headersDict)
headers = {'x-fantasy-filter': json.dumps(headersDict)}

response = requests.request("GET", url, headers=headers, data=payload)
print(response.status_code)

data = response.json()
playersList = data['players']

filename = "espn.json"

with open(filename, 'w') as file:
    json.dump(playersList, file, indent=4)

# for player in playersList[0:10]:
#     print(player['onTeamId'])
#     print(player['id'])
#     print(player['player']['fullName'])

