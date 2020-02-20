from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators, IntegerField, DateField, SelectField

class WorktimerecordForm(FlaskForm):
    name = StringField("Type of work done", [validators.Length(min=3)])
    done = BooleanField("Done")
    hours = IntegerField("Hours", [validators.number_range(min=0, max=24, message="Hours 0-24")])
    dateofwork = DateField("Date(YYYY-MM-DD)", [validators.input_required(message="YYYY-MM-DD")])
    project = SelectField("Project Name", coerce=int)
# choices=[('1', 'eka'),('2','toka')]

    class Meta:
        csrf = False