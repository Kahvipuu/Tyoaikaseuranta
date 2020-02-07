from application import db
from application.models import Base
from application.projects.models import Project_worktimerecord, Project

class Worktimerecord(Base):

    __tablename__ = "worktimerecord"

    #name on nyt työaikakirjauksen selite, kun ehtii niin pitäisi etsiä hyvä refactorointi keino VisualSC:een ja muuttaa esim. definition
    name = db.Column(db.String(144), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    hours = db.Column(db.Integer)
    dateofwork = db.Column(db.Date)


    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable = False)

    project_id = db.relationship("Project_worktimerecord", backref='worktimerecords', lazy = True)

    def __init__(self, name):
        self.name = name
        self.done = False