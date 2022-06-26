import json

with open('level_data.txt', 'r') as filehandle:
    level_data = json.load(filehandle)
with open('weather_data.txt', 'r') as filehandle:
    weather_data = json.load(filehandle)

dataset_x = []
dataset_y = []
for year in range(0, 19):
    for month in range(12):
        lst = []
        if month > 0:
            for w in weather_data[year][month-1][len(weather_data[year][month-1])-90+len(weather_data[year][month]):] + weather_data[year][month]:
                lst.append(list(w.values()))
        else:
            if year > 0:
                for w in weather_data[year-1][11][len(weather_data[year-1][11]) - 90+len(weather_data[year][month]):] + weather_data[year][month]:
                    lst.append(list(w.values()))
        if lst:
            if len(lst) == 90:
                dataset_x.append(lst)
                dataset_y.append(level_data[year][month])

for i in dataset_x:
    if len(i) != 90:
        print(len(i))

