from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.worktimerecords.models import Worktimerecord
from application.worktimerecords.forms import WorktimerecordForm
from application.projects.models import Project
from application.auth.models import User

@app.route("/worktimerecords", methods=["GET"])
def worktimerecords_index():
    return render_template("worktimerecords/list.html", worktimerecords = Worktimerecord.query.all(), users_record = User.find_users_records(), users = User.query.all())

@app.route("/worktimerecords/new/")
@login_required
def worktimerecords_form():
    return render_template("worktimerecords/new.html", form = WorktimerecordForm())

@app.route("/worktimerecords/remove/<worktimerecord_id>/", methods=["POST"])
@login_required
def worktimerecords_remove(worktimerecord_id):

    wtr = Worktimerecord.query.get(worktimerecord_id)

    if wtr.account_id == current_user.id:
        db.session().delete(wtr)
        db.session().commit()
  
    return redirect(url_for("worktimerecords_index"))

@app.route("/worktimerecords/", methods=["GET", "POST"])
@login_required
def worktimerecords_create():

    project_list = Project.query.all()

    project_choices = [ (i.id, i.name) for i in project_list ]

    form = WorktimerecordForm(request.form)
    form.project.choices = project_choices
    # vaihtoehdot ei mene formiin asti
    # [('1', 'eka'),('2','toka')]

    if not form.validate():
        return render_template("worktimerecords/new.html", form = form)

    wtr = Worktimerecord(form.name.data)
    wtr.hours = form.hours.data
    wtr.dateofwork = form.dateofwork.data
    wtr.account_id = current_user.id

    # miten?? Jotenkin pitäisi projekti ja kirjaus liittää toisiinsa
    proj = Project.query.get(form.project.data)
    wtr.project_name = proj.name
    wtr.project_id = proj.id

    db.session().add(wtr)
    db.session().commit()

    return redirect(url_for("worktimerecords_index"))