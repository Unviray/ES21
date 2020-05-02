"""
es21.forms
==========

Include all form used in es21.
"""

import re

from flask_wtf import FlaskForm
from wtforms.widgets.core import Input
from wtforms.validators import (
    Optional,
    DataRequired,
    ValidationError, )
from wtforms import (
    DateField,
    BooleanField,
    IntegerField,
    StringField,
    SelectField, )

from tinydb import Query


class IntegerInput(Input):
    """
    Render a single-line integer input.
    """

    input_type = 'number'


class DateInput(Input):
    """
    Render a single-line date input.
    """
    input_type = 'date'


class IntField(IntegerField):
    def process_formdata(self, valuelist):
        try:
            super(IntField, self).process_formdata(valuelist)
        except ValueError:
            pass


int_kwargs = dict(
    widget=IntegerInput(),
    validators=[Optional()],
    default=0, )

date_kwargs = dict(
    widget=DateInput(),
    validators=[Optional()],
    default='', )


def eval_phone(phone_number):
    local = re.compile(r'03[0-9] [0-9]{2} [0-9]{3} [0-9]{2}')
    inter = re.compile(r'\+261 3[0-9] [0-9]{2} [0-9]{3} [0-9]{2}')

    return local.fullmatch(phone_number) or inter.fullmatch(phone_number)


class ReportForm(FlaskForm):
    publication = IntField('Zavatra napetraka', **int_kwargs)
    video = IntField('Video', **int_kwargs)
    hour = IntField('Ora', **int_kwargs)
    visit = IntField('Fiverenana mitsidika', **int_kwargs)
    study = IntField('Fampianarana', **int_kwargs)

    remark = StringField('Fanamarihana')

    pionner = SelectField('Mpisavalalana', choices=[
        ('', 'Tsy mpisavalalana'),
        ('Aux', 'Mpanampy'),
        ('Reg', 'Maharitra'), ], )

    def validate_hour(self, field):
        if field.data is None:
            raise ValidationError('Misy diso ny Ora nampidirinao')

        if field.data < 1:
            raise ValidationError("Tokony hiotran'ny 0 ny Ora")

    def validate_visit(self, field):
        if field.data < self.study.data:
            raise ValidationError(
                "Tsy mitombina ny hoe kely nohon'ny "
                "Fampianarana ny Fiverenana mitsidika")


class PreacherForm(FlaskForm):
    id = IntField('Nomerao', **int_kwargs)

    last_name = StringField('Anarana')
    first_name = StringField(
        label="Fanampin'anarana",
        validators=[DataRequired("Ilaina ity")], )

    phone1 = StringField('Laharana Finday1', validators=[Optional()])
    phone2 = StringField('Laharana Finday2', validators=[Optional()])
    phone3 = StringField('Laharana Finday3', validators=[Optional()])

    address = StringField('Adiresy')
    gender = SelectField('Lahy sa Vavy', choices=[
        ('Lahy', 'Lahy'),
        ('Vavy', 'Vavy'), ])

    birth = DateField('Teraka', **date_kwargs)
    baptism = DateField('Batisa', **date_kwargs)

    group = IntField('Groupe', **int_kwargs)
    promo = SelectField('Tombotsoa', choices=[
        ('', 'Tsy misy'),
        ('Rahalahy vita Batisa', 'Rahalahy vita Batisa'),
        ("Mpanampy amin'ny fanompoana", "Mpanampy amin'ny fanompoana"),
        ("Anti-panahy", "Anti-panahy")
    ])
    regular_pionner = BooleanField('Mpisavalalana maharitra', default=False)

    def validate_id(self, field):
        from .database import get_db
        db = get_db()
        q = Query()

        n = db.get(q.id == field.data)
        if n is not None:
            raise ValidationError('Efa misy manana io nomerao io')

    def validate_phone1(self, field):
        if eval_phone(field.data) is None:
            raise ValidationError('Hamarino ny nomerao finday')

    def validate_phone2(self, field):
        if eval_phone(field.data) is None:
            raise ValidationError('Hamarino ny nomerao finday')

    def validate_phone3(self, field):
        if eval_phone(field.data) is None:
            raise ValidationError('Hamarino ny nomerao finday')


class EditPreacherForm(PreacherForm):
    last_id = IntField('Nomerao taloha', **int_kwargs)

    def validate_id(self, field):
        if self.last_id.data != field.data:
            super(EditPreacherForm, self).validate_id(field)
