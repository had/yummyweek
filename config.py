import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    BOOTSTRAP_BOOTSWATCH_THEME = "united"
    SECRET_KEY = os.environ.get('SECRET_KEY') or "t0p.5ecr3t"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SSL_REDIRECT = False

    # files upload
    MAX_CONTENT_LENGTH = 1024 * 1024  # 1MB

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


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'yummyweek.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class HerokuConfig(ProductionConfig):
    # https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "").replace("postgres://", "postgresql://")
    SSL_REDIRECT = (os.environ.get("DYNO") is not None)

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        # setup logging
        import logging
        from logging import StreamHandler
        handler = StreamHandler()
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    # TODO
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'default': DevelopmentConfig
}
