import aiogram.utils.markdown as fmt
from parser.event import Event
from db.utils import find_by_name, find_by_date


def create_answer(regatta: Event):
    start = regatta.RegattaStartDate
    end = regatta.RegattaEndDate
    date = f'{start.day}.{start.month}.{start.year}-{end.day}.{end.month}.{end.year}'
    text = fmt.text(
        fmt.text(regatta.YachtClass, '\n'),
        fmt.text(regatta.RegattaName, '\n'),
        fmt.text(date, '\n'),
        fmt.text(regatta.RegattaLocation, '\n'),
        sep='\n',
    )
    return text


def date_response(data: dict):
    regattas = find_by_date(data)
    return [create_answer(r) for r in regattas]


def name_response(data: dict):
    regattas = find_by_name(data)
    return [create_answer(r) for r in regattas]
