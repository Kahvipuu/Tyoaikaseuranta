from application import db
from application.models import Base


class Worktimerecord(Base):

    __tablename__ = "worktimerecord"

    # name on nyt työaikakirjauksen selite, kun ehtii niin pitäisi etsiä hyvä refactorointi keino VisualSC:een ja muuttaa esim. definition
    name = db.Column(db.String(144), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    hours = db.Column(db.Integer)
    dateofwork = db.Column(db.Date)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    project_name = db.Column(db.String(144))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __init__(self, name):
        self.name = name
        self.done = False

    def get_id(self):
        return self.id


# Kokeillaan toisella tavalla
'''
class Project_worktimerecord(Base):

    __tablename__ = "project_worktimerecord"

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    worktimerecord_id = db.Column(
        db.Integer, db.ForeignKey('worktimerecord.id'))

    project = db.relationship("Project", backref="wrts", lazy=True)
    worktimerecord = db.relationship(
        "Worktimerecord", backref="project", lazy=True)


#ja tätä ei tehdä näin ollenkaan
project_worktimerecord = db.Table("project_worktimerecord", 
    db.Column('worktimerecord_id', db.Integer, db.ForeignKey('worktimerecord.id'), primary_key=True), 
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True))


'''
