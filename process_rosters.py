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

with open('rosters_2025_1_2.json') as file:
    data = json.load(file)
    exp = {}
    # print(data[8])
    yb = data[8]
    for entry in yb['roster']['entries']:
        slot = entry['lineupSlotId']
        id = entry['playerId']
        player = entry['playerPoolEntry']['player']
        fullName = player['fullName']
        injruyStatus = player['injuryStatus']
        print(fullName, slot, injruyStatus)
        exp[slot] = fullName
    print(exp)
    
        # print(player['fullName'])
        # print(player['defaultPositionId'])
        # print(player['injuryStatus'])
        # print(player['proTeamId'])
        # print(player['stats'])
        # print(player['playerId'])
        # print(player['ownership
    #     print(team)