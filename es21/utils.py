"""
es21.uils
=========

Utilities for many view.
"""

from functools import wraps

from flask import (
    request,
    redirect,
    url_for as url,
    current_app as app,
    render_template as render, )


def templated(template=None):
    """
    https://flask.palletsprojects.com/patterns/viewdecorators.html#templating-decorator

    Decorate view with this insted of returning render_template obj
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render(template_name, **ctx)
        return decorated_function
    return decorator


def navbar_form(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            try:  # Search form
                value = request.form['search']
                return redirect(url('main.search', value=value))
            except KeyError:
                pass

            try:  # Month form
                if request.form['month']:
                    y = request.form['month'].split('-')[0]
                    m = request.form['month'].split('-')[1]

                    app.config['MONTH'].__init__(f'{m}_{y}')
            except KeyError:
                pass

        return f(*args, **kwargs)
    return decorated_function


def get_service_year(month=None):
    """
    Build service year from month.
    """

    MONTH = month or app.config['MONTH']
    year = MONTH.year

    if MONTH.month in (9, 10, 11, 12):
        return [
            MONTH.new_me(f'sep_{year}'),
            MONTH.new_me(f'oct_{year}'),
            MONTH.new_me(f'nov_{year}'),
            MONTH.new_me(f'dec_{year}'),
            MONTH.new_me(f'jan_{year + 1}'),
            MONTH.new_me(f'feb_{year + 1}'),
            MONTH.new_me(f'mar_{year + 1}'),
            MONTH.new_me(f'apr_{year + 1}'),
            MONTH.new_me(f'may_{year + 1}'),
            MONTH.new_me(f'jun_{year + 1}'),
            MONTH.new_me(f'jul_{year + 1}'),
            MONTH.new_me(f'aug_{year + 1}'), ]

    else:
        return [
            MONTH.new_me(f'sep_{year - 1}'),
            MONTH.new_me(f'oct_{year - 1}'),
            MONTH.new_me(f'nov_{year - 1}'),
            MONTH.new_me(f'dec_{year - 1}'),
            MONTH.new_me(f'jan_{year}'),
            MONTH.new_me(f'feb_{year}'),
            MONTH.new_me(f'mar_{year}'),
            MONTH.new_me(f'apr_{year}'),
            MONTH.new_me(f'may_{year}'),
            MONTH.new_me(f'jun_{year}'),
            MONTH.new_me(f'jul_{year}'),
            MONTH.new_me(f'aug_{year}'), ]
