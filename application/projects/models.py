from application import db
from application.models import Base
from flask_login import current_user

class Project(Base):

    ___tablename__ = "project"

    name = db.Column(db.String(144), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    leader = db.Column(db.String(144), nullable=False)

    projectlead_account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                                       nullable=False)

    worktimerecord_id = db.relationship('Worktimerecord', backref='project', lazy=True)

    def __init__(self, name):
        self.name = name
        self.active = True
        self.leader = current_user.name
        self.projectlead_account_id = current_user.id

