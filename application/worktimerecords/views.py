from flask import redirect, render_template, request, url_for
from flask_login import login_required

from application import app, db
from application.worktimerecords.models import Worktimerecord
from application.worktimerecords.forms import WorktimerecordForm

@app.route("/worktimerecords", methods=["GET"])
def worktimerecords_index():
    return render_template("worktimerecords/list.html", worktimerecords = Worktimerecord.query.all())

@app.route("/worktimerecords/new/")
@login_required
def worktimerecords_form():
    return render_template("worktimerecords/new.html", form = WorktimerecordForm())

@app.route("/worktimerecords/<worktimerecord_id>/", methods=["POST"])
@login_required
def worktimerecords_set_done(worktimerecord_id):

    t = Worktimerecord.query.get(worktimerecord_id)
    t.done = True
    db.session().commit()
  
    return redirect(url_for("worktimerecords_index"))

@app.route("/worktimerecords/", methods=["POST"])
@login_required
def worktimerecords_create():
    form = WorktimerecordForm(request.form)

    if not form.validate():
        return render_template("worktimerecords/new.html", form = form)

    t = Worktimerecord(form.name.data)
    t.done = form.done.data

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("worktimerecords_index"))