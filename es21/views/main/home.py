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

    return dict(
        hour_chart=hour_chart(preacher),
        growth=[growth_hour(preacher)],
        not_returned=not_returned,
        preacher=preacher,
        post=post, )


def get_hour(pr, month):
    return pr['tatitra'][str(month)]['ora']


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
    ChartData = namedtuple('ChartData', ['legend', 'label', 'data'])

    label = []
    data = []

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
        label=label,
        data=data, )


def growth_hour(preachers):
    GrowthData = namedtuple('GrowthData', ['desc', 'last', 'now'])

    MONTH = app.config['MONTH']

    month = str(MONTH)
    last_month = MONTH.new_me() - 1

    f = Filter(preachers)
    f('returned', month=str(month))
    last_f = Filter(preachers)
    last_f('returned', month=str(last_month))

    hour = sum([get_hour(pr, month) for pr in f.preachers])
    last_hour = sum([get_hour(pr, last_month) for pr in last_f.preachers])

    return GrowthData("Ora", last_hour, hour)
