from db.crud import get_regattas_by_yacht
from db.database import SessionLocal

date_dict = {'Январь-Март': [1, 3], 'Апрель-Июнь': [4, 6], 'Июль-Сентябрь': [7, 9], 'Октябрь-Декабрь': [10, 12],
             'Весь год': [1, 12]}

worlds = ['world', 'worlds', 'мир', 'world championship', 'worlds championship', 'чемпионат мира', 'wirld']

europeans = ['euro', 'european', 'europeans', 'euros', 'европа', 'евро', 'чемпионат европы']

junior = ['junior', 'junior worlds', 'u23 worlds', 'u23', 'юношеский', 'первенство', 'первенство мира', 'junior euro',
          'junior europeans', 'первенство европы', 'юношеский мир']

world_cup = ['world cup', 'cup', 'world cup series', 'series', 'кубок', 'кубок мира', 'этап', 'этап кубка мира',
             'worldcup',  'worldcup series', 'кубокмира']

olympics = ['olimpic', 'olympic', 'olympics', 'olimpics', 'olympic game', 'olympic games', 'olympics game',
            'olympics games', 'olimpic game', 'olimpic games', 'olimpics game', 'olimpics games', 'олимпийские игры',
            'олимпиада', 'олимп']

sofia = ['trofeoprincesasofia', 'princesa', 'sofia', 'princesa sofia', 'princess', 'princess sofia', 'софия',
         'принцеса', 'принцесса', 'принцесса', 'принцесса софия']

kiel = ['kieler woche', 'woche', 'kieler', 'kil', 'kill', 'kiel', 'киль', 'кильская', 'кильская регата',
        'кильская неделя']

hyeres = ['hyeres regatta', 'hyeres', 'yer', 'йер', 'йерская регата']


def find_by_boat(data: dict):
    yacht = data['boat']
    db = SessionLocal()
    regattas = get_regattas_by_yacht(db, yacht)
    db.close()
    return regattas


def find_by_date(data: dict):
    regattas = find_by_boat(data)
    monthes = date_dict[data['filter_type']]
    reg = [r for r in regattas if monthes[0] <= r.RegattaStartDate.month <= monthes[1]]
    print(reg)
    return reg


def find_by_name(data: dict):
    regattas = find_by_boat(data)
    name_part = data['filter_type'].lower()
    if name_part in worlds:
        name = 'world'
    elif name_part in europeans:
        name = 'euro'
    elif name_part in junior:
        name = 'junior'
    elif name_part in world_cup:
        name = 'cup'
    elif name_part in olympics:
        name = 'olympic'
    elif name_part in sofia:
        name = 'sofia'
    elif name_part in kiel:
        name = 'kiel'
    elif name_part in hyeres:
        name = 'hyer'
    else:
        name = name_part
    reg = [r for r in regattas if name in r.RegattaName.lower()]
    print(reg)
    return reg
