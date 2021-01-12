from sqlalchemy.orm import Session
from parser.event import Event, event_from_db
from . import models


def create_regatta(db: Session, regatta: Event):
    db_regatta = models.Regatta(
        yachtclass=regatta.YachtClass,
        regattaname=regatta.RegattaName,
        regattastartdate=regatta.RegattaStartDate,
        regattaenddate=regatta.RegattaEndDate,
        regattalocation=regatta.RegattaLocation,
        url=regatta.Url,
        tags=str(regatta.Tags)
    )
    db.add(db_regatta)
    db.commit()
    db.refresh(db_regatta)
    return db_regatta


def delete_regatta(db: Session, regatta_name: str):
    db.query(models.Regatta).filter(models.Regatta.regattaname == regatta_name).delete(synchronize_session=False)
    db.commit()


def get_regattas(db: Session):
    regattas = db.query(models.Regatta).all()
    return [event_from_db(r) for r in regattas]
