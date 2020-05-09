"""
es21.sorters
============

Include all sorters of preachers.
"""

from collections import namedtuple

from flask import current_app as app
from tinydb import Query

from .database import get_db
from .filters import not_returned


q = Query()


def tri_pionner(preachers, month=None):
    """
    Sort all :param preachers: to 3 type in :param month:
    - default
    - auxiliary pionner
    - regular pionner
    """

    mdb = get_db('mpanampy')
    month = month or str(app.config['MONTH'])
    aux_list = mdb.get(q.volana == month)

    try:
        aux_list = aux_list['mpitory']
    except TypeError:
        aux_list = []

    non = []  # basic preachers
    aux = []  # auxiliar pionner
    reg = []  # regular pionner

    for preacher in preachers:
        if preacher['id'] in aux_list:
            aux.append(preacher)

        elif preacher['maharitra']:
            reg.append(preacher)

        else:
            non.append(preacher)

    result = namedtuple('TriPionner', ['non', 'aux', 'reg', 'all'])
    return result(non, aux, reg, preachers)


def sort_hour(preachers, month=None):
    """
    Sort all :param preachers: to 3 type in :param month:
    - hour < 5
    - 5 < hour < 9
    - hour >= 10
    """

    month = month or str(app.config['MONTH'])
    notReturned = not_returned(month)

    less_than_5 = []
    between_5_9 = []
    more_than_10 = []

    for preacher in preachers:
        if notReturned(preacher):
            less_than_5.append(preacher)
            continue

        hour = preacher['tatitra'][month]['ora']

        if hour < 5:
            less_than_5.append(preacher)
            continue

        if 5 <= hour < 10:
            between_5_9.append(preacher)
            continue

        if hour >= 10:
            more_than_10.append(preacher)

    result = namedtuple('SortHour', ['less_than_5',
                                     'between_5_9',
                                     'more_than_10'], )

    return result(less_than_5, between_5_9, more_than_10)
