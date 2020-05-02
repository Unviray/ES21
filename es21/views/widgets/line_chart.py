"""
es21.views.widgets.line_chart
=============================

Display line chart.
"""

from flask import jsonify

from ...utils import templated
from ...const import color_chart


@templated('widgets/line_chart.html')
def entry(data):
    """
    :param data: namedTuple who has these properties:
    - label: List[str]
    - legend: List[str]
    - data: List[Tuple[int, ...]:len(legend)]
    """

    length = len(data.legend)

    datasets = []
    for i in range(0, length):
        datasets.append({
            'label': data.legend[i],
            **default_line,
            'borderColor': color(data.id[i], 1),
            'pointBorderColor': color(data.id[i], 1),
            'pointHoverBackgroundColor': color(data.id[i], 1),
            'pointHoverBorderColor': "rgba(220,220,220,1)",
            'data': [_[i] for _ in data.data], })

    chart_data = {
        'labels': data.label,
        'datasets': datasets, }

    return dict(chart_data=jsonify(chart_data))


default_line = {
    'fill': False,
    'borderCapStyle': 'butt',
    'cubicInterpolationMode': 'monotone',
    'borderDash': [],
    'borderDashOffset': 0.0,
    'borderJoinStyle': 'miter',
    'pointBackgroundColor': "#fff",
    'pointBorderWidth': 1,
    'pointHoverRadius': 5,
    'pointHoverBorderWidth': 2,
    'pointRadius': 1,
    'pointHitRadius': 10,
    'spanGaps': False, }


def color(index, alpha):
    r = color_chart[index][0]
    g = color_chart[index][1]
    b = color_chart[index][2]

    return f'rgba({r},{g},{b},{alpha})'
