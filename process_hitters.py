import pandas as pd

df = pd.read_csv('batters.csv')

df['PTS'] = (df['1B'] + 2*df['2B'] + 3*df['3B'] + 4*df['HR'] + df['R'] + df['RBI'] + 2*df['SB'] + df['BB']).round(0)
df['PTS/G'] = df['PTS'] / df['G']
df['PTS/G'] = df['PTS/G'].round(2)

simp = df[['Name', 'Team', 'PTS', 'PTS/G', 'NameASCII', 'PlayerId', 'MLBAMID']].sort_values(by='PTS', ascending=False).reset_index(drop=True)
simp.rename(columns={'PlayerId': 'FangraphsId'}, inplace=True)

replacement_h = simp.iloc[96-5:96+5]
replacement_level = replacement_h['PTS'].mean()
simp['VORP'] = simp['PTS'] - replacement_level

simp.to_csv('hitters_simp.csv', index=False)