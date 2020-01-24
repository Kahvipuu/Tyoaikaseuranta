from application import app, db
from flask import redirect, render_template, request, url_for
from application.worktimerecords.models import Worktimerecord

@app.route("/worktimerecords", methods=["GET"])
def worktimerecords_index():
    return render_template("worktimerecords/list.html", worktimerecords = Worktimerecord.query.all())

@app.route("/worktimerecords/new/")
def worktimerecords_form():
    return render_template("worktimerecords/new.html")

@app.route("/worktimerecords/<worktimerecord_id>/", methods=["POST"])
def worktimerecords_set_done(worktimerecord_id):

    t = Worktimerecord.query.get(worktimerecord_id)
    t.done = True
    db.session().commit()
  
    return redirect(url_for("worktimerecords_index"))

@app.route("/worktimerecords/", methods=["POST"])
def worktimerecords_create():
    t = Worktimerecord(request.form.get("name"))

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("worktimerecords_index"))