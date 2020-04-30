"""
es21.views.widgets.main_board
=============================
"""

from ...utils import templated


@templated('widgets/main_board.html')
def entry(content):
    return dict(content=content)
