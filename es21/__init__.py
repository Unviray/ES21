"""
es21
====

Root of entire project include app factory (create_app).
"""

from random import randint

from flask import (
    Flask,
    url_for as url, )

from . import (
    config,
    database, )

from .views import (
    main, )


def load_views(app):
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='home')


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object(config.Config)
    else:
        app.config.from_mapping(test_config)

    database.init_app(app)

    load_views(app)

    @app.context_processor
    def processor():
        return dict(
            len=len,
            round=round,
            rand10=lambda: randint(0, 100) < 100,
            url=url,
            app=app,
        )

    return app
