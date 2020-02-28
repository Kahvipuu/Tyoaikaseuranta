from application import db
from application.models import Base

from flask_login import current_user
from sqlalchemy.sql import text, func

from application.worktimerecords.models import Worktimerecord
from application.projects.models import Project

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

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
    def find_users_projectlead_records():
        projectsowned = Project.query.filter_by(projectlead_account_id = current_user.id)
        projectsowned_id = [(p.id) for p in projectsowned]
        records = Worktimerecord.query.filter(Worktimerecord.project_id.in_(projectsowned_id)).order_by(Worktimerecord.project_id).all()
        return records

    @staticmethod
    def find_projectleaders_summary():
        projectsowned = Project.query.filter_by(projectlead_account_id = current_user.id)
        
        hours = []
        counter = 0
        
        for p in projectsowned:
            hours.append(0)
            hourrec = Worktimerecord.query.filter_by(project_id = p.id)
            for h in hourrec:
                hours[counter] += h.hours
            counter += 1
        
        counter = 0
        response = []
        for project in projectsowned:
            response.append({
            "name":project.name, 
            "hours":hours[counter], 
            "workers": Worktimerecord.query.filter_by(project_id = project.id).group_by(Worktimerecord.account_id).count()
            })
            counter += 1


# Toimiva versio, ennenkuin alan herokun toimintaa selvittämään...
#            "workers": Worktimerecord.query.filter_by(project_id = project.id).group_by(Worktimerecord.account_id).count()


        # joku päivä sitten summa toimimaan
        # Worktimerecord.query.filter_by(project_id = project.id).group_by(project_id).sum(Worktimerecord.hours)

        return response


    @staticmethod
    def find_workercount_in_all_projects():
        #Jostain mystisestä syystä täytyy laittaa kyselyt sisäkkäin
        usercount = text("SELECT COUNT(1) AS quantity FROM (SELECT account.id FROM account"
                        " GROUP BY account.id) AS sub")
#                        " JOIN account ON worktimerecord.account_id = account.id"
#                        " JOIN project ON worktimerecord.project_id = project.id"

        query = db.engine.execute(usercount)

        response = []
        for r in query:
            response.append({"quantity":r[0]})

        return response
# testivaihe


# tää on vissiin lähinnä sama kuin projectleads summary. paitsi nyt kun mikään ei toimi niinkuin pitäisi.
    @staticmethod
    def summary_of_records():

        stmt = text("SELECT project.name, SUM(worktimerecord.hours) FROM Account"
                     " JOIN worktimerecord ON worktimerecord.account_id = Account.id"
                     " JOIN project ON project.id = worktimerecord.project_id"
                     " GROUP BY project.id")

#                       Nämä muistona että mitä on jo yritetty, jos tähän tulee palattua joskus...
#                     " WHERE project.id IN :projectsid"
#                      .params(projectsid = (projects_id,))
        
        res = db.engine.execute(stmt)
        
        response = []
        for row in res:
            response.append({"name":row[0], "hours":row[1]})

        return response