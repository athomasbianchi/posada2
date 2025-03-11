import json
import pandas as pd

pro_team_dict = {
  19: 'LAD'
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
  16: 'Bench?',
  17: 'Bench?',
  19: 'IF'
}

pos_list = [
  0, 1, 2, 3, 4, 5, 12, 13, 14, 15,
]

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

'''
    {
        "draftAuctionValue": 0,
        "id": 39832,
        "keeperValue": 12,
        "keeperValueFuture": 0,
        "lineupLocked": false,
        "onTeamId": 0,
        "player": {
            "active": true,
            "defaultPositionId": 10,
            "draftRanksByRankType": {
                "STANDARD": {
                    "auctionValue": 79,
                    "published": false,
                    "rank": 1,
                    "rankSourceId": 0,
                    "rankType": "STANDARD",
                    "slotId": 0
                },
                "ROTO": {
                    "auctionValue": 53,
                    "published": false,
                    "rank": 1,
                    "rankSourceId": 0,
                    "rankType": "ROTO",
                    "slotId": 0
                }
            },
            "droppable": false,
            "eligibleSlots": [
                11,
                12,
                16,
                17,
                13,
                14
            ],
            "firstName": "Shohei",
            "fullName": "Shohei Ohtani",
            "id": 39832,
            "injured": false,
            "injuryStatus": "ACTIVE",
            "jersey": "17",
            "lastName": "Ohtani",
            "lastNewsDate": 1740858478000,
            "ownership": {
                "activityLevel": null,
                "auctionValueAverage": 77.62380952380953,
                "auctionValueAverageChange": -1.9360863095238017,
                "averageDraftPosition": 1.4924924924924925,
                "averageDraftPositionPercentChange": -0.06359807693743935,
                "date": 1741259105122,
                "leagueType": 0,
                "percentChange": -0.012432012959010308,
                "percentOwned": 99.81698303573523,
                "percentStarted": 97.4964217837115
            },
            "proTeamId": 19,
            "seasonOutlook": "Ohtani has scripted quite the r\u00e9sum\u00e9 already over his seven MLB seasons: Rookie of the Year (2018), MVP honors (2021), first player in history to hit 30-plus homers while also striking out 200-plus batters (2022), back-to-back MVPs (2023-24) and, most recently, becoming the charter member of baseball's 50/50 club (2024). While further history book rewrites might seem logically unattainable for the now-30-year-old, it's still within the realm of possibility that he'll score a career-high total fantasy points in 2025 and/or set a personal best in Wins Above Replacement. As both a hitter and pitcher from 2021-23 -- his expected role once again in 2025 -- Ohtani <i>averaged</i> 214 fantasy points more than the league's next-best player annually, an advantage that can be readily exploited in ESPN's standard game with its daily transaction format. Ohtani's fantasy utility hinges heavily upon how your league handles him, but a universal, No. 1 overall case is a relatively easy one.",
            "stats": [
                {
                    "appliedAverage": 5.534591194968553,
                    "appliedTotal": 880.0,
                    "externalId": "2024",
                    "id": "002024",
                    "proTeamId": 0,
                    "scoringPeriodId": 0,
                    "seasonId": 2024,
                    "statSourceId": 0,
                    "statSplitTypeId": 0,
                    "stats": {
                        "0": 636.0,
                        "1": 197.0,
                        "2": 0.30974843,
                        "3": 38.0,
                        "4": 7.0,
                        "5": 54.0,
                        "6": 99.0,
                        "7": 98.0,
                        "8": 411.0,
                        "9": 0.64622642,
                        "10": 81.0,
                        "11": 10.0,
                        "12": 6.0,
                        "13": 5.0,
                        "14": 0.0,
                        "15": 5.0,
                        "16": 731.0,
                        "17": 0.39010989,
                        "18": 1.03633631,
                        "19": 162.86075,
                        "20": 134.0,
                        "21": 130.0,
                        "22": 15.0,
                        "23": 59.0,
                        "24": 4.0,
                        "25": 55.0,
                        "26": 7.0,
                        "27": 162.0,
                        "28": 2838.0,
                        "29": 3.89835165,
                        "31": 1.0,
                        "67": 0.0,
                        "68": 0.0,
                        "69": 0.0,
                        "70": 0.0,
                        "71": 0.0,
                        "72": 0.0,
                        "73": 0.0,
                        "74": 96.0,
                        "75": 63.0,
                        "76": 0.0,
                        "77": 0.0,
                        "81": 159.0
                    }
                },
                {
                    "appliedAverage": 0.0,
                    "appliedTotal": 0.0,
                    "externalId": "2025",
                    "id": "002025",
                    "proTeamId": 0,
                    "scoringPeriodId": 0,
                    "seasonId": 2025,
                    "statSourceId": 0,
                    "statSplitTypeId": 0,
                    "stats": {}
                },
                {
                    "appliedAverage": 0.0,
                    "appliedTotal": 0.0,
                    "externalId": "2025",
                    "id": "012025",
                    "proTeamId": 0,
                    "scoringPeriodId": 0,
                    "seasonId": 2025,
                    "statSourceId": 0,
                    "statSplitTypeId": 1,
                    "stats": {}
                },
                {
                    "appliedAverage": 0.0,
                    "appliedTotal": 0.0,
                    "externalId": "2025",
                    "id": "032025",
                    "proTeamId": 0,
                    "scoringPeriodId": 0,
                    "seasonId": 2025,
                    "statSourceId": 0,
                    "statSplitTypeId": 3,
                    "stats": {}
                },
                {
                    "appliedAverage": 0.0,
                    "appliedTotal": 0.0,
                    "externalId": "2025",
                    "id": "022025",
                    "proTeamId": 0,
                    "scoringPeriodId": 0,
                    "seasonId": 2025,
                    "statSourceId": 0,
                    "statSplitTypeId": 2,
                    "stats": {}
                },
                {
                    "appliedAverage": 7.319727971428572,
                    "appliedTotal": 1076.0000118,
                    "externalId": "2025",
                    "id": "102025",
                    "proTeamId": 0,
                    "scoringPeriodId": 0,
                    "seasonId": 2025,
                    "statSourceId": 1,
                    "statSplitTypeId": 0,
                    "stats": {
                        "0": 588.0,
                        "1": 174.0,
                        "2": 0.296,
                        "3": 32.0,
                        "4": 6.0,
                        "5": 44.0,
                        "6": 82.0,
                        "7": 92.0,
                        "8": 350.0,
                        "9": 0.595,
                        "10": 79.0,
                        "11": 11.0,
                        "12": 5.0,
                        "13": 4.0,
                        "15": 4.0,
                        "16": 682.0,
                        "17": 0.382,
                        "18": 0.977,
                        "20": 112.0,
                        "21": 112.0,
                        "23": 32.0,
                        "24": 6.0,
                        "25": 26.0,
                        "26": 7.0,
                        "27": 161.0,
                        "32": 20.0,
                        "33": 20.0,
                        "34": 354.0,
                        "35": 479.0,
                        "37": 93.0,
                        "38": 0.219858156,
                        "39": 39.0,
                        "41": 1.12,
                        "42": 6.0,
                        "43": 0.288100209,
                        "44": 51.0,
                        "45": 47.0,
                        "46": 16.0,
                        "47": 3.58,
                        "48": 144.0,
                        "50": 10.0,
                        "53": 9.0,
                        "54": 4.0,
                        "55": 0.692307692,
                        "63": 12.0,
                        "81": 147.0,
                        "82": 3.69
                    }
                },
                {
                    "appliedAverage": 5.095238095238095,
                    "appliedTotal": 107.0,
                    "externalId": "2024",
                    "id": "102024",
                    "proTeamId": 0,
                    "scoringPeriodId": 0,
                    "seasonId": 2024,
                    "statSourceId": 1,
                    "statSplitTypeId": 0,
                    "stats": {
                        "0": 84.0,
                        "1": 24.0,
                        "2": 0.286,
                        "3": 5.0,
                        "4": 1.0,
                        "5": 7.0,
                        "6": 13.0,
                        "7": 11.0,
                        "8": 52.0,
                        "9": 0.619,
                        "10": 11.0,
                        "11": 2.0,
                        "12": 1.0,
                        "16": 96.0,
                        "17": 0.375,
                        "18": 0.994,
                        "20": 17.0,
                        "21": 14.0,
                        "23": 6.0,
                        "24": 1.0,
                        "25": 5.0,
                        "26": 1.0,
                        "27": 22.0,
                        "81": 21.0
                    }
                }
            ]
        },
        "rosterLocked": false,
        "status": "FREEAGENT",
        "tradeLocked": false
    },
'''


with open('espn.json', 'r') as file:
    data = json.load(file)
    export_data = []
    for d in data:
      player_data = {}
      espn_id = d['id']
      player_data['EspnId'] = espn_id
      player = d['player']
      player_data['Name'] = player['fullName']
      for pos in player['eligibleSlots']:
        if not pos in pos_list:
          continue
        if pos in pos_dict:
          player_data[pos_dict[pos]] = True
        else:
          print(pos)
      # print(player['stats'])
      for year in player['stats']:
        if year['id'] == '102025':
          player_data['Espn_proj'] = round(year['appliedTotal'],0)
      export_data.append(player_data)
    df = pd.DataFrame(export_data)
    df.fillna(False, inplace=True)
    df.to_csv("positions.csv")

