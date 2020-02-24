from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators

class ProjectForm(FlaskForm):
    name = StringField("Project name", [validators.Length(min=3, max=50, message="3-50 characters")])
    active = BooleanField("active")
    projectleader = StringField("Project leader")

    class Meta:
        csrf = False