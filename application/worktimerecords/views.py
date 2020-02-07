from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.worktimerecords.models import Worktimerecord
from application.worktimerecords.forms import WorktimerecordForm
from application.projects.models import Project
from application.auth.models import User

@app.route("/worktimerecords", methods=["GET"])
def worktimerecords_index():
    return render_template("worktimerecords/list.html", worktimerecords = Worktimerecord.query.all(), users_record = User.find_users_records())

@app.route("/worktimerecords/new/")
@login_required
def worktimerecords_form():
    return render_template("worktimerecords/new.html", form = WorktimerecordForm())

# oikeasti kirjauksen poisto, muutetaan nimi aikanaan
@app.route("/worktimerecords/<worktimerecord_id>/", methods=["POST"])
@login_required
def worktimerecords_set_done(worktimerecord_id):

    wtr = Worktimerecord.query.get(worktimerecord_id)

    db.session().delete(wtr)
    db.session().commit()
  
    return redirect(url_for("worktimerecords_index"))

@app.route("/worktimerecords/", methods=["POST"])
@login_required
def worktimerecords_create():
    form = WorktimerecordForm(request.form)

    if not form.validate():
        return render_template("worktimerecords/new.html", form = form)

    wtr = Worktimerecord(form.name.data)
    wtr.hours = form.hours.data
    wtr.dateofwork = form.dateofwork.data
    wtr.account_id = current_user.id

    # miten?? Jotenkin pitäisi projekti ja kirjaus liittää toisiinsa
    proj = Project(form.project.data)

    db.session().add(wtr)
    db.session().add(proj)
    db.session().commit()

    return redirect(url_for("worktimerecords_index"))