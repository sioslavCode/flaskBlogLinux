"""Obzirom da importitamo flaskbgloh py file classe iz models.py a u models.py importiramo db.kreiraniu u flaskblog
   događa nam se kružna petkla koja stvara error. da bi to izbjelgi trebamo naš python module pretvoriti u package.
   to cemo napraviti tako sto cemo stvoriti inite file"""

# Ovdje cemo inicijalirati komponente

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'  # ime funckije opet #ovo je za onaj dekorater @login required da zna na koju stranicu/route preusmjerit
login_manager.login_message_category = 'info'

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users  # Znaci ovo je instanca Blueprinta kao sto se vidi u tom fileu
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
