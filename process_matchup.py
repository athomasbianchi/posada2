import json

tj_team_dict = {
  0: 'FA',
  1: 'CHEATING RAIDERS',
  2: 'STRUCTURE FIRE',
  3: 'BAYOU SHOOTERS',
  4: 'RYNO WORLD',
  5: 'DETROIT NITTANY TIDE',
  6: 'ORLANDO RENEGADES',
  7: 'SPRINGFIELD ZEPHYRS',
  8: 'DIP CITY THUNDER',
  9: 'YOUNG BUCKS',
  10: 'COUNTRY STRONG',
  # 11: '???',
  12: 'THE JEFF BROS.',
  # 13: '???',
  14: 'The Driscoll Brothers',
  15: 'Carlos to Carlos',
  16: 'Halladay Holliday',
  17: 'Crimson Water',
  18: '#buckstrong',
  19: 'MIDTOWN JAGUARS',
  20: 'WEST COAST SPARTANS'
}

with open('scoretest_2.json') as file:
  data = json.load(file)

  # print(data['schedule'])

  print(len(data['schedule']))

  for matchup in data['schedule']:
    if matchup['matchupPeriodId'] != 1:
      break
    print(matchup)
    home_team = matchup['home']['teamId']
    away_team = matchup['away']['teamId']
    home_score = matchup['home']['totalPoints']
    away_score = matchup['away']['totalPoints']
    print(tj_team_dict[home_team], home_score)
    print(tj_team_dict[away_team], away_score)
    print('\n')