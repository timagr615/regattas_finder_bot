import requests
import datetime
from bs4 import BeautifulSoup
from parser.parser_config import url_49er, month_dict_49, year
from parser.event import *


def compute_date(date: str) -> datetime.date:
    start_list = date.split(' ')
    start_month = month_dict_49[start_list[0]]
    start_day = int(start_list[1].replace('th', '').replace('rd', '').replace('nd', '').replace('st', ''))
    return datetime.date(year, start_month, start_day)


def find_content():
    response = requests.get(url_49er)
    soup = BeautifulSoup(response.text, 'lxml')
    content = soup.find('div', class_='tab-content active').find_all('div', class_='event-item')
    return content


def find_params(event_info):
    date_place = event_info.find('div', class_='meta-line').text
    name_url = event_info.find('h3').find('a')
    name = name_url.text
    url = name_url.get('href')

    info = date_place.split(',')

    date = info.pop(0).split(' - ')
    start = date[0]
    end = date[1]
    start_date = compute_date(start)
    end_date = compute_date(end)
    place = ''
    for i in info:
        place += i + ','
    place = place[1:-1]
    regatta_dict = {
        'YachtClass': '49er',
        'RegattaName': name,
        'RegattaStartDate': start_date,
        'RegattaEndDate': end_date,
        'RegattaLocation': place,
        'Url': url,
    }
    return regatta_dict


def get_data_49er():
    content = find_content()
    return [event(find_params(i)) for i in content]
