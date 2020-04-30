"""
es21.views.widgets
==================

All widgets goes here.
"""

from flask import Blueprint

from . import pr_card


blueprint = Blueprint('widget', __name__, url_prefix='/widget')


blueprint.add_url_rule(
    '/pr_card',
    'pr_card',
    pr_card.entry, )
