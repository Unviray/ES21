"""
es21.views.main
===============

Handle main first views.
Many view here accept POST method for search in navbar or other POST.
"""

from flask import Blueprint

from . import (
    home,
    search,
    preacher, )


bp = Blueprint('main', __name__)


bp.add_url_rule(
    '/',
    'home',
    home.entry,
    methods=('GET', 'POST'))

bp.add_url_rule(
    '/fitadiavana',
    'search',
    search.entry,
    methods=('GET', 'POST'))

bp.add_url_rule(
    '/mpitory/<int:id>/',
    'preacher',
    preacher.entry,
    methods=('POST', 'GET'))
