from sqlalchemy import Column, Integer, String, Date
from .database import Base


class Regatta(Base):
    __tablename__ = 'regattas'
    id = Column(Integer, primary_key=True, index=True)
    yachtclass = Column(String)
    regattaname = Column(String)
    regattastartdate = Column(Date)
    regattaenddate = Column(Date)
    regattalocation = Column(String)
    url = Column(String, nullable=True)
    tags = Column(String, nullable=True)