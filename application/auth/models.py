from application import db
from application.models import Base

from sqlalchemy.sql import text

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

# jostain syystä "Wtr" täytyy olla isolla, viittaus luokkaan ei tauluun
    worktimerecords = db.relationship("Worktimerecord", backref='account', lazy = True)

# Toteutetaan ehkä myöhemmin
#    projectlead = db.relationship("Project", secondary=account_project, back_populates = 'account', lazy = True)

    def __init__(self, name):
        self.name = name

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonumous(self):
        return True

    def is_authenticated(self):
        return True

    @staticmethod
    def find_users_records():
        stmt = text("SELECT SUM(Worktimerecord.hours) FROM Account"
                     " LEFT JOIN Worktimerecord ON Worktimerecord.account_id = Account.id"
                     " LEFT JOIN Project_worktimerecord ON Project_worktimerecord.worktimerecord_id = Worktimerecord.id"
                     " LEFT JOIN Project ON Project.id = Project_worktimerecord.project_id")
#                     " GROUP BY project.id")
#testiä
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"hours":row[0]})

        return response