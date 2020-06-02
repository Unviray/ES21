from pathlib import Path
from datetime import date

import pytest

from es21 import create_app
from es21.config import MonthBase


class Config(object):
    y = date.today().year
    m = date.today().month

    last_month = MonthBase(date(year=y, month=m, day=1))  # day 1 is ignored

    MONTH = last_month - 1

    SECRET_KEY = 'dev'

    PATH = Path('./test_dir')

    DATABASE = PATH / 'db.json'
    LOG = PATH / 'log'


@pytest.fixture
def client():
    app = create_app({
        'MONTH': Config.MONTH,
        'SECRET_KEY': Config.SECRET_KEY,
        'PATH': Config.PATH,
        'DATABASE': Config.DATABASE,
        'LOG': Config.LOG,

        'TESTING': True,
    })

    with app.test_client() as cl:
        yield cl

    for _file in app.config['PATH'].iterdir():
        _file.unlink()

    app.config['PATH'].rmdir()
