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

# Kansiosta application tiedoston views sisältö, omaa kamaa
from application import views
# Kansiosta applic/worktimerecords
from application.worktimerecords import models
from application.worktimerecords import views
# autentikaatio
from application.auth import models
from application.auth import views

# kirjautumistoiminnallisuus
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Luodaan lopulta tarvittavat tietokantataulut
try:
    db.create_all()
except:
    pass