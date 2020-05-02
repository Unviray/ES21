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

    # growth widget
    growth = [
        growth_data('zavatra_napetraka', 'Zavatra napetraka', preachers),
        growth_data('video', 'Video', preachers),
        growth_data('ora', 'Ora', preachers),
        growth_data('fitsidihana', 'Fitsidihana', preachers),
        growth_data('fampianarana', 'Fampianarana', preachers),
    ]

    return dict(
        growth=growth,
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
    ChartData = namedtuple('ChartData', ['legend', 'label', 'data'])

    label = []
    data = []

    for month in service_year:
        fr = Filter(preachers)
        fr('is_auxiliary', month=str(month))
        fr('returned', month=str(month))

        s_hour = sum([pr['tatitra'][str(month)]['ora'] for pr in fr.preachers])

        label.append(month.prettie('{short_month} {short_year}'))
        data.append((s_hour,))

    return ChartData(['Ora'], label, data)


def growth_data(id, name, preachers):
    GrowthData = namedtuple('GrowthData', ['desc', 'last', 'now'])

    MONTH = app.config['MONTH']

    month = str(MONTH)
    last_month = MONTH.new_me() - 1

    def get_data(pr, month):
        return pr['tatitra'][str(month)][id]

    f = Filter(preachers)
    f('returned', month=str(month))
    last_f = Filter(preachers)
    last_f('returned', month=str(last_month))

    now_data = sum([get_data(pr, month) for pr in f.preachers])
    last_data = sum([get_data(pr, last_month) for pr in last_f.preachers])

    return GrowthData(name, last_data, now_data)
