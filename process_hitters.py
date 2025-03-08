import pandas as pd

df = pd.read_csv('batters.csv')

df['PTS'] = (df['1B'] + 2*df['2B'] + 3*df['3B'] + 4*df['HR'] + df['R'] + df['RBI'] + 2*df['SB'] + df['BB']).round(0)
df['PTS/G'] = df['PTS'] / df['G']
df['PTS/G'] = df['PTS/G'].round(2)
print(df.columns)

simp = df[['Name', 'Team', 'PTS', 'PTS/G', 'NameASCII', 'PlayerId', 'MLBAMID']].sort_values(by='PTS', ascending=False).reset_index(drop=True)

print(simp.head(100))