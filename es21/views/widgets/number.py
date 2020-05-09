"""
es21.views.widgets.number
=========================
"""

from ...utils import templated
from ...sorters import sort_hour


@templated('widgets/number.html')
def entry(preachers):
    hour_sorted = sort_hour(preachers)

    lt5 = hour_sorted.less_than_5
    b59 = hour_sorted.between_5_9
    m10 = hour_sorted.more_than_10

    less5 = (len(lt5), percenter(len(lt5), len(preachers)))
    btw59 = (len(b59), percenter(len(b59), len(preachers)))
    mor10 = (len(m10), percenter(len(m10), len(preachers)))

    return {
        'less5': less5,
        'btw59': btw59,
        'mor10': mor10,
    }


def percenter(n, total):
    if total == 0:
        return 0
    return (100 * n) / total
