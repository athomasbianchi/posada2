import requests
import csv

url = 'https://www.fangraphs.com/api/projections?type=atc&stats=bat&pos=all&team=0&players=0&lg=all&z=1741684965525&download=1'

response = requests.request("GET", url)

print(response)
data = response.json()
print(data)

def write_csv(data, file_path):
      with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        
        if data:
            header = list(data[0].keys())
            writer.writerow(header)
            for row in data:
                writer.writerow(row.values())

write_csv(data, 'batters_2.csv')