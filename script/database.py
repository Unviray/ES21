from pathlib import Path
from datetime import datetime, date

from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb_serialization import Serializer, SerializationMiddleware


PATH = Path.home() / '.es21/'

DATABASE = PATH / 'db.json'


class DateSerializer(Serializer):
    OBJ_CLASS = date
    FORMAT = '%Y-%m-%d'

    def encode(self, obj):
        return obj.strftime(self.FORMAT)

    def decode(self, s):
        d = datetime.strptime(s, self.FORMAT)

        return date(d.year, d.month, d.day)


def get_db(table=None):
    serializer = SerializationMiddleware(JSONStorage)
    serializer.register_serializer(DateSerializer(), 'TinyDate')

    db = TinyDB(DATABASE, storage=serializer, indent=4)

    if table is None:
        return db
    else:
        return db.table(table)


from es21.filters import Filter, not_returned, returned
from es21.config import Config


db = get_db()
MONTH = Config.MONTH


def ret6():
    """
    if returned once in 6 month
    """

    f = Filter(db.all())

    for p in f.preachers:
        anarana = p["anarana_feno"] if p.get("anarana_feno") else f"{p['anarana']} {p['fanampinanarana']}"

        months = [
            MONTH.new_me("dec_2022"),
            MONTH.new_me("jan_2023"),
            MONTH.new_me("feb_2023"),
            MONTH.new_me("mar_2023"),
            MONTH.new_me("apr_2023"),
            MONTH.new_me("may_2023"),
        ]

        for month in months:
            if returned(str(month))(p):
                break
        else:
            print(f"{anarana}")

def main_count():
    """
    if not returned once in 6 month
    """

    f = Filter(db.all())

    for p in f.preachers:
        t=0
        anarana = p["anarana_feno"] if p.get("anarana_feno") else f"{p['anarana']} {p['fanampinanarana']}"

        months = [
            MONTH.new_me("sep_2022"),
            MONTH.new_me("oct_2022"),
            MONTH.new_me("nov_2022"),
            MONTH.new_me("dec_2022"),
            MONTH.new_me("jan_2023"),
            MONTH.new_me("feb_2023"),
        ]

        for month in months:
            if not_returned(str(month))(p):
                t+=1
        if t == 6:
            print(anarana)

def main():
    """
    if not returned once in 6 month
    """

    f = Filter(db.all())

    for p in f.preachers:
        t=0
        anarana = p["anarana_feno"] if p.get("anarana_feno") else f"{p['anarana']} {p['fanampinanarana']}"

        months = [
            MONTH.new_me("nov_2023"),
            MONTH.new_me("dec_2023"),
            MONTH.new_me("jan_2024"),
            MONTH.new_me("feb_2024"),
            MONTH.new_me("mar_2024"),
            MONTH.new_me("apr_2024"),
        ]

        for month in months:
            if not_returned(str(month))(p):
                t+=1
        if t == 6:
            print(anarana)

if __name__ == "__main__":
    main()
