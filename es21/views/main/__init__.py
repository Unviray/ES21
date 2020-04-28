"""
es21.views.main
===============

Handle main first views.
Many view here accept POST method for search in navbar or other POST.
"""

from flask import Blueprint

from . import (
    new,
    edit,
    home,
    delete,
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
    methods=('GET', 'POST'))

bp.add_url_rule(
    '/mpitory-vaovao',
    'new',
    new.entry,
    methods=('GET', 'POST'))

bp.add_url_rule(
    '/mpitory/<int:id>/hanavao',
    'edit',
    edit.entry,
    methods=('GET', 'POST'))

bp.add_url_rule(
    '/mpitory/<int:id>/hamafa',
    'delete',
    delete.entry,
    methods=['POST'])


bp.add_url_rule(
    '/preacher/<int:id>',
    'pr_card',
    search.get_pr_card, )
