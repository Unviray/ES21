"""
es21
====

Root of entire project include app factory (create_app).
"""

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

    return app
