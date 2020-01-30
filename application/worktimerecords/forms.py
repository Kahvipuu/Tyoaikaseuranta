from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators

class WorktimerecordForm(FlaskForm):
    name = StringField("Worktimerecord name", [validators.Length(min=3)])
    done = BooleanField("Done")

    class Meta:
        csrf = False