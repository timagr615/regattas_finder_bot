import aiogram.utils.markdown as fmt
from parser.event import Event
from db.utils import find_by_name, find_by_date


def create_answer(regatta: Event):
    start = regatta.RegattaStartDate
    end = regatta.RegattaEndDate
    date = f'{start.day}.{start.month}.{start.year}-{end.day}.{end.month}.{end.year}'
    text = fmt.text(
        fmt.text(fmt.hbold(regatta.YachtClass)),
        fmt.text(fmt.hunderline(regatta.RegattaName)),
        fmt.text(date, '\n'),
        fmt.text(regatta.RegattaLocation, '\n'),
        sep='\n',
    )
    return [regatta.YachtClass, regatta.RegattaName, date, regatta.RegattaLocation]


def text_answer(data: list):
    text = fmt.text(
        fmt.text(fmt.hbold(data[0])),
        fmt.text(fmt.hunderline(data[1])),
        fmt.text(data[2], '\n'),
        fmt.text(data[3], '\n'),
        sep='\n',
    )
    return text


def date_response(data: dict):
    return [create_answer(r) for r in find_by_date(data)]


def name_response(data: dict):
    return [create_answer(r) for r in find_by_name(data)]
