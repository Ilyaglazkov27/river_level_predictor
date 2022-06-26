import pandas as pd
import json
data = pd.read_excel('./level_data.xlsx')
all_data = []
for year in range(52, 71):
    year_data = []
    for month in range(1, 13):
        year_data.append(data[month][year])
    all_data.append(year_data)
print(all_data)
with open('level_data.txt', 'w') as filehandle:
    json.dump(all_data, filehandle)

with open('level_data.txt', 'r') as filehandle:
    data = json.load(filehandle)
