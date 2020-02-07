from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators, IntegerField, DateField

class WorktimerecordForm(FlaskForm):
    name = StringField("Type of work done", [validators.Length(min=3)])
    done = BooleanField("Done")
    hours = IntegerField("Hours")
    dateofwork = DateField("Date(YYYY-MM-DD)")
    project = StringField("Project Name")

    class Meta:
        csrf = False