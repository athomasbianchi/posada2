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

  # add age
  age = pd.read_csv("24_age.csv", dtype=str)
  age['Age'] = age['Age'].astype(int)
  age['Age'] = age['Age'] + 1
  age.rename(columns={'PlayerId': 'FangraphsId'}, inplace=True)
  age_merge = age[['FangraphsId', 'Age']]
  contracts = contracts.reset_index()
  contracts = pd.merge(contracts, age_merge, how='left', on='FangraphsId')
  return contracts

# TODO handle contract price formatting
def format_contracts(contracts):
  contracts.sort_values(by='Team', ascending=False, inplace=True)
  
  contracts.loc[contracts['Yrs'] == "U", 'contractType'] = 'AA'
  contracts.loc[contracts['Note'] == '@', 'contractType'] = 'pre-arb'
  contracts.loc[contracts['Note'] == '¹', 'contractType'] = 'arb1'
  contracts.loc[contracts['Note'] == '²', 'contractType'] = 'arb2'
  contracts.loc[contracts['Note'] == '³', 'contractType'] = 'arb3'
  contracts.loc[contracts['Cost'] == 'AAA opt', 'contractType'] = 'AAA opt'
  contracts.loc[contracts['Level'] == 'Cut', 'contractType'] = 'cut'
  contracts.loc[contracts['contractType'].isna(), 'contractType'] = 'contract'

  return contracts

def add_projections(contracts):
  h = pd.read_csv('hitters_simp.csv')
  sp = pd.read_csv('sp_simp.csv')
  rp = pd.read_csv('rp_simp.csv')

  proj = pd.concat([h, sp, rp], ignore_index=True)
  proj.sort_values(by="VORP", ascending=False, inplace=True, ignore_index=True)

  proj_merge = proj[['Name', 'NameASCII', 'Team', 'FangraphsId', 'PTS', 'PTS/G', 'VORP', 'isRP']]
  contracts_merge = contracts[['FangraphsId', 'EspnId', 'Team', 'Level', 'Yrs', 'Cost', 'Note', 'contractType', 'Age']]

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

