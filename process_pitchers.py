import pandas as pd

df = pd.read_csv('pitchers.csv')
print(df.head())
print(df.columns)

W = 10
SV = 10
SO = 1
CG = 5
ER = -1
HBP = -0.5
BB = -0.5
H = -0.5
IP = 2

df['PTS'] = (W*df['W'] + SV*df['SV'] + SO*df['SO'] + ER*df['ER'] + BB*df['BB'] + H*df['H'] + HBP*df['HBP'] + IP*df['IP']).round(2)
df['PTS/G'] = df['PTS'] / df['G']
df['PTS/G'] = df['PTS/G'].round(2)
df['ERA'] = df['ERA'].round(2)
df['RPS'] = df['G'] - df['GS'].astype(int)
df['isRP'] = (df['RPS'] > 10) & (df['GS'] < 15)
# simp = df[['RP', 'Name', 'Team', 'PTS', 'PTS/G', 'NameASCII', 'PlayerId', 'MLBAMID']].sort_values(by='PTS', ascending=False)
rp = (df[df['isRP']])
sp = (df[~df['isRP']])

# SP
sp = sp[['Name', 'Team', 'RPS', 'GS', 'PTS', 'PTS/G', 'SV', 'HLD', 'NameASCII', 'PlayerId', 'MLBAMID']].sort_values(by='PTS', ascending=False).reset_index(drop=True)

replacement_sp = sp.iloc[96-5:96+5]
replacement_level_sp = replacement_sp['PTS'].mean()
sp['VORP'] = sp['PTS'] - replacement_level_sp
print(sp.head(25))

# RP
rp = rp[['Name', 'Team', 'RPS', 'GS', 'PTS', 'PTS/G', 'SV', 'HLD', 'NameASCII', 'PlayerId', 'MLBAMID']].sort_values(by='PTS', ascending=False).reset_index(drop=True)

replacement_rp = rp.iloc[21:26]
replacement_level_rp = replacement_rp['PTS'].mean()
rp['VORP'] = rp['PTS'] - replacement_level_rp
print(rp.head(25))


