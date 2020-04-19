"""
es21.views.main.home
====================

Home entry page.
"""

from flask import (
    current_app as app,
    render_template as render, )

from ...broadcast import templated, navbar_form
from ...database import get_db


@templated('home.html')
@navbar_form
def entry():
    db = get_db()

    preacher = db.all()

    if len(preacher) == 0:
        # empty database
        return render('welcome.html')

    return dict(
        preacher=preacher,
        app=app, )
