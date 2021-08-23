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


from es21.filters import Filter, not_returned
from es21.config import Config


db = get_db()
MONTH = Config.MONTH


def main():
    try:
        andn = int(input("Numero andiampitory: "))
    except:
        return

    f = Filter(db.all())
    f("in_group", andn)

    for p in f.preachers:
        anarana = p["anarana_feno"] if p.get("anarana_feno") else f"{p['anarana']} {p['fanampinanarana']}"

        months = [
            MONTH.new_me("sep_2020"),
            MONTH.new_me("oct_2020"),
            MONTH.new_me("nov_2020"),
            MONTH.new_me("dec_2020"),
            MONTH.new_me("jan_2021"),
            MONTH.new_me("feb_2021"),
            MONTH.new_me("mar_2021"),
            MONTH.new_me("apr_2021"),
        ]

        print(anarana)
        for month in months:
            if not_returned(str(month))(p):
                print(f"  Tapaka ny {month.prettie()}")

        print()

if __name__ == "__main__":
    main()
