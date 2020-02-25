from flask import redirect, render_template, request, url_for, abort
from flask_login import current_user

from application import app, db, login_required
from application.worktimerecords.models import Worktimerecord
from application.worktimerecords.forms import WorktimerecordForm
from application.projects.models import Project
from application.auth.models import User
from application.projects.forms import ProjectForm

@app.route("/worktimerecords", methods=["GET"])
def worktimerecords_index():
    return render_template("worktimerecords/list.html", worktimerecords = Worktimerecord.query.all(), users_record = User.find_users_records(), users = User.query.all())

@app.route("/worktimerecords/new/")
@login_required
def worktimerecords_form():
    
    project_list = Project.query.all()
    if not project_list:
        return render_template("projects/new.html", form = ProjectForm())
    project_choices = [ (i.id, i.name) for i in project_list ]
    form = WorktimerecordForm()
    form.project.choices = project_choices
    
    return render_template("worktimerecords/new.html", form = form, choices = project_choices)

@app.route("/worktimerecords/modify/<worktimerecord_id>", methods=["POST", "GET"])
@login_required
def worktimerecords_modify(worktimerecord_id):
    wtr = Worktimerecord.query.get(worktimerecord_id)
    project = Project.query.get(wtr.project_id)
    projectlead = project.projectlead_account_id

    if wtr.account_id != current_user.id or projectlead != current_user.id:
        abort(403)

    project_list = Project.query.all()
    project_choices = [ (i.id, i.name) for i in project_list ]

    form = WorktimerecordForm(request.form)

    form.name.data = wtr.name
    form.hours.data = wtr.hours
    form.dateofwork.data = wtr.dateofwork
    form.project.choices = project_choices
    form.project.data = wtr.project_id

    return render_template("worktimerecords/modify.html", form = form, worktimerecord_id = wtr.id)


@app.route("/worktimerecords/modifyselected/<worktimerecord_id>", methods=["POST", "GET"])    
@login_required
def worktimerecords_modify_selected(worktimerecord_id):
    wtr = Worktimerecord.query.get(worktimerecord_id)
    project = Project.query.get(wtr.project_id)
    projectlead = project.projectlead_account_id

    if wtr.account_id != current_user.id or projectlead != current_user.id:
        abort(403)

    project_list = Project.query.all()
    project_choices = [ (i.id, i.name) for i in project_list ]

    form = WorktimerecordForm(request.form)
    form.project.choices = project_choices

#sdfgdfb
    if not form.validate_on_submit():
        return render_template("worktimerecords/modify.html", form = form, worktimerecord_id = wtr.id)

    wtr.name = form.name.data
    wtr.hours = form.hours.data
    wtr.dateofwork = form.dateofwork.data

    newproject = Project.query.get(form.project.data)
    wtr.project_name = newproject.name
    wtr.project_id = newproject.id

    db.session().commit()

    return redirect(url_for("worktimerecords_index"))

@app.route("/worktimerecords/remove/<worktimerecord_id>/", methods=["POST"])
@login_required
def worktimerecords_remove(worktimerecord_id):

    wtr = Worktimerecord.query.get(worktimerecord_id)

    if wtr.account_id == current_user.id:
        db.session().delete(wtr)
        db.session().commit()
        return redirect(url_for("worktimerecords_index"))

    return redirect(url_for("worktimerecords_index", error = "Only project lead or maker can delete record"))

@app.route("/worktimerecords/", methods=["GET", "POST"])
@login_required
def worktimerecords_create():

    form = WorktimerecordForm(request.form)


    project_list = Project.query.all()
    project_choices = [ (i.id, i.name) for i in project_list ]
    form.project.choices = project_choices

    # tää kuoli jossain kohtaa.. ja jostain syytä toimii kun laittoi xx_on_submit.. oli väärin tehty, ei toimi..
    # Toimii kun laittoi vaihtoehdot uudestaan formiin tässä metodissa
    if not form.validate_on_submit():
        return render_template("worktimerecords/new.html", form = form)

    wtr = Worktimerecord(form.name.data)
    wtr.hours = form.hours.data
    wtr.dateofwork = form.dateofwork.data
    wtr.account_id = current_user.id

    proj = Project.query.get(form.project.data)
    wtr.project_name = proj.name
    wtr.project_id = proj.id

    db.session().add(wtr)
    db.session().commit()

    return redirect(url_for("worktimerecords_index"))