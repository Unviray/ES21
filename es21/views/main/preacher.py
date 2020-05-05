"""
es21.views.main.preacher
========================

Show stat and report of preacher.
"""

from collections import OrderedDict, namedtuple

from flask import (
    flash,
    redirect,
    url_for as url,
    current_app as app, )

from werkzeug.exceptions import abort
from tinydb import Query

from ...utils import templated, navbar_form, get_service_year
from ...database import get_db
from ...forms import ReportForm

from ...filters import Filter, returned, is_auxiliary


q = Query()


@templated('preacher.html')
@navbar_form
def entry(id):
    MONTH = str(app.config['MONTH'])
    db = get_db()
    preacher = db.get(q.id == id)

    if preacher is None:
        abort(404)

    report = sort_month(preacher['tatitra'])

    has_report = returned(MONTH)(preacher)

    report_handler = ReportHandler(ReportForm, preacher, has_report)
    pushed = report_handler.push()

    if pushed:
        flash("Tafiditra soaman'tsara ny tatitra", 'success')
        return redirect(url('main.preacher', id=id))

    months = auxiliary_check(id)

    # growth widget
    growth = [
        growth_data('zavatra_napetraka', 'Zavatra napetraka', [preacher]),
        growth_data('video', 'Video', [preacher]),
        growth_data('ora', 'Ora', [preacher]),
        growth_data('fitsidihana', 'Fitsidihana', [preacher]),
        growth_data('fampianarana', 'Fampianarana', [preacher]),
    ]
    growth_six = [
        growth_data_six('zavatra_napetraka', 'Zavatra napetraka', [preacher]),
        growth_data_six('video', 'Video', [preacher]),
        growth_data_six('ora', 'Ora', [preacher]),
        growth_data_six('fitsidihana', 'Fitsidihana', [preacher]),
        growth_data_six('fampianarana', 'Fampianarana', [preacher]),
    ]

    return dict(
        pr=preacher,
        report=report,
        months=months,
        growth=growth,
        growth_six=growth_six,
        has_report=has_report,
        is_auxiliary=is_auxiliary()(preacher),
        form=report_handler.form, )


def sort_month(report, revers=True):
    month_id = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12,
    }

    # sort month
    keys = sorted(report, key=lambda x: month_id[x.split('_')[0]])

    result_month = OrderedDict()
    for key in keys:
        result_month[key] = report[key]

    # sort year
    keys = sorted(result_month, key=lambda x: int(x.split('_')[1]))

    result_year = OrderedDict()
    for key in keys:
        result_year[key] = result_month[key]

    if revers:
        result_rev = OrderedDict()
        for key in reversed(result_year):
            result_rev[key] = result_year[key]

        return result_rev

    else:
        return result_year


class ReportHandler(object):
    """
    Handler for report that create new report or update existing report.
    """

    def __init__(self, form_class, preacher, has_report):
        MONTH = str(app.config['MONTH'])

        self.form_class = form_class
        self.preacher = preacher
        self.has_report = has_report

        if self.has_report:
            self.report = preacher['tatitra'][MONTH]

        self.init_report()

    def init_pionner(self):
        MONTH = str(app.config['MONTH'])

        if self.has_report:
            return False

        mdb = get_db('mpanampy')

        if self.preacher.get('maharitra', False):
            return 'Reg'

        elif self.preacher['id'] in mdb.get(q.volana == MONTH)['mpitory']:
            return 'Aux'

        else:
            return False

    def init_report(self):
        if not self.has_report:
            pionner = self.init_pionner()
            if pionner:
                self.form = self.form_class(pionner=pionner)
            else:
                self.form = self.form_class()

        else:
            self.form = self.form_class(
                publication=self.report['zavatra_napetraka'],
                video=self.report['video'],
                hour=self.report['ora'],
                visit=self.report['fitsidihana'],
                study=self.report['fampianarana'],
                remark=self.report['fanamarihana'],
                pionner=self.report['mpisavalalana'],
            )

    def push(self):
        MONTH = str(app.config['MONTH'])
        db = get_db()

        if self.form.validate_on_submit():
            data = {
                'zavatra_napetraka': self.form.publication.data,
                'video': self.form.video.data,
                'ora': self.form.hour.data,
                'fitsidihana': self.form.visit.data,
                'fampianarana': self.form.study.data,
                'fanamarihana': self.form.remark.data,
                'mpisavalalana': self.form.pionner.data, }

            def add_month(volana, data):
                def transform(doc):
                    doc['tatitra'][MONTH] = data

                return transform

            db.update(add_month(MONTH, data), q.id == self.preacher['id'])
            return True

        else:
            return False


def auxiliary_check(id):
    """
    Build checkable month for auxiliary.
    """

    mdb = get_db('mpanampy')
    service_year = get_service_year()

    MonthObj = namedtuple('MonthObj', ['active', 'id', 'checked', 'name'])

    months = []
    for service_month in service_year:
        month = mdb.get(q.volana == str(service_month))

        if month is None:
            months.append(MonthObj(
                active='',
                id=str(service_month),
                checked='',
                name=service_month.prettie(), ))

        elif month.get('mpitory') is None:
            months.append(MonthObj(
                active='',
                id=str(service_month),
                checked='',
                name=service_month.prettie(), ))

        elif id in month.get('mpitory'):  # Only active
            months.append(MonthObj(
                active='active',
                id=str(service_month),
                checked='checked',
                name=service_month.prettie(), ))

        else:
            months.append(MonthObj(
                active='',
                id=str(service_month),
                checked='',
                name=service_month.prettie(), ))

    return months


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
    last_month_1 = str(MONTH.new_me() - 1)
    last_month_2 = str(MONTH.new_me() - 2)
    last_month_3 = str(MONTH.new_me() - 3)
    last_month_4 = str(MONTH.new_me() - 4)
    last_month_5 = str(MONTH.new_me() - 5)
    last_month_6 = str(MONTH.new_me() - 6)

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
