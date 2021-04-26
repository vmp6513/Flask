import os

class Config:
    # GENERAL CONFIG
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'vmp6513'
    # EMAIL CONFIG
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '373009794@qq.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'jxmvgtcagoswbjie')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <373009794@qq.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN', 'Flasky Admin <373009794@qq.com>')
    # DATABASE CONFIG
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:w1470671730@localhost:3306/flask?charset=utf8'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:w1470671730@localhost:3306/flask_test?charset=utf8'


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}