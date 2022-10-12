from flask import Flask
from flask_bootstrap import Bootstrap4
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
bootstrap = Bootstrap4()
login_manager = LoginManager()
login_manager.login_view = 'users.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .users import users as users_bp
    app.register_blueprint(users_bp)

    from .meals import meals as meals_bp
    app.register_blueprint(meals_bp)

    from .calendar import calendar as calendar_bp
    app.register_blueprint(calendar_bp)

    from .planner import planner as planner_bp
    app.register_blueprint(planner_bp)

    return app
