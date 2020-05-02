"""
es21.views.regular
==================

Views for regular pionners.
Many view here accept POST method for search in navbar or other POST.
"""

from flask import Blueprint

from . import home


blueprint = Blueprint('regular', __name__, url_prefix='/maharitra')


blueprint.add_url_rule(
    '/',
    'home',
    home.entry,
    methods=('GET', 'POST'))
