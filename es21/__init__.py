"""
es21
====

Root of entire project include app factory (create_app).
"""

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from . import tfilter
from . import ctx_processor
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
    load_context_processor(app)
    load_error_handler(app)
    load_error_logger(app)

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


def load_context_processor(app):
    app.context_processor(ctx_processor.processor)
    app.context_processor(ctx_processor.color_processor)


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
