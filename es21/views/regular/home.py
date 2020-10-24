"""
es21.views.regular.home
=========================

Home entry page for regular pionner.
"""

from collections import namedtuple

from flask import current_app as app

from tinydb import Query

from ...utils import templated, navbar_form, get_service_year
from ...database import get_db
from ...filters import Filter, returned

from es21._type import _sum


@templated('group/home.html')
@navbar_form
def entry():
    db = get_db()
    q = Query()

    preachers = db.search(q.maharitra == True)  # noqa

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
    growth_six = [
        growth_data_six('zavatra_napetraka', 'Zavatra napetraka', preachers),
        growth_data_six('video', 'Video', preachers),
        growth_data_six('ora', 'Ora', preachers),
        growth_data_six('fitsidihana', 'Fitsidihana', preachers),
        growth_data_six('fampianarana', 'Fampianarana', preachers),
    ]

    return dict(
        id='is_regular',
        short_name='maharitra',
        name='mpisavalalana maharitra',
        color='warning',

        growth=growth,
        growth_six=growth_six,
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
    ChartData = namedtuple('ChartData', ['legend', 'id', 'label', 'data'])

    label = []
    data = []

    for month in service_year:
        fr = Filter(preachers)
        fr('is_regular')
        fr('returned', month=str(month))

        s_hour = _sum([pr['tatitra'][str(month)]['ora'] for pr in fr.preachers])

        label.append(month.prettie('{short_month} {short_year}'))
        data.append((s_hour,))

    return ChartData(['Ora'], ['reg'], label, data)


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

    now_data = _sum([get_data(pr, month) for pr in f.preachers])
    last_data = _sum([get_data(pr, last_month) for pr in last_f.preachers])

    return GrowthData(name, last_data, now_data)


def growth_data_six(id, name, preachers):
    GrowthData = namedtuple('GrowthData', ['desc', 'last', 'now'])

    MONTH = app.config['MONTH']

    month = str(MONTH)
    last_month_1 = MONTH.new_me() - 1
    last_month_2 = MONTH.new_me() - 2
    last_month_3 = MONTH.new_me() - 3
    last_month_4 = MONTH.new_me() - 4
    last_month_5 = MONTH.new_me() - 5
    last_month_6 = MONTH.new_me() - 6

    def get_data(pr, month):
        return pr['tatitra'][str(month)][id]

    f = Filter(preachers)
    f('returned', month=str(month))

    last_f1 = Filter(preachers)
    last_f1('returned', month=str(last_month_1))

    last_f2 = Filter(preachers)
    last_f2('returned', month=str(last_month_2))

    last_f3 = Filter(preachers)
    last_f3('returned', month=str(last_month_3))

    last_f4 = Filter(preachers)
    last_f4('returned', month=str(last_month_4))

    last_f5 = Filter(preachers)
    last_f5('returned', month=str(last_month_5))

    last_f6 = Filter(preachers)
    last_f6('returned', month=str(last_month_6))

    now_data = _sum([get_data(pr, month) for pr in f.preachers])
    last_data_1 = _sum([get_data(pr, last_month_1) for pr in last_f1.preachers])
    last_data_2 = _sum([get_data(pr, last_month_2) for pr in last_f2.preachers])
    last_data_3 = _sum([get_data(pr, last_month_3) for pr in last_f3.preachers])
    last_data_4 = _sum([get_data(pr, last_month_4) for pr in last_f4.preachers])
    last_data_5 = _sum([get_data(pr, last_month_5) for pr in last_f5.preachers])
    last_data_6 = _sum([get_data(pr, last_month_6) for pr in last_f6.preachers])

    last_data = _sum([
        last_data_1,
        last_data_2,
        last_data_3,
        last_data_4,
        last_data_5,
        last_data_6,
    ]) / 6

    return GrowthData(name, last_data, now_data)
