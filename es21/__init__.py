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
        from .views.main.search import get_pr_card

        return dict(
            len=len,
            round=round,
            url=url,
            app=app,
            pr_card=get_pr_card, )

    @app.context_processor
    def color_processor():
        def color_returned(preacher):
            try:
                hour = preacher['tatitra'][str(app.config['MONTH'])]['ora']
            except KeyError:
                return 'danger'
            else:
                return 'danger' if hour == 0 else 'primary'

        return dict(
            color_returned=color_returned, )

    return app


def load_views(app):
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='home')


def load_template_filter(app):
    app.add_template_filter(tfilter.month_name)
    app.add_template_filter(tfilter.pionner_name)
    app.add_template_filter(tfilter.date)
