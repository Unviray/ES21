"""
es21.broadcast
==============

Utilities for many view.
"""

from functools import wraps

from flask import (
    request,
    redirect,
    url_for as url,
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
            try:
                value = request.form['search']
                return redirect(url('main.search', value=value))
            except KeyError:
                pass

        return f(*args, **kwargs)
    return decorated_function
