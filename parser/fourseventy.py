import requests
import datetime
from bs4 import BeautifulSoup
from parser.parser_config import month_dict, year, url_470
from parser.event import *


def find_date(content):
    info = content.find('div', class_='col-sm-1 col-xs-2 fechas-float-l')
    d = info.find_all('div')
    date = info.find_all('span', class_='month')
    month_start = date[0].text
    month_end = date[1].text
    start = d[0].text.replace('\n', '').replace(' ', '').replace('\t', '').replace(month_start, '')
    end = d[-1].text.replace('\n', '').replace(' ', '').replace('\t', '').replace(month_end, '')
    date_start = datetime.date(year, month_dict[month_start], int(start))
    date_end = datetime.date(year, month_dict[month_end], int(end))
    return [date_start, date_end]


def find_name(content):
    info = content.find('div', class_='col-xs-12 p-t-5')

    tag = info.find_all('span')
    tags = []
    for t in tag:
        tags.append(t.text)
    name = info.find('h2')
    name_text = name.text.replace('\n', '')
    name_href = 'http://www.470.org/' + name.find('a').get('href')
    try:
        place = content.find('div', class_='col-sm-12').find('span').text
    except AttributeError:
        r = requests.get(name_href)
        s = BeautifulSoup(r.text, 'lxml')
        regatta = s.find('div', class_="content").find('div', class_='row').find_all('div', recursive=False)[1]
        place = regatta.find('div', class_='col-sm-12')
        country = place.find('span').text

        town = place.text.replace('\n', '').replace('\t', '').replace(country, '').replace(' ', '')
        if town:
            place = town + ', ' + country
        else:
            place = country

    return [name_text, place, name_href, tags]


def event_dict(cont):
    date = find_date(cont)
    name = find_name(cont)
    regatta_dict = {
        'YachtClass': '470',
        'RegattaName': name[0],
        'RegattaStartDate': date[0],
        'RegattaEndDate': date[1],
        'RegattaLocation': name[1],
        'Url': name[2],
        'Tags': name[3]
    }
    return regatta_dict


def get_data_470() -> list:
    response = requests.get(url_470)
    soup = BeautifulSoup(response.text, 'lxml')
    content = soup.find('div', class_="content").find('div', class_='row').find_all('div', recursive=False)[3:-1]
    return [event(event_dict(i)) for i in content]
