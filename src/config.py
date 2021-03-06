# -*- coding:utf-8 -*-
import os

rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MISSOURI_ADMIN = os.environ.get('MISSOURI_ADMIN')
    MISSOURI_MAIL_SENDER = os.environ.get('MAIL_USERNAME')
    POSTS_PER_PAGE = os.environ.get('POSTS_PER_PAGE')
    BABEL_DEFAULT_COCALE = 'zh'
    MISSOURI_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(Config):
    """
    Testing environment
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(rootdir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(Config):
    """
    Debugging environment
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(rootdir, 'data-dev.sqlite')


class ProductionConfig(Config):
    """
    Production environment
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(rootdir, 'data.sqlite')


class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


conf = {
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'heroku': HerokuConfig
}
