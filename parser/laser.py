import requests
import datetime
from bs4 import BeautifulSoup
from parser.parser_config import url_ilca, month_dict_49
from parser.event import *


def compute_date(date: str) -> datetime.date:
    date = date.split(' ')[-3:]
    day = int(date[0])
    month = month_dict_49[date[1]]
    year = int(date[2])
    return datetime.date(year, month, day)


def find_content():
    response = requests.get(url_ilca)
    soup = BeautifulSoup(response.text, 'lxml')
    content = soup.find_all('div', class_='well ilcaWell')
    return content


def choose_yacht_class(regatta_name: str) -> str:
    if 'Laser Radial' in regatta_name:
        return 'Laser Radial'
    elif 'Laser 4.7' in regatta_name:
        return 'Laser 4.7'
    else:
        return 'Laser'


def find_params(cont):
    name = cont.find('div', class_='eventListTitle').text.replace('\t', '').replace('\n', '').lstrip().rstrip()
    yacht_class = choose_yacht_class(name)
    info = cont.find('div', class_='span8')
    date_place = info.find('b').text.replace('\t', '').lstrip().split('\n')[:-1]
    place = date_place[1].lstrip().rstrip()

    date = date_place[0].split(' - ')
    date_start = compute_date(date[0])
    date_end = compute_date(date[1])

    regatta_dict = {
        'YachtClass': yacht_class,
        'RegattaName': name,
        'RegattaStartDate': date_start,
        'RegattaEndDate': date_end,
        'RegattaLocation': place,
    }
    return regatta_dict


def get_data_laser():
    content = find_content()
    return [event(find_params(i)) for i in content]
