from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from blinker import Namespace
from flask.ext.login import LoginManager


# Initialize the db extension, but without configuring
# it with an application instance.
db = SQLAlchemy()
flask_bcrypt = Bcrypt()
login_manager = LoginManager()

socializer_signals = Namespace()
user_followed = socializer_signals.signal('user-followed')

from signal_handlers import *


def create_app(config=None):
    app = Flask(__name__)

    if config is not None:
        app.config.from_object(config)

    # Initialize any extensions and bind blueprints to the
    # application instance here.
    db.init_app(app)
    flask_bcrypt.init_app(app)
    login_manager.init_app(app)

    from application.users.views import users

    app.register_blueprint(users, url_prefix='/users')

    from application.users import models as user_models

    @login_manager.user_loader
    def load_user(user_id):
        return user_models.User.query.get(int(user_id))

    return app
