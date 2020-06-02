"""
es21.views.main.new
====================

Creating new preacher.
"""

from flask import (
    flash,
    request,
    redirect,
    url_for as url, )

from tinydb import Query

from ...utils import templated, navbar_form
from ...database import get_db
from ...forms import PreacherForm


@templated('pr_edit.html')
@navbar_form
def entry():
    new_preacher_handler = NewPreacherHandler()
    pushed = new_preacher_handler.push()

    if pushed:
        id = new_preacher_handler.form.id.data

        flash("Tafiditra soaman'tsara ny mpitory", 'success')

        return redirect(url('main.preacher', id=id))

    return dict(
        title='Mpitory vaovao',
        form=new_preacher_handler.form,
        hide_search=request.args.get('hide_search', False), )


class NewPreacherHandler(object):
    def __init__(self):
        self.db = get_db()
        q = Query()

        no_id = 100
        while self.db.get(q.id == no_id) is not None:
            no_id += 1

        self.form = PreacherForm(id=no_id)

    def push(self):
        if not self.form.validate_on_submit():
            return False

        data = {
            'id': self.form.id.data,
            'anarana': self.form.last_name.data,
            'fanampinanarana': self.form.first_name.data,
            'finday': [self.form.phone1.data,
                       self.form.phone2.data,
                       self.form.phone3.data, ],
            'adiresy': self.form.address.data,
            'lahy_sa_vavy': self.form.gender.data,
            'teraka': self.form.birth.data,
            'batisa': self.form.baptism.data,
            'groupe': self.form.group.data,
            'tombotsoa': self.form.promo.data,
            'maharitra': self.form.regular_pionner.data,
            'tatitra': {}, }

        self.db.insert(data)

        return True
