"""
es21.sorters
============

Include all sorters of preachers.
"""

from collections import namedtuple

from flask import current_app as app
from tinydb import Query

from .database import get_db


q = Query()


def tri_pionner(preachers, month=None):
    """
    Sort all :param preachers: to 3 type in :param month:
    """

    mdb = get_db('mpanampy')
    month = month or str(app.config['MONTH'])

    non = []  # basic preachers
    aux = []  # auxiliar pionner
    reg = []  # permanent pionner

    for preacher in preachers:
        if preacher['id'] in mdb.get(q.volana == month)['mpitory']:
            aux.append(preacher)

        elif preacher['maharitra']:
            reg.append(preacher)

        else:
            non.append(preacher)

    result = namedtuple('TriPionner', ['non', 'aux', 'reg', 'all'])
    return result(non, aux, reg, preachers)
