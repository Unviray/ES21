from werkzeug.utils import import_string

from flask import (
    url_for as url,
    current_app as app, )


def processor():
    def get_widget(name, *args, **kwargs):
        module_widget = import_string(f'es21.views.widgets.{name}:entry')

        return module_widget(*args, **kwargs)

    return dict(
        len=len,
        str=str,
        round=round,
        url=url,
        app=app,
        widget=get_widget,
        MONTH=app.config['MONTH'], )


def color_processor():
    def color_returned(preacher):
        try:
            hour = preacher['tatitra'][str(app.config['MONTH'])]['ora']
        except KeyError:
            return 'danger'
        else:
            return 'danger' if hour == 0 else 'primary'

    def color_contrast(c):
        return {
            'dark': 'white',
            'danger': 'white',
            'primary': 'white',
            'secondary': 'white',
            'light': 'dark',
            'success': 'white',
            'info': 'dark',
            'warning': 'dark',
        }.get(c, 'dark')

    return dict(
        color_returned=color_returned,
        color_contrast=color_contrast, )
