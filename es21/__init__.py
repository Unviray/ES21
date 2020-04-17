"""
es21
====

Root of entire project include app factory (create_app).
"""

from random import randint

from flask import Flask

from . import config

from .views import (
    main,
)


def load_views(app):
    app.register_blueprint(main.bp)


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object(config.Config)
    else:
        app.config.from_mapping(test_config)

    load_views(app)

    @app.context_processor
    def processor():
        return dict(
            len=len,
            round=round,
            rand10=lambda: randint(0, 100) < 10,
            app=app,
        )

    return app
