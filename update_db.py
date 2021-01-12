from time import time
from db.crud import create_regatta, get_regattas, delete_regatta
from db.database import SessionLocal
from parser.laser import get_data_laser
from parser.fournine import get_data_49er
from parser.fourseventy import get_data_470

t1 = time()
data = get_data_470() + get_data_49er() + get_data_laser()
db = SessionLocal()
regattas = get_regattas(db)
for r in regattas:
    if r not in data:
        delete_regatta(db, r.RegattaName)
for regatta in data:
    if regatta.YachtClass == 'Laser 4.7':
        continue
    if regatta not in regattas:
        create_regatta(db, regatta)
db.close()
print(round(time() - t1, 2))
