"""
es21.views.widgets
==================

All widgets goes here.
"""

from flask import Blueprint

from . import (
    pr_card,
    pr_card_uncached,
    main_board,
    line_chart,
    growth, )


blueprint = Blueprint('widget', __name__, url_prefix='/widget')


blueprint.add_url_rule(
    '/pr_card/<int:id>',
    'pr_card',
    pr_card.entry, )
blueprint.add_url_rule(
    '/pr_card_uncached/<int:id>',
    'pr_card_uncached',
    pr_card_uncached.entry, )

blueprint.add_url_rule(
    '/main_board',
    'main_board',
    main_board.entry, )

blueprint.add_url_rule(
    '/line_chart',
    'line_chart',
    line_chart.entry, )

blueprint.add_url_rule(
    '/growth',
    'growth',
    growth.entry, )
