from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db, login_required
from application.auth.models import User
from application.auth.forms import LoginForm, SignInForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "Username/Password wrong! (testuser = user/pass)")

    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/sign_in", methods = ["GET", "POST"])
def auth_sign_in():
    if request.method == "GET":
        return render_template("auth/signinform.html", form = SignInForm())

    form = SignInForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()
    if user:
        return render_template("auth/signinform.html", form = form,
                                error = "Username already taken")

    if not form.validate():
        return render_template("auth/signinform.html", form = form)

    new_user = User(form.username.data)
    new_user.username = form.username.data
    new_user.password = form.password.data

    db.session().add(new_user)
    db.session().commit()

    login_user(new_user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))
    