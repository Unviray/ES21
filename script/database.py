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
