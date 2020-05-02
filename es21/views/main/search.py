"""
es21.views.main.search
======================

Fetch and search through list of preacher.
"""

import re

from flask import (
    request,
    redirect,
    url_for as url, )

from markupsafe import Markup

from tinydb import Query

from ...utils import templated, navbar_form
from ...const import filter_name, reverse_filter_name
from ...database import get_db
from ...filters import Filter


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
    query_filters = request.args.get('filter', '').split(' ')

    value = Markup(value).unescape()  # can use regexp

    search_args = dict(regex=value, flags=re.IGNORECASE)

    result = db.search(
        (q.anarana.search(**search_args)) |
        (q.fanampinanarana.search(**search_args)) |
        (q.anarana_feno.search(**search_args)) |

        (q.id == integer(value)) |
        (q.groupe == integer(value)) |
        (q.finday.test(lambda s: value in s)))

    ft = Filter(result)

    for qf in query_filters:
        ft(qf)

    if len(ft.preachers) == 1:
        return redirect(url('main.preacher', id=ft.preachers[0]['id']))

    all_ft = [filter_name[_] for _ in list(ft.filters)]
    on_ft = [filter_name[_] for _ in ft.filtered_by]

    def is_active(ft):
        """
        helper function for color.
        """

        return '' if ft in on_ft else '-outline'

    def add_f(f_to_add):
        f_to_add = reverse_filter_name[f_to_add]
        f = ' '.join(ft.filtered_by + [f_to_add])

        return url('main.search', value=value, filter=f)

    def remove_f(f_to_remove):
        on_ft.remove(f_to_remove)
        f = ' '.join([reverse_filter_name[_] for _ in on_ft])
        on_ft.append(f_to_remove)

        return url('main.search', value=value, filter=f)

    return dict(
        value=value,

        on_ft=on_ft,
        all_ft=all_ft,

        add_f=add_f,
        remove_f=remove_f,

        hide_search=True,
        is_active=is_active,
        preacher=ft.preachers, )
