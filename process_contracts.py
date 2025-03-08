import pandas as pd

contracts = pd.read_csv('contracts.csv')
contracts.sort_values(by="Yrs", inplace=True, ascending=False)
contracts.rename(columns={'Player': 'Name'}, inplace=True)

# add ids
def add_ids(contracts):

  # https://www.smartfantasybaseball.com/2020/12/everything-you-need-to-know-about-the-player-id-map/#WhatIs
  id_map = pd.read_csv("id_map.csv", dtype=str)
  id_map = id_map[['ESPNNAME', 'IDFANGRAPHS', 'ESPNID']]
  id_map.columns = ['Name', 'FangraphsId', 'EspnId']

  contracts = pd.merge(contracts, id_map, how="left", on='Name')
  contracts['Name'] = contracts['Name'].str.strip('@©2 ')
  contracts.drop_duplicates(subset=['Name'], keep='first', inplace=True, ignore_index=True)
  contracts = contracts.set_index('Name')

  # batter & pitcher zips projectsions (deepest ids)
  batters = pd.read_csv("zipsb.csv", dtype=str)
  batters = batters[['Name', 'PlayerId']]
  batters.rename(columns={'PlayerId': 'FangraphsId'}, inplace=True)
  batters.drop_duplicates(subset="Name", inplace=True)
  batters = batters.set_index('Name')
  contracts.loc[contracts['FangraphsId'].isna(), 'FangraphsId'] = batters['FangraphsId']

  pitchers = pd.read_csv("zipsp.csv", dtype=str)
  pitchers = pitchers[['Name', 'PlayerId']]
  pitchers.rename(columns={'PlayerId': 'FangraphsId'}, inplace=True)
  pitchers.drop_duplicates(subset="Name", inplace=True)
  pitchers = pitchers.set_index('Name')
  contracts.loc[contracts['FangraphsId'].isna(), 'FangraphsId'] = pitchers['FangraphsId']

  # prospect board
  board = pd.read_csv('the_board.csv')
  board = board[['Name', 'PlayerId']]
  board.rename(columns={'PlayerId': 'FangraphsId'}, inplace=True)
  board = board.set_index('Name')
  contracts.loc[contracts['FangraphsId'].isna(), 'FangraphsId'] = board['FangraphsId']

  # previous year prospect board
  board_24 = pd.read_csv('the_board_24.csv')
  board_24 = board_24[['Name', 'PlayerId']]
  board_24.rename(columns={'PlayerId': 'FangraphsId'}, inplace=True)
  board_24.drop_duplicates(subset="Name", inplace=True)
  board_24 = board_24.set_index('Name')
  contracts.loc[contracts['FangraphsId'].isna(), 'FangraphsId'] = board_24['FangraphsId']

  # college draft board
  draft = pd.read_csv("draft.csv", dtype=str)
  draft = draft[['Name', 'PlayerId']]
  draft.rename(columns={'PlayerId': 'FangraphsId'}, inplace=True)
  draft.drop_duplicates(subset="Name", inplace=True)
  draft = draft.set_index('Name')
  contracts.loc[contracts['FangraphsId'].isna(), 'FangraphsId'] = draft['FangraphsId']

  # fallbacks for retirees
  fallback = pd.read_csv("fallback_ids.csv", dtype=str)
  fallback = fallback.set_index('Name')
  contracts.loc[contracts['FangraphsId'].isna(), 'FangraphsId'] = fallback['FangraphsId']

  # unnamed = contracts[contracts['FangraphsId'].isna()]
  # print(unnamed)

  return contracts

def format_contracts(contracts):
  contracts = contracts.reset_index()
  print(contracts)
  contracts = contracts.set_index('FangraphsId')
  print(contracts)
  print(contracts.index.is_unique)
  duplicates = contracts.index.duplicated(keep=False)
  print(duplicates)

  contracts = contracts.groupby(level=0).first()  # remove duplicates
  print(contracts)
  print(contracts.index.is_unique)

  # adael = contracts[contracts['Name'] == 'Adael Amador']
  # print(adael)
  # print(contracts[contracts['Yrs'].isna()])
  # print(contracts.iloc['Adael Amador'])

  # print(contracts.columns)
  # print(contracts.head(10))
  # contracts['Type'] = pd.Series()
  # contracts.loc[contracts['Yrs'] == 'U', 'Type'] = 'AA'
  # contracts.loc[contracts['Yrs'] == 'U', 'Cost'] = 0
  # contracts.loc[contracts['Type'] == 'AA', 'Yrs'] = ""
  # minors = contracts[contracts['Type'] == 'AA']
  # minors.sort_values(by="Team", inplace=True)
  # print(minors.shape)
  # print(minors.head(20))

  # print(contracts[contracts['Yrs'].isna()])

  # series = contracts['Yrs']
  # series.drop_duplicates(inplace=True)
  # print(series)

  # longs = contracts[contracts['Yrs'] > 3]
  # print(longs.head(20))
  return contracts

contracts = add_ids(contracts)
contracts = format_contracts(contracts)

# yb = (contracts[contracts['Team'] == 'Young Bucks'])
# print(yb.shape)
# print(yb.head(50))
