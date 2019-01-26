import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQL_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(basedir, 'flask_boilerplate_main.db'))
    SQL_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQL_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(basedir, 'flask_boilerplate_test.db'))
    SQL_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    DEBUG = False

config_by_name = dict(
    dev= DevelopmentConfig,
    test= TestingConfig,
    prod= ProductionConfig
)

key = Config.SECRET_KEY
