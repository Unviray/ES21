"""
es21.views.auxiliary.home
=========================

Home entry page for auxiliary pionner.
"""

from flask import current_app as app

from tinydb import Query

from ...utils import templated, navbar_form
from ...database import get_db


@templated('auxiliary/home.html')
@navbar_form
def entry():
    db = get_db()
    mdb = get_db('mpanampy')
    q = Query()

    MONTH = str(app.config['MONTH'])

    ids = mdb.get(q.volana == MONTH)['mpitory']

    preacher = db.search(q.id.one_of(ids))

    return dict(preacher=preacher)
