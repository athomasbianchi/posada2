import requests
import json

url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/2025/segments/0/leagues/12577?view=mBoxscore&view=mMatchupScore&view=mRoster&scoringPeriodId=10"

response = requests.request("GET", url)

data = response.json()

print(data)

with open('scoretest_2.json', 'w') as file:
    json.dump(data, file, indent=4)