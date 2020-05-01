"""
es21.views.widgets.line_chart
=============================
"""

from flask import jsonify

from ...utils import templated


@templated('widgets/line_chart.html')
def entry(data):
    length = len(data.legend)

    datasets = []
    for i in range(0, length):
        datasets.append({
            'label': data.legend[i],
            **default_line,
            'borderColor': color(i, 1),
            'pointBorderColor': color(i, 1),
            'pointHoverBackgroundColor': color(i, 1),
            'pointHoverBorderColor': "rgba(220,220,220,1)",
            'data': [_[i] for _ in data.data], })

    chart_data = {
        'labels': data.label,
        'datasets': datasets, }

    return dict(chart_data=jsonify(chart_data))


default_line = {
    'fill': False,
    'lineTension': 0.2,
    'borderCapStyle': 'butt',
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
    cl = [
        '0,0,230',
        '0,200,200',
        '0,200,0',

        '192,75,75',
        '75,192,75',
        '75,75,192',
    ]

    return f'rgba({cl[index]},{alpha})'
