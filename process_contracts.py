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
  merged.rename(columns={'EspnId_x': 'EspnId'}, inplace=True)

  pos_to_merge = pos[['Name', 'EspnId', 'Espn_proj', 'C', '1B', '2B', '3B', 'SS', 'OF', 'Util', 'SP', 'RP', 'P']]

  merged = merged.astype({'EspnId': 'str'})
  pos_to_merge = pos_to_merge.astype({'EspnId': 'str'})

  with_pos = pd.merge(merged, pos_to_merge, how="left", on="EspnId")
  with_pos.sort_values(by='VORP', ascending=False, inplace=True)
  return(with_pos)

def find_hitter_vorp(ranks):
  hitters = ranks[(ranks['Util'] == True) & (ranks['VORP'] >= -10)]
  catcher = hitters[hitters['C'] == True]
  first = hitters[hitters['1B'] == True]
  second = hitters[hitters['2B'] == True]
  third = hitters[hitters['3B'] == True]
  short = hitters[hitters['SS'] == True]
  of = hitters[hitters['OF'] == True]
  dh_only = hitters[(hitters["C"] == False) & (hitters['1B'] == False) & (hitters['2B'] == False) & (hitters['3B'] == False) & (hitters['SS'] == False) & (hitters['OF'] == False)]

  v_c = len(catcher)
  v_1 = len(first)
  v_2 = len(second)
  v_3 = len(third)
  v_ss = len(short)
  v_of = len(of)
  v_dh = len(dh_only)

  print(v_c)
  print(v_1)
  print(v_2)
  print(v_3)
  print(v_ss)
  print(v_of / 3)
  print(v_dh)

  default_order = ['C', '2B', 'OF', '3B', '1B', 'SS']
  # hitters['default'] = 'C' if hitters['C'] else '2B' if hitters['2B'] else 'OF' if hitters['OF'] else '3B' if hitters['3B'] else '1B' if hitters['1B'] else 'SS' if hitters['SS'] else 'UT'
  # hitters['default'] = hitters.where

  # df.loc[df['c1'] == 'Value', 'c2'] = 10

  ranks.loc[ranks['SS'] == True, 'DefaultPos'] = 'SS'
  ranks.loc[ranks['1B'] == True, 'DefaultPos'] = '1B'
  ranks.loc[ranks['3B'] == True, 'DefaultPos'] = '3B'
  ranks.loc[ranks['OF'] == True, 'DefaultPos'] = 'OF'
  ranks.loc[ranks['2B'] == True, 'DefaultPos'] = '2B'
  ranks.loc[ranks['C'] == True, 'DefaultPos'] = 'C'
  ranks.loc[ranks['RP'] == True, 'DefaultPos'] = 'RP'
  ranks.loc[ranks['SP'] == True, 'DefaultPos'] = 'SP'
  ranks.loc[ranks['DefaultPos'].isna(), 'DefaultPos'] = 'Util'

  hitters = ranks[(ranks['Util'] == True) & (ranks['VORP'] >= -10)]
  default_counts = hitters['DefaultPos'].value_counts()
  print(default_counts)

  HITTER_VP = .12
  SP_VP = .08
  RP_VP = .02

  print(ranks.head(50))
  return

contracts = add_ids(contracts)
contracts = format_contracts(contracts)
merged = add_projections(contracts)
ranks = add_positions(merged)
w_vorp = find_hitter_vorp(ranks)


# yb = (contracts[contracts['Team'] == 'Young Bucks'])
# print(yb.shape)
# print(yb.head(50))
