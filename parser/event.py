import json
from pydantic import BaseModel
from db.models import Regatta
import datetime


class Event(BaseModel):
    YachtClass: str
    RegattaName: str
    RegattaStartDate: datetime.date
    RegattaEndDate: datetime.date
    RegattaLocation: str
    Url: str = None
    Tags: list = None


def event(data: dict) -> Event:
    return Event(**data)


def event_from_db(regatta: Regatta) -> Event:
    if regatta.tags != 'None':
        tags = [s.replace("'", "").strip() for s in regatta.tags[1:-1].split(',')]
    else:
        tags = None
    regatta_data = {
        'YachtClass': regatta.yachtclass,
        'RegattaName': regatta.regattaname,
        'RegattaStartDate': regatta.regattastartdate,
        'RegattaEndDate': regatta.regattastartdate,
        'RegattaLocation': regatta.regattalocation,
        'Url': regatta.url,
        'Tags': tags
    }
    return Event(**regatta_data)
