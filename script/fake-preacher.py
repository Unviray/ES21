from pathlib import Path
from datetime import datetime, date

from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb_serialization import Serializer, SerializationMiddleware
from tinydb import Query


PATH = Path.home() / ".es21/"

DATABASE = PATH / "db.json"


class DateSerializer(Serializer):
    OBJ_CLASS = date
    FORMAT = "%Y-%m-%d"

    def encode(self, obj):
        return obj.strftime(self.FORMAT)

    def decode(self, s):
        d = datetime.strptime(s, self.FORMAT)

        return date(d.year, d.month, d.day)


def get_db(table=None):
    serializer = SerializationMiddleware(JSONStorage)
    serializer.register_serializer(DateSerializer(), "TinyDate")

    db = TinyDB(DATABASE, storage=serializer, indent=4)

    if table is None:
        return db
    else:
        return db.table(table)


from es21.filters import Filter, not_returned, returned
from es21.config import Config

q = Query()


db = get_db()
mdb = get_db("mpanampy")

MONTH = Config.MONTH


def main():
    """
    if not returned once in 6 month
    """

    f = Filter(db.all())
    aux_list = mdb.get(q.volana == str(MONTH))

    def fake_preacher():
        month = str(MONTH)

        def func(preacher):
            try:
                hour = preacher["tatitra"][month]["ora"]
                return (
                    (hour > 1)
                    and (not (preacher["id"] in aux_list))
                    and (preacher["tatitra"][str(MONTH)]["mpisavalalana"] == "")
                )

            except KeyError:
                return False

        return func

    f.register_filter(fake_preacher)

    f("fake_preacher")

    hour = 0

    for p in f.preachers:
        anarana = (
            p["anarana_feno"]
            if p.get("anarana_feno")
            else f"{p['anarana']} {p['fanampinanarana']}"
        )

        hour += p["tatitra"][str(MONTH)]["ora"]
        print(anarana)
    print(len(f.preachers))
    print(hour)


if __name__ == "__main__":
    main()
