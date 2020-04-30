"""
es21
====

Root of entire project include app factory (create_app).
"""

import logging
from logging.handlers import RotatingFileHandler

from werkzeug.utils import import_string
from flask import (
    Flask,
    url_for as url, )

from . import tfilter
from . import config, database

from .views import (
    main,
    auxiliary,
    error,
    widgets, )


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object(config.Config)
    else:
        app.config.from_mapping(test_config)

    database.init_app(app)

    load_views(app)
    load_template_filter(app)
    load_error_handler(app)
    load_error_logger(app)

    @app.context_processor
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

    @app.context_processor
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

    return app


def load_views(app):
    app.register_blueprint(main.blueprint)
    app.add_url_rule('/', endpoint='home')

    app.register_blueprint(auxiliary.blueprint)
    app.register_blueprint(widgets.blueprint)


def load_template_filter(app):
    app.add_template_filter(tfilter.month_name)
    app.add_template_filter(tfilter.pionner_name)
    app.add_template_filter(tfilter.date)


def load_error_handler(app):
    app.register_error_handler(404, error.page_not_found)
    app.register_error_handler(500, error.server_error)


def load_error_logger(app):
    file_handler = RotatingFileHandler(app.config['LOG'])
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))

    if not app.debug:
        app.logger.addHandler(file_handler)
