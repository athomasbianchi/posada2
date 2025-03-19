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

pos_dict = {
  0: 'C',
  1: '1B',
  2: '2B',
  3: '3B',
  4: 'SS',
  5: 'OF',
  6: 'MI',
  7: 'CI',
  8: 'LF',
  9: 'CF',
  10: 'RF',
  11: 'DH',
  12: "Util",
  13: 'P',
  14: 'SP',
  15: 'RP',
  16: 'Bench',
  17: 'IL',
  19: 'IF'
}

with open('rosters_2025_2_2.json') as file:
    data = json.load(file)
    exp = {}
    # print(data[8])
    yb = data[8]
    # for entry in yb['roster']['entries']:
    #     slot = entry['lineupSlotId']
    #     id = entry['playerId']
    #     player = entry['playerPoolEntry']['player']
    #     fullName = player['fullName']
    #     injruyStatus = player['injuryStatus']
    #     print(fullName, slot, injruyStatus)
    #     exp[slot] = fullName
    # print(exp)

    for team in data:
        team_name = tj_team_dict[team['id']]
        exp[team_name] = {
           'active_count': 0,
            'il_count': 0
        }
        for entry in team['roster']['entries']:
            slot = entry['lineupSlotId']
            id = entry['playerId']
            player = entry['playerPoolEntry']['player']
            fullName = player['fullName']
            injruyStatus = player['injuryStatus']
            # injured IL eligible
            injured = player['injured']
            
            if slot == 17:
              exp[team_name]['il_count'] = exp[team_name].get('il_count', 0) + 1
              print(team_name)
              print(fullName, slot, injruyStatus, injured)
            else:
               exp[team_name]['active_count'] = exp[team_name].get('active_count', 0) + 1
            if exp[team_name].get(slot):
                exp[team_name][slot].append({'name': fullName, 'il_eligible': injured})
            else:
              exp[team_name][slot] = [{'name': fullName, 'il_eligible': injured}]
    print(exp['YOUNG BUCKS'])

    for team in exp:
        # print(exp[team])
        print(team)
        active_count = exp[team]['active_count']
        il_count = exp[team]['il_count']
        print(active_count, il_count)
        if 17 in exp[team]:
          # print(exp[team][17])
          for player in exp[team][17]:
            if player['il_eligible'] == False:
               print('IL ALERT!')
               print(player['name'] + ' is not IL eligible')
              
        if active_count != 28:
          print('ACTIVE ALERT!:', active_count)
        else:
          print('active players', active_count)
        print('\n')
        # print(team)
        # print(exp[team]['active_count'])
        # print(exp[team]['il_count'])
        # print(player['fullName'])
        # print(player['defaultPositionId'])
        # print(player['injuryStatus'])
        # print(player['proTeamId'])
        # print(player['stats'])
        # print(player['playerId'])
        # print(player['ownership
    #     print(team)