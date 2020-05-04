"""
es21.views.group
================

Views for groups of pionners.
Many view here accept POST method for search in navbar or other POST.
"""

from flask import Blueprint

from . import home


blueprint = Blueprint('group', __name__, url_prefix='/andiam-pitory/<int:gid>')


blueprint.add_url_rule(
    '/',
    'home',
    home.entry,
    methods=('GET', 'POST'))
