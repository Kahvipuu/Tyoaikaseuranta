from application import db
from application.models import Base

# vikaa..
# Projekti-Työaikakirjaus ,tarvitseeko db.Integerin??
class Project_worktimerecord(Base):

    __tablename__ = "project_worktimerecord"

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    worktimerecord_id = db.Column(db.Integer, db.ForeignKey('worktimerecord.id'))

class Project(Base):

    ___tablename__ = "project"

    name = db.Column(db.String(144), nullable=False)

# myöhemmin
#    projectlead_account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
#                           nullable = False)

    worktimerecord_id = db.relationship("Project_worktimerecord", backref='projects', lazy = True)

    def __init__(self, name):
        self.name = name


# Henkilö-Projekti, toteutetaan ehkä myöhemmin
# account_project = db.Table('account_project', Base.metadata,
#    db.Column("account_id", db.Integer, db.ForeignKey('account.id')),
#    db.Column("project_id", db.Integer, db.ForeignKey('project.id')) )

