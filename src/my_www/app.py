import os

from flask import Flask
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "2e4d864d-158f-480f-ba80-6e0d6e93186d"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URI"]

    from .db import db, User

    db.init_app(app)

    from .routes import routes_blueprint

    app.register_blueprint(routes_blueprint)

    login_manager = LoginManager()
    login_manager.session_protection = None
    login_manager.login_view = "routes.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    db.create_all(app=app)

    return app
