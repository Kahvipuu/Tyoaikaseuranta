from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators, IntegerField, DateField, SelectField
from datetime import date

class WorktimerecordForm(FlaskForm):
    name = StringField("Type of work done", [validators.Length(min=3, max=30, message="3-30 characters")])
    done = BooleanField("Done")
    hours = IntegerField("Hours", [validators.number_range(min=1, max=24, message="Hours 1-24")])
    dateofwork = DateField("Date(YYYY-MM-DD)", [validators.input_required(message="YYYY-MM-DD")], default=date.today())
    project = SelectField("Project Name", coerce=int, validators = None )

    class Meta:
        csrf = False