"""
es21.views.main
===============

Handle main first views.
Many view here accept POST method for search in navbar or other POST.
"""

import re

from flask import (
    request,
    Blueprint,
    current_app as app,
    render_template as render, )

from tinydb import Query
from markupsafe import Markup

from ..broadcast import templated, navbar_form
from ..database import get_db


bp = Blueprint('main', __name__)


@bp.route('/', methods=('GET', 'POST'))
@templated('home.html')
@navbar_form
def home():
    db = get_db()

    if len(db.all()) == 0:
        return render('welcome.html')

    return dict(
        app=app, )


@bp.route('/fitadiavana', methods=('GET', 'POST'))
@templated('search.html')
@navbar_form
def search():
    db = get_db()
    q = Query()
    value = request.args.get('value', '')

    value = Markup(value).unescape()  # can use regexp

    def integer(n):
        """
        Cast {n} to an integer but avoid error
        """

        try:
            return int(n)
        except ValueError:
            return None

    search_args = dict(regex=value, flags=re.IGNORECASE)

    result = db.search(
        (q.anarana.search(**search_args)) |
        (q.fanampinanarana.search(**search_args)) |
        (q.anarana_feno.search(**search_args)) |

        (q.id == integer(value)) |
        (q.groupe == integer(value)) |
        (q.finday.test(lambda s: value in s)))

    return dict(
        hide_search=True,
        preacher=result, )
