"""
es21.views.main.search
======================

Fetch and search through list of preacher.
"""

import re

from flask import request

from markupsafe import Markup

from tinydb import Query

from ...utils import templated, navbar_form
from ...database import get_db


def integer(n):
    """
    Cast {n} to an integer but avoid error
    """

    try:
        return int(n)
    except ValueError:
        return None


@templated('search.html')
@navbar_form
def entry():
    db = get_db()
    q = Query()
    value = request.args.get('value', '')

    value = Markup(value).unescape()  # can use regexp

    search_args = dict(regex=value, flags=re.IGNORECASE)

    result = db.search(
        (q.anarana.search(**search_args)) |
        (q.fanampinanarana.search(**search_args)) |
        (q.anarana_feno.search(**search_args)) |

        (q.id == integer(value)) |
        (q.groupe == integer(value)) |
        (q.finday.test(lambda s: value in s)))

    return dict(
        value=value,
        hide_search=True,
        preacher=result, )
