"""
es21.views.main.edit
====================

Edit/Update preacher's informations.
"""

from flask import (
    flash,
    redirect,
    url_for as url, )

from tinydb import Query

from ...forms import EditPreacherForm
from ...database import get_db
from ...utils import navbar_form, templated


@templated('pr_edit.html')
@navbar_form
def entry(id):
    db = get_db()
    q = Query()

    preacher = db.get(q.id == id)

    form = EditPreacherForm(
        last_id=preacher['id'],
        id=preacher['id'],
        last_name=preacher['anarana'],
        first_name=preacher['fanampinanarana'],
        phone1=preacher['finday'][0],
        phone2=preacher['finday'][1],
        phone3=preacher['finday'][2],
        address=preacher['adiresy'],
        gender=preacher['lahy_sa_vavy'],
        birth=preacher['teraka'],
        baptism=preacher['batisa'],
        group=preacher['groupe'],
        promo=preacher['tombotsoa'],
        permanent_pionner=preacher['maharitra'])

    if form.validate_on_submit():
        data = {
            'id': form.id.data,
            'anarana': form.last_name.data,
            'fanampinanarana': form.first_name.data,
            'finday': [
                form.phone1.data,
                form.phone2.data,
                form.phone3.data],
            'adiresy': form.address.data,
            'lahy_sa_vavy': form.gender.data,
            'teraka': form.birth.data,
            'batisa': form.baptism.data,
            'groupe': form.group.data,
            'tombotsoa': form.promo.data,
            'maharitra': form.permanent_pionner.data,
            'tatitra': preacher['tatitra'], }

        db.update(data, q.id == id)

        flash('Tontosa ny fanavaozana ny mpitory', 'success')

        return redirect(url('main.preacher', id=form.id.data))

    return dict(
        title='Fanovana',
        form=form, )
