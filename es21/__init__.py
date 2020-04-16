from flask import Flask

from .views import (
    main,
)


def load_views(app):
    app.register_blueprint(main.bp)


def create_app(test_config=None):
    app = Flask(__name__)

    load_views(app)

    return app
