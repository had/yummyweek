import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    BOOTSTRAP_BOOTSWATCH_THEME = 'litera'
    SECRET_KEY = 't0p.5ecr3t'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app): pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "yummyweek-dev.sqlite")
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 465

class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "yummyweek-test.sqlite")
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    # TODO
    # 'production': ProductionConfig,
    'default': DevelopmentConfig
}