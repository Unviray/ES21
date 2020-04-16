from flask import (
    Blueprint,
    current_app as app, )

from ..broadcast import templated


bp = Blueprint('main', __name__)


@bp.route('/')
@templated('home.html')
def home():
    return dict(
        app=app, )
