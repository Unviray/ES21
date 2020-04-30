"""
es21.views.widgets.hour_chart
=============================
"""

from flask import jsonify

from ...utils import templated


@templated('widgets/hour_chart.html')
def entry(data):
    legend = 'Ora'

    chart_data = {
        'labels': [_[0] for _ in data],
        'datasets': [{
            'label': legend,
            'fill': True,
            'lineTension': 0.2,
            'backgroundColor': "rgba(75,192,192,0.4)",
            'borderColor': "rgba(75,192,192,1)",
            'borderCapStyle': 'butt',
            'borderDash': [],
            'borderDashOffset': 0.0,
            'borderJoinStyle': 'miter',
            'pointBorderColor': "rgba(75,192,192,1)",
            'pointBackgroundColor': "#fff",
            'pointBorderWidth': 1,
            'pointHoverRadius': 5,
            'pointHoverBackgroundColor': "rgba(75,192,192,1)",
            'pointHoverBorderColor': "rgba(220,220,220,1)",
            'pointHoverBorderWidth': 2,
            'pointRadius': 1,
            'pointHitRadius': 10,
            'data': [_[1] for _ in data],
            'spanGaps': False, }], }

    return dict(chart_data=jsonify(chart_data))
