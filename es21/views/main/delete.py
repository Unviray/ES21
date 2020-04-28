"""
es21.views.main.delete
======================

Delete preacher.
"""

from flask import (
    request,
    redirect,
    url_for as url, )

from tinydb import Query

from ...database import get_db


def entry(id):
    db = get_db()
    q = Query()
    name = request.form.get('name', None)

    preacher = db.get(q.id == id)

    pattern = [
        f"{preacher['anarana']} {preacher['fanampinanarana']}",
        preacher['anarana'],
        preacher['fanampinanarana'], ]

    if preacher['anarana_feno'] != '':
        pattern.append(preacher['anarana_feno'])

    if name in pattern:
        db.remove(q.id == id)
        return redirect(url('home'))

    return redirect(url('main.preacher', id=id))
