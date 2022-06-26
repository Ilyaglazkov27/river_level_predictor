# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json



url = 'https://www.gismeteo.ru/diary/4608/'
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, lzma, sdch',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
}
def f(data):
    day_data = {}
    day_data["tempreture"] = int(data[0].text)
    day_data["pressure"] = int(data[1].text)

    if data[2].find('img'):
        if data[2].find('img')['src'].find("dull.png") != -1:
            day_data["cloudiness"] = 4
        elif data[2].find('img')['src'].find("suncl.png") != -1:
            day_data["cloudiness"] = 3
        elif data[2].find('img')['src'].find("sunc.png") != -1:
            day_data["cloudiness"] = 2
        else:
            day_data["cloudiness"] = 1
    else:
        day_data["cloudiness"] = 0

    if data[3].find('img'):
        if data[3].find('img')['src'].find("rain.png") != -1:
            day_data["phenomena"] = 3
        elif data[3].find('img')['src'].find("snow.png") != -1:
            day_data["phenomena"] = 2
        elif data[3].find('img')['src'].find("storm.png") != -1:
            day_data["phenomena"] = 1
        else:
            day_data["phenomena"] = 0
    else:
        day_data["phenomena"] = 0

    if data[4].find('span').text[0] == "Ш":
        day_data['direction'] = 1
        day_data['speed'] = 0
    else:
        if data[4].find('span').text[0] + data[4].find('span').text[1] == "С ":
            day_data['direction'] = 2
        elif data[4].find('span').text[0] + data[4].find('span').text[1] == "СЗ":
            day_data['direction'] = 3
        elif data[4].find('span').text[0] + data[4].find('span').text[1] == "З ":
            day_data['direction'] = 4
        elif data[4].find('span').text[0] + data[4].find('span').text[1] == "ЮЗ":
            day_data['direction'] = 5
        elif data[4].find('span').text[0] + data[4].find('span').text[1] == "Ю ":
            day_data['direction'] = 6
        elif data[4].find('span').text[0] + data[4].find('span').text[1] == "ЮВ":
            day_data['direction'] = 7
        elif data[4].find('span').text[0] + data[4].find('span').text[1] == "В ":
            day_data['direction'] = 8
        else:
            day_data['direction'] = 9
        text = data[4].find('span').text
        c = 1
        speed = 0
        for i in range(len(text) - 4, 0, -1):
            if text[i].isdigit():
                speed += c * int(text[i])
                c *= 10
            else:
                break
        day_data['speed'] = speed
    return day_data

alldata = []
for year in range(1998, 2017):
    year_data = []
    print(year)
    for month in range(1, 13):
        month_data = []
        page = requests.get(url + str(year) + "/" + str(month) + "/", headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        allDays = soup.findAll('tr', align='center')
        for day in allDays:
            try:
                data = list(day.children)
                data = list(filter(lambda a: a != '\n', data))
                day_data = f(data[1:6])
                month_data.append(day_data)
                day_data = f(data[6:])
                month_data.append(day_data)
            except:
                pass
        year_data.append(month_data)
    alldata.append(year_data)

with open('weather_data.txt', 'w') as filehandle:
    json.dump(alldata, filehandle)

with open('weather_data.txt', 'r') as filehandle:
    data = json.load(filehandle)

