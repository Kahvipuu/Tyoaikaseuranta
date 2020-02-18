#Flask käyttöön
from flask import Flask
app = Flask(__name__)

# Tuodaan SQLAlchemy käyttöön
from flask_sqlalchemy import SQLAlchemy

#Valinta heroku/oma kone
import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    # Käytetään worktimerecords.db-nimistä SQLite-tietokantaa. Kolme vinoviivaa
    # kertoo, tiedosto sijaitsee tämän sovelluksen tiedostojen kanssa
    # samassa paikassa
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///worktimerecords.db"
    # Pyydetään SQLAlchemyä tulostamaan kaikki SQL-kyselyt
    app.config["SQLALCHEMY_ECHO"] = True

# Luodaan db-olio, jota käytetään tietokannan käsittelyyn
db = SQLAlchemy(app)

# kirjautumistoiminnallisuus
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login"

# Roolit kirjautumiseen
from functools import wraps

def login_required(_func=None, *, role="ANY"):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not (current_user and current_user.is_authenticated):
                return login_manager.unauthorized()

            acceptable_roles = set(("ANY", *current_user.roles()))

            if role not in acceptable_roles:
                return login_manager.unauthorized()

            return func(*args, **kwargs)
        return decorated_view
    return wrapper if _func is None else wrapper(_func)

# Kansiosta application tiedoston views sisältö, omaa kamaa
from application import models
from application import views
# Kansiosta applic/worktimerecords
from application.worktimerecords import models
from application.worktimerecords import views
# autentikaatio
from application.auth import models
from application.auth import views
# projektit
from application.projects import models
from application.projects import views

# Kirjautumistoiminnallisuus, osa2
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Luodaan lopulta tarvittavat tietokantataulut
try:
    db.create_all()
except:
    pass