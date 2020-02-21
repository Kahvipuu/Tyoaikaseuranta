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
    projects = db.relationship("Project", backref='account', lazy = True)

    def __init__(self, name):
        self.name = name

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def is_authenticated(self):
        return True

    def roles(self):
        return ["ADMIN"]

    @staticmethod
    def find_users_records():
        stmt = text("SELECT project.name, SUM(worktimerecord.hours) FROM Account"
                     " LEFT JOIN worktimerecord ON worktimerecord.account_id = Account.id"
                     " LEFT JOIN project ON project.id = worktimerecord.project_id"
                     " GROUP BY project.id")


        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"name":row[0], "hours":row[1]})

        return response