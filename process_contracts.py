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

  # batter & pitcher zips projections (deepest ids)
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
  # print(contracts)
  return contracts

# TODO later, not important now
def format_contracts(contracts):
  contracts = contracts.reset_index()
  print(contracts)

  # check for dups
  # ids = contracts['FangraphsId']
  # dups = contracts[ids.isin(ids[ids.duplicated()])].sort_values("FangraphsId")
  # print(dups)


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

def add_projections(contracts):
  h = pd.read_csv('hitters_simp.csv')
  sp = pd.read_csv('sp_simp.csv')
  rp = pd.read_csv('rp_simp.csv')

  proj = pd.concat([h, sp, rp], ignore_index=True)
  proj.sort_values(by="VORP", ascending=False, inplace=True, ignore_index=True)

  proj_merge = proj[['Name', 'NameASCII', 'Team', 'FangraphsId', 'PTS', 'PTS/G', 'VORP']]
  contracts_merge = contracts[['FangraphsId', 'EspnId', 'Team']]

  merged = pd.merge(proj_merge, contracts_merge, how='left', on='FangraphsId')
  merged.rename(columns={'Team_x': 'Pro', 'Team_y': 'TJ'}, inplace=True)
  merged.loc[merged['TJ'].isna(), 'TJ'] = 'FA'

  return merged

def add_positions(merged):
  pos = pd.read_csv('positions.csv')
  # merged_wo_eid = merged[merged['EspnId'].isna()]
  eid_merge = pos[['Name', 'EspnId']]
  eid_merge.rename(columns={'Name': 'NameASCII'}, inplace=True)
  eid_merge['EspnId'].astype('int64')
  eid_merge['NameASCII'] = eid_merge['NameASCII'].replace('Luis Ortiz', 'Luis L. Ortiz')
  eid_merge['NameASCII'] = eid_merge['NameASCII'].replace('Jose Ferrer',  'Jose A. Ferrer')
  eid_merge = pd.concat([eid_merge, pd.DataFrame({
    "NameASCII": ['Kyle Hart'],
    "EspnId": ["39936"]
  }, index=None)], ignore_index=True)

  merged = pd.merge(merged, eid_merge, on='NameASCII', how='left')
  merged['EspnId_x'].fillna(merged['EspnId_y'], inplace=True)
  # merged_wo_eid = merged[merged['EspnId_x'].isna()]
  # print(merged_wo_eid)
  merged.rename(columns={'EspnId_x': 'EspnId'}, inplace=True)
  print(merged.head(25))
  pos_to_merge = pos[['EspnId', 'Espn_proj', 'C', '1B', '2B', '3B', 'SS', 'OF', 'Util', 'SP', 'RP', 'P']]
  print(pos_to_merge.head(25))

  # print(merged)
  # print(merged['EspnId_x'].dtype)
  # print(merged['EspnId_y'].dtype)
  # print(eid_merge)



contracts = add_ids(contracts)
contracts = format_contracts(contracts)
merged = add_projections(contracts)
ranks = add_positions(merged)


# yb = (contracts[contracts['Team'] == 'Young Bucks'])
# print(yb.shape)
# print(yb.head(50))
