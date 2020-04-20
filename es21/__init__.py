"""
es21
====

Root of entire project include app factory (create_app).
"""

from flask import (
    Flask,
    url_for as url, )

from . import tfilter
from . import config, database

from .views import main


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object(config.Config)
    else:
        app.config.from_mapping(test_config)

    database.init_app(app)

    load_views(app)
    load_template_filter(app)

    @app.context_processor
    def processor():
        return dict(
            len=len,
            round=round,
            url=url,
            app=app,
        )

    return app


def load_views(app):
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='home')


def load_template_filter(app):
    app.add_template_filter(tfilter.month_name)
