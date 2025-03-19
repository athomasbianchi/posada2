import requests
import json

url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/2025/segments/0/leagues/12577?view=mRoster"

response = requests.request("GET", url)

data = response.json()

gameId = data['gameId']
scoringPeriodId = data['scoringPeriodId']
seasonId = data['seasonId']
segmentId = data['segmentId']
print(response.status_code)
print(data)

teams = data['teams']

with open(f'rosters_{seasonId}_{scoringPeriodId}_{gameId}.json', 'w') as file:
    json.dump(teams, file, indent=4)