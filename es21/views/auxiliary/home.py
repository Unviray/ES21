"""
es21.views.auxiliary.home
=========================

Home entry page for auxiliary pionner.
"""

from collections import namedtuple

from flask import current_app as app

from tinydb import Query

from ...utils import templated, navbar_form, get_service_year
from ...database import get_db
from ...filters import Filter, returned


@templated('auxiliary/home.html')
@navbar_form
def entry():
    db = get_db()
    mdb = get_db('mpanampy')
    q = Query()

    MONTH = str(app.config['MONTH'])

    ids = mdb.get(q.volana == MONTH)['mpitory']

    preachers = db.search(q.id.one_of(ids))

    # No report widget
    f = Filter(preachers)
    f('not_returned')
    not_returned = f.preachers

    return dict(
        preachers=preachers,
        not_returned=not_returned,
        hour_chart=hour_chart(db.all()),
        indiv_report=indiv_report(preachers), )


def indiv_report(preachers):
    MONTH = str(app.config['MONTH'])
    pr = namedtuple(
        'pr',
        ['pr_obj', 'publication', 'video', 'hour', 'visit', 'study'], )

    result = []
    for preacher in preachers:

        if returned()(preacher):
            result.append(pr(
                pr_obj=preacher,
                publication=preacher['tatitra'][MONTH]['zavatra_napetraka'],
                video=preacher['tatitra'][MONTH]['video'],
                hour=preacher['tatitra'][MONTH]['ora'],
                visit=preacher['tatitra'][MONTH]['fitsidihana'],
                study=preacher['tatitra'][MONTH]['fampianarana'], ))
        else:
            result.append(pr(
                pr_obj=preacher,
                publication=0,
                video=0,
                hour=0,
                visit=0,
                study=0, ))

    return result


def hour_chart(preachers):
    service_year = get_service_year()
    result = []

    for month in service_year:
        fr = Filter(preachers)
        fr('is_auxiliary', month=str(month))
        fr('returned', month=str(month))

        s_hour = sum([pr['tatitra'][str(month)]['ora'] for pr in fr.preachers])

        result.append((month.prettie('{short_month} {short_year}'), s_hour))

    return result
