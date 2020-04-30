"""
es21.views.widgets.main_board
=============================
"""

from ...utils import templated

from markupsafe import Markup


@templated('widgets/main_board.html')
def entry(content):
    content = Markup(content).unescape()

    return dict(content=content)