def add_vorp(ranks):
  hitters = ranks[(ranks['Util'] == True) & (ranks['VORP'] >= -10)]
  catcher = hitters[hitters['C'] == True]
  first = hitters[hitters['1B'] == True]
  second = hitters[hitters['2B'] == True]
  third = hitters[hitters['3B'] == True]
  short = hitters[hitters['SS'] == True]
  of = hitters[hitters['OF'] == True]
  dh_only = hitters[(hitters["C"] == False) & (hitters['1B'] == False) & (hitters['2B'] == False) & (hitters['3B'] == False) & (hitters['SS'] == False) & (hitters['OF'] == False)]


  ranks.loc[ranks['SS'] == True, 'DefaultPos'] = 'SS'
  ranks.loc[ranks['1B'] == True, 'DefaultPos'] = '1B'
  ranks.loc[ranks['3B'] == True, 'DefaultPos'] = '3B'
  ranks.loc[ranks['OF'] == True, 'DefaultPos'] = 'OF'
  ranks.loc[ranks['2B'] == True, 'DefaultPos'] = '2B'
  ranks.loc[ranks['C'] == True, 'DefaultPos'] = 'C'
  ranks.loc[ranks['RP'] == True, 'DefaultPos'] = 'RP'
  ranks.loc[ranks['SP'] == True, 'DefaultPos'] = 'SP'
  ranks.loc[ranks['DefaultPos'].isna(), 'DefaultPos'] = 'Util'
  
  ranks['PosStr'] = ""
  ranks.loc[ranks['C'] == True, 'PosStr'] = ranks["PosStr"] + 'C'
  ranks.loc[(ranks['2B'] == True) & (ranks['PosStr'] != ""), 'PosStr'] = ranks["PosStr"] + '/2B'
  ranks.loc[(ranks['2B'] == True) & (ranks['PosStr'] == ""), 'PosStr'] = ranks["PosStr"] + '2B'

  ranks.loc[(ranks['OF'] == True) & (ranks['PosStr'] != ""), 'PosStr'] = ranks["PosStr"] + '/OF'
  ranks.loc[(ranks['OF'] == True) & (ranks['PosStr'] == ""), 'PosStr'] = ranks["PosStr"] + 'OF'

  ranks.loc[(ranks['3B'] == True) & (ranks['PosStr'] != ""), 'PosStr'] = ranks["PosStr"] + '/3B'
  ranks.loc[(ranks['3B'] == True) & (ranks['PosStr'] == ""), 'PosStr'] = ranks["PosStr"] + '3B'

  ranks.loc[(ranks['1B'] == True) & (ranks['PosStr'] != ""), 'PosStr'] = ranks["PosStr"] + '/1B'
  ranks.loc[(ranks['1B'] == True) & (ranks['PosStr'] == ""), 'PosStr'] = ranks["PosStr"] + '1B'

  ranks.loc[(ranks['SS'] == True) & (ranks['PosStr'] != ""), 'PosStr'] = ranks["PosStr"] + '/SS'
  ranks.loc[(ranks['SS'] == True) & (ranks['PosStr'] == ""), 'PosStr'] = ranks["PosStr"] + 'SS'

  ranks.loc[(ranks['Util'] == True) & (ranks['PosStr'] == ""), 'PosStr'] = ranks['PosStr'] + 'DH'

  ranks.loc[(ranks['SP'] == True) & (ranks['PosStr'] != ""), 'PosStr'] = ranks["PosStr"] + '/SP'
  ranks.loc[(ranks['SP'] == True) & (ranks['PosStr'] == ""), 'PosStr'] = ranks["PosStr"] + 'SP'

  ranks.loc[(ranks['RP'] == True) & (ranks['PosStr'] != ""), 'PosStr'] = ranks['PosStr'] + '/RP'
  ranks.loc[(ranks['RP'] == True) & (ranks['PosStr'] == ""), 'PosStr'] = ranks['PosStr'] + 'RP'

  hitters = ranks[(ranks['Util'] == True) & (ranks['VORP'] >= -10)]
  # default_counts = hitters['DefaultPos'].value_counts()
  # print(default_counts)

  # guesses, how do we calculate these in the future
  # TODO C_VP
  SP_VP = .105
  HITTER_VP = .085
  RP_VP = .055

  ranks.loc[ranks['isRP'] == True, 'Projected $'] = ranks['VORP'] * RP_VP
  ranks.loc[(ranks['isRP'] == False) & (ranks['Util'] == True), 'Projected $'] = ranks['VORP'] * HITTER_VP
  ranks.loc[(ranks['isRP'] == False) & (ranks['Util'] == False), 'Projected $'] = ranks['VORP'] * SP_VP

  ranks.sort_values(by='Projected $', ascending=False, inplace=True)
  ranks.loc[(ranks['Projected $'] <= 1) & (ranks['Projected $'] > -5), 'Projected $'] = 1
  ranks.loc[(ranks['Projected $'] <= -5), 'Projected $'] = 0


  ranks.loc[ranks['Espn_proj'].isna(), 'Espn_proj'] = 0
  ranks.loc[ranks['Espn_proj'] == False, 'Espn_proj'] = 0
  ranks.loc[ranks['Espn_proj'] == 'False', 'Espn_proj'] = 0
  ranks['Espn_proj'] = ranks['Espn_proj'].astype(float)
  ranks['Espn_dif'] = ranks['PTS'] - ranks['Espn_proj']
  ranks['Espn_dif'] = ranks['Espn_dif'].round(2)

  ranks_preview = ranks[['NameASCII','Pro', 'DefaultPos', 'PosStr', 'TJ', 'Level', 'Yrs', 'Cost', 'Note', 'contractType', 'PTS', 'PTS/G', 'VORP', 'Projected $']]
  # print(ranks_preview[ranks_preview['DefaultPos'] == 'SP'].head(108))
  # print(ranks_preview[ranks_preview['contractType'].str.startswith('arb') == True].head(50))
  return(ranks)

def export_to_csv(ranks):
  export_array = ['NameASCII', 'Pro', 'PosStr', 'Age', 'TJ', 'Yrs', 'Cost', 'Espn_dif', 'Espn_proj','PTS', 'PTS/G', 'VORP', 'Projected $']
  arb_export = ranks[ranks['contractType'].str.startswith('arb') == True]
  arb_export = arb_export[['NameASCII', 'Pro', 'PosStr', 'Age', 'TJ', 'contractType', 'Cost', 'Espn_proj', 'PTS', 'PTS/G', 'VORP', 'Projected $']]
  arb_export.sort_values(by=['contractType', 'VORP'], ascending=[False, False], inplace=True)
  arb_export.to_csv('exp_arb.csv', index=False)

  pos_array = ['C', '1B', '2B', '3B', 'SS', 'OF', 'SP', 'RP']
  for pos in pos_array:
    pos_export = ranks[ranks[pos] == True]
    pos_export = pos_export[export_array]
    pos_export.to_csv(f'exp_{pos}.csv', index=False)
  return

contracts = add_ids(contracts)
print(contracts.columns)
contracts = format_contracts(contracts)
print(contracts.columns)
merged = add_projections(contracts)
print(merged.columns)
ranks = add_positions(merged)
print(ranks.columns)
w_vorp = add_vorp(ranks)
print(w_vorp.columns)
export_to_csv(w_vorp)

# print(w_vorp)


# yb = (w_vorp[w_vorp['TJ'] == 'Young Bucks'])
# print(yb.shape)
# print(yb.head(50))
