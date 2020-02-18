from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False


class SignInForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=3, max=20, message="length between 3-20")])
    password = PasswordField("Password", [validators.Length(min=5, message="length min 5")])
    password_confirmation = PasswordField("Password confirmation", [validators.equal_to("password", message="doesn't match password")])

    class Meta:
        csrf = False
