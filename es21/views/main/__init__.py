"""
es21.views.main
===============

Handle main first views.
Many view here accept POST method for search in navbar or other POST.
"""

from flask import Blueprint

from . import (
    new,
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

bp.add_url_rule(
    '/mpitory-vaovao',
    'new',
    new.entry,
    methods=('POST', 'GET'))


bp.add_url_rule(
    '/preacher/<int:id>',
    'pr_card',
    search.get_pr_card, )
