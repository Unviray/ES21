"""
es21.views.widgets.growth
=========================
"""

from math import inf
from collections import namedtuple

from ...utils import templated


@templated('widgets/growth.html')
def entry(title, data):

    GData = namedtuple('GData', ['desc', 'is_increasing', 'value'])

    new_data = []
    for d in data:
        percent = 0
        if (d.last == 0) or (d.now == 0):
            percent = inf
        else:
            if (d.now >= d.last):
                percent = 100 - ((d.last / d.now) * 100)
            else:
                percent = 100 - ((d.now / d.last) * 100)

        new_data.append(GData(
            desc=d.desc,
            is_increasing=(d.now >= d.last),
            value=percent
        ))
    return dict(
        title=title,
        data=new_data,
    )
