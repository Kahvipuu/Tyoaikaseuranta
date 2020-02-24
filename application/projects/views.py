from flask import redirect, render_template, request, url_for, abort
from flask_login import current_user

from application import app, db, login_required
from application.worktimerecords.models import Worktimerecord
from application.worktimerecords.forms import WorktimerecordForm
from application.projects.models import Project
from application.projects.forms import ProjectForm
from application.auth.models import User

@app.route("/projects", methods=["GET"])
def projects_index():
    return render_template("projects/list.html", projects = Project.query.all())

@app.route("/projects/new/")
@login_required
def projects_form():
    return render_template("projects/new.html", form = ProjectForm())

@app.route("/projects/remove/<project_id>/", methods=["POST"])
@login_required
def projects_remove(project_id):
    project = Project.query.get(project_id)
    user = current_user.username
    wtrs = Worktimerecord.query.all()

    for wtr in wtrs:
        if wtr.project_id == project.id:
            return render_template("projects/list.html", projects = Project.query.all(), 
                error = "There are workrecords in the project you are trying to remove")

    if project.leader == user:
        db.session().delete(project)
        db.session().commit()
        return redirect(url_for("projects_index"))

    else:       
        return redirect(url_for("projects_index"))

@app.route("/projects/modify/<project_id>/", methods=["GET", "POST"])
@login_required
def projects_modify(project_id):
    project = Project.query.get(project_id)
    return render_template('projects/modify.html', form = ProjectForm(), project_id = project.id)

@app.route("/projects/modifyselected/<project_id>/", methods=["GET", "POST"])
@login_required
def projects_modify_selected(project_id):
    project = Project.query.get(project_id)

    # olisi parempi tunnistaa id:lla
    if project.projectlead_account_id != current_user.id:
        abort(403)

    form = ProjectForm(request.form)

    if not form.validate():
        return redirect(url_for("projects_index"))

    project.name = form.name.data

    # vanhojen projektinimien muuttaminen kirjauksista.

    db.session.commit()

    return redirect(url_for("projects_index"))

@app.route("/projects/create/", methods=["POST"])
@login_required
def projects_create():
    form = ProjectForm(request.form)

    if not form.validate():
        return render_template("projects/new.html", form = form)

    project = Project(form.name.data)

    db.session().add(project)
    db.session().commit()

    return redirect(url_for("projects_index"))