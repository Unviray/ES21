"""
es21.views.auxiliary
====================

Views for auxiliary pionners.
Many view here accept POST method for search in navbar or other POST.
"""

from flask import Blueprint

from . import home


blueprint = Blueprint('auxiliary', __name__, url_prefix='/mpanampy')


blueprint.add_url_rule(
    '/',
    'home',
    home.entry,
    methods=('GET', 'POST'))
