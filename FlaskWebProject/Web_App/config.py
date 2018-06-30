import os
from Web_App.sqlConnection import get_sql_connection_string

class Config(object):
    SECRET_KEY = os.environ.get('CC_APP_SECRET')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = get_sql_connection_string(svr=os.environ.get('CC_SVR'),db=os.environ.get('CC_SVR'),user=os.environ.get('CC_USER'),psw=os.environ.get('CC_PSW'))
    DEBUG = False

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = get_sql_connection_string(svr=os.environ.get('CC_SVR'),db=os.environ.get('CC_SVR'),user=os.environ.get('CC_USER'),psw=os.environ.get('CC_PSW'))
    DEBUG = None
