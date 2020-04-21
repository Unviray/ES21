"""
es21.forms
==========

Include all form used in es21.
"""

from flask_wtf import FlaskForm
from wtforms.widgets.core import Input
from wtforms.validators import Optional
from wtforms import (
    StringField,
    IntegerField,
    SelectField, )


class IntegerInput(Input):
    """
    Render a single-line integer input.
    """

    input_type = 'number'


int_kwargs = dict(
    widget=IntegerInput(),
    validators=[Optional()],
    default=0, )


class ReportForm(FlaskForm):
    publication = IntegerField('Zavatra napetraka', **int_kwargs)
    video = IntegerField('Video', **int_kwargs)
    hour = IntegerField('Ora', **int_kwargs)
    visit = IntegerField('Fiverenana mitsidika', **int_kwargs)
    study = IntegerField('Fampianarana', **int_kwargs)

    remark = StringField('Fanamarihana')

    pionner = SelectField('Mpisavalalana', choices=[
        ('', 'Tsy mpisavalalana'),
        ('Aux', 'Mpanampy'),
        ('Reg', 'Maharitra'), ], )
