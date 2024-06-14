from pathlib import Path
from datetime import datetime, date
import json
from tomark import Tomark
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb_serialization import Serializer, SerializationMiddleware


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


from es21.filters import Filter, in_group
from es21.config import Config


db = get_db()
MONTH = Config.MONTH


def main():
    """
    if not returned once in 6 month
    """

    f = Filter(db.all())

    months = [
        MONTH.new_me("nov_2023"),
        MONTH.new_me("dec_2023"),
        MONTH.new_me("jan_2024"),
        MONTH.new_me("feb_2024"),
        MONTH.new_me("mar_2024"),
        MONTH.new_me("apr_2024"),
    ]

    # Mpisavalalana maharitra
    #f("is_regular")

    # Vita batisa
    #f("baptised")
    #f("is_not_regular")

    # Tsy vita batisa
    #f("not_baptised")
    #f("is_not_regular")

    # Tapaka
    f("stopped", months)

    for p in f.preachers:
        anarana = (
            p["anarana_feno"]
            if p.get("anarana_feno")
            else f"{p['anarana']} {p['fanampinanarana']}"
        )
        print(f"# {anarana}")

        data = []
        for month in months:
            report = p["tatitra"].get(
                str(month),
                {
                    "zavatra_napetraka": 0,
                    "video": 0,
                    "ora": 0,
                    "fitsidihana": 0,
                    "fampianarana": 0,
                    "fanamarihana": "",
                    "mpisavalalana": "",
                },
            )

            del report["zavatra_napetraka"]
            del report["video"]
            del report["fitsidihana"]

            if report["mpisavalalana"] != "Reg" and report["mpisavalalana"] != "Aux":
                report["ora"] = (
                    "X" if report["ora"] > 0 else ""
                )

            report["mpisavalalana"] = {
                "Reg": "Maharitra",
                "Aux": "Mpanampy",
                "": "",
            }.get(report["mpisavalalana"], "")

            data.append({"volana": month.prettie(), **report})

        print(Tomark.table(data))


if __name__ == "__main__":
    main()
