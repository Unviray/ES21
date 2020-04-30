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


blueprint = Blueprint('main', __name__)


blueprint.add_url_rule(
    '/',
    'home',
    home.entry,
    methods=('GET', 'POST'))

blueprint.add_url_rule(
    '/fitadiavana',
    'search',
    search.entry,
    methods=('GET', 'POST'))

blueprint.add_url_rule(
    '/mpitory/<int:id>/',
    'preacher',
    preacher.entry,
    methods=('GET', 'POST'))

blueprint.add_url_rule(
    '/mpitory-vaovao',
    'new',
    new.entry,
    methods=('GET', 'POST'))

blueprint.add_url_rule(
    '/mpitory/<int:id>/hanavao',
    'edit',
    edit.entry,
    methods=('GET', 'POST'))

blueprint.add_url_rule(
    '/mpitory/<int:id>/hamafa',
    'delete',
    delete.entry,
    methods=['POST'])
