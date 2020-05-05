"""
es21.views.main.home
====================

Home entry page.
"""

from collections import namedtuple

from flask import (
    current_app as app,
    render_template as render, )

from ...utils import templated, navbar_form, get_service_year
from ...database import get_db

from ...sorters import tri_pionner
from ...filters import Filter


@templated('home.html')
@navbar_form
def entry():
    db = get_db()

    preacher = db.all()

    if len(preacher) == 0:
        # empty database
        return render('welcome.html')

    # Post Report table widget
    f = Filter(db.all())
    f('returned')
    tri = tri_pionner(f.preachers)
    post = post_report(tri)

    # No report
    f = Filter(db.all())
    f('not_returned')
    not_returned = f.preachers

    # growth widget
    growth = [
        growth_data('zavatra_napetraka', 'Zavatra napetraka', preacher),
        growth_data('video', 'Video', preacher),
        growth_data('ora', 'Ora', preacher),
        growth_data('fitsidihana', 'Fitsidihana', preacher),
        growth_data('fampianarana', 'Fampianarana', preacher),
    ]
    growth_six = [
        growth_data_six('zavatra_napetraka', 'Zavatra napetraka', preacher),
        growth_data_six('video', 'Video', preacher),
        growth_data_six('ora', 'Ora', preacher),
        growth_data_six('fitsidihana', 'Fitsidihana', preacher),
        growth_data_six('fampianarana', 'Fampianarana', preacher),
    ]

    return dict(
        grp_list=group_number(preacher),
        hour_chart=hour_chart(preacher),
        color='dark',
        growth=growth,
        growth_six=growth_six,
        not_returned=not_returned,
        preacher=preacher,
        post=post, )


def post_report(preachers):
    """
    Produce table main report table to post.
    :param preacher: list of tri sorted preacher
    :return: result object. preachers is accessible with
    'non, aux, reg, tot' properties.
    """

    p = preachers

    MONTH = str(app.config['MONTH'])

    non = {
        'isa': len(p.non),
        'zvn': sum([_['tatitra'][MONTH]['zavatra_napetraka'] for _ in p.non]),
        'vid': sum([_['tatitra'][MONTH]['video'] for _ in p.non]),
        'ora': sum([_['tatitra'][MONTH]['ora'] for _ in p.non]),
        'fit': sum([_['tatitra'][MONTH]['fitsidihana'] for _ in p.non]),
        'fam': sum([_['tatitra'][MONTH]['fampianarana'] for _ in p.non]), }

    aux = {
        'isa': len(p.aux),
        'zvn': sum([_['tatitra'][MONTH]['zavatra_napetraka'] for _ in p.aux]),
        'vid': sum([_['tatitra'][MONTH]['video'] for _ in p.aux]),
        'ora': sum([_['tatitra'][MONTH]['ora'] for _ in p.aux]),
        'fit': sum([_['tatitra'][MONTH]['fitsidihana'] for _ in p.aux]),
        'fam': sum([_['tatitra'][MONTH]['fampianarana'] for _ in p.aux]), }

    reg = {
        'isa': len(p.reg),
        'zvn': sum([_['tatitra'][MONTH]['zavatra_napetraka'] for _ in p.reg]),
        'vid': sum([_['tatitra'][MONTH]['video'] for _ in p.reg]),
        'ora': sum([_['tatitra'][MONTH]['ora'] for _ in p.reg]),
        'fit': sum([_['tatitra'][MONTH]['fitsidihana'] for _ in p.reg]),
        'fam': sum([_['tatitra'][MONTH]['fampianarana'] for _ in p.reg]), }

    tot = {
        'isa': len(p.all),
        'zvn': sum([_['tatitra'][MONTH]['zavatra_napetraka'] for _ in p.all]),
        'vid': sum([_['tatitra'][MONTH]['video'] for _ in p.all]),
        'ora': sum([_['tatitra'][MONTH]['ora'] for _ in p.all]),
        'fit': sum([_['tatitra'][MONTH]['fitsidihana'] for _ in p.all]),
        'fam': sum([_['tatitra'][MONTH]['fampianarana'] for _ in p.all]), }

    result = namedtuple('PostReport', ['non', 'aux', 'reg', 'tot'])
    return result(non, aux, reg, tot)


def hour_chart(preachers):
    service_year = get_service_year()
    ChartData = namedtuple('ChartData', ['legend', 'id', 'label', 'data'])

    label = []
    data = []

    def get_hour(pr, month):
        return pr['tatitra'][str(month)]['ora']

    for month in service_year:
        f = Filter(preachers)
        f('returned', month=str(month))

        hour = sum([get_hour(pr, month) for pr in f.preachers])

        f_aux = Filter(f.preachers)
        f_aux('is_auxiliary', month=str(month))

        aux_hour = sum([get_hour(pr, month) for pr in f_aux.preachers])

        f_reg = Filter(f.preachers)
        f_reg('is_regular')

        reg_hour = sum([get_hour(pr, month) for pr in f_reg.preachers])

        label.append(month.prettie('{short_month} {short_year}'))
        data.append((hour, reg_hour, aux_hour))

    return ChartData(
        legend=['Mpitory rehetra', 'Maharitra', 'Mpanampy'],
        id=['all', 'reg', 'aux'],
        label=label,
        data=data, )


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

    now_data = sum([get_data(pr, month) for pr in f.preachers])
    last_data_1 = sum([get_data(pr, last_month_1) for pr in last_f1.preachers])
    last_data_2 = sum([get_data(pr, last_month_2) for pr in last_f2.preachers])
    last_data_3 = sum([get_data(pr, last_month_3) for pr in last_f3.preachers])
    last_data_4 = sum([get_data(pr, last_month_4) for pr in last_f4.preachers])
    last_data_5 = sum([get_data(pr, last_month_5) for pr in last_f5.preachers])
    last_data_6 = sum([get_data(pr, last_month_6) for pr in last_f6.preachers])

    last_data = sum([
        last_data_1,
        last_data_2,
        last_data_3,
        last_data_4,
        last_data_5,
        last_data_6,
    ]) / 6

    return GrowthData(name, last_data, now_data)


def group_number(preachers):
    grp_list = []
    for preacher in preachers:
        if preacher['groupe'] not in grp_list:
            grp_list.append(preacher['groupe'])

    return sorted(grp_list)
