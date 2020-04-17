from datetime import datetime, date

from flask import (
    current_app as app,
    g, )

from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb_serialization import Serializer, SerializationMiddleware


class DateSerializer(Serializer):
    OBJ_CLASS = date
    FORMAT = '%Y-%m-%d'

    def encode(self, obj):
        return obj.strftime(self.FORMAT)

    def decode(self, s):
        d = datetime.strptime(s, self.FORMAT)

        return date(d.year, d.month, d.day)


def get_db(table=None):
    if 'db' not in g:
        serializer = SerializationMiddleware(JSONStorage)
        serializer.register_serializer(DateSerializer(), 'TinyDate')

        g.db = TinyDB(app.config['DATABASE'], storage=serializer, indent=4)

    if table is None:
        return g.db
    else:
        return g.db.table(table)


def close_db(e=None):
    g.pop('db', None)


def init_app(app):
    app.teardown_appcontext(close_db)
