"""
es21.views.main.preacher
========================

Show stat and report of preacher.
"""

from collections import OrderedDict

from flask import current_app as app
from werkzeug.exceptions import abort
from tinydb import Query

from ...utils import templated, navbar_form
from ...database import get_db

from ...filters import returned


@templated('preacher.html')
@navbar_form
def entry(id):
    db = get_db()
    q = Query()

    result = db.get(q.id == id)

    if result is None:
        abort(404)

    report = sort_month(result['tatitra'])

    has_report = returned(str(app.config['MONTH']))(result)

    return dict(
        pr=result,
        report=report,
        has_report=has_report, )


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
