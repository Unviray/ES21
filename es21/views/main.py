from flask import (
    Blueprint,
    current_app as app, )

from ..broadcast import templated
from ..database import get_db


bp = Blueprint('main', __name__)


@bp.route('/')
@templated('home.html')
def home():
    db = get_db()
    return dict(
        db=db,
        app=app, )
