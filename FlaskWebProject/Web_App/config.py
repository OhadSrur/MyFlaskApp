import os
from Web_App.sqlConnection import get_sql_connection_string

class Config(object):
    SECRET_KEY = os.environ.get('CC_APP_SECRET')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.sendgrid.net')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[CoveredCall Admin]'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'No-reply-Covered-Call@azureadmin.com')
    MAIL_DEBUG = False

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = get_sql_connection_string(svr=os.environ.get('CC_SVR'),db=os.environ.get('CC_SVR'),user=os.environ.get('CC_USER'),psw=os.environ.get('CC_PSW'))
    DEBUG = False

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = get_sql_connection_string(svr=os.environ.get('CC_SVR'),db=os.environ.get('CC_SVR'),user=os.environ.get('CC_USER'),psw=os.environ.get('CC_PSW'))
    DEBUG = None
