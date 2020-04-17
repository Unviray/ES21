from flask import (
    Blueprint,
    current_app as app,
    render_template as render, )

from ..broadcast import templated
from ..database import get_db


bp = Blueprint('main', __name__)


@bp.route('/')
@templated('home.html')
def home():
    db = get_db()

    if len(db.all()) == 0:
        return render('welcome.html')

    return dict(
        app=app, )


@bp.route('/fitadiavana')
@templated('search.html')
def search():
    db = get_db()
    return dict(
        hide_search=True,
        mpitory=db.all())
