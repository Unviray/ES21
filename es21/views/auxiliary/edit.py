"""
es21.views.auxiliary.edit
=========================

Add/Remove/Update preacher in auxiliary pionner place.
"""

from flask import (
    flash,
    request,
    redirect,
    url_for as url, )

from tinydb import Query
from tinydb.operations import set

from ...database import get_db
from ...utils import get_service_year


q = Query()


def entry(id):
    mdb = get_db('mpanampy')
    service_year = get_service_year()

    for service_month in service_year:
        month = str(service_month)
        preacher = getsert(month)['mpitory']

        if request.form.get(month) in (None, 'off', False):
            if id in preacher:
                preacher.remove(id)
                mdb.update(set('mpitory', preacher), q.volana == month)

        else:
            if id not in preacher:
                preacher.append(id)
                mdb.update(set('mpitory', preacher), q.volana == month)

    flash('Tontosa ny fampidirana mpisavalalana mpanampy', 'success')

    return redirect(url('main.preacher', id=id))


def getsert(key):
    """
    Get or insert if no record.
    """

    mdb = get_db('mpanampy')

    result = mdb.get(q.volana == key)

    if result is not None:
        return result
    else:
        mdb.insert(dict(volana=key, mpitory=[]))
        return getsert(key)
