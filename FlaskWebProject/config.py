import os

class Config(object):
    secret_key=os.environ.get('CC_APP_SECRET')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = get_sql_connection_string(svr=os.environ.get('CC_SVR'),db=CC_DB,user=os.environ.get('CC_USER'),psw=os.environ.get('CC_PSW'))
    DEBUG = False

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = get_sql_connection_string(svr=os.environ.get('CC_SVR'),db=CC_DB,user=os.environ.get('CC_USER'),psw=os.environ.get('CC_PSW'))
    DEBUG = True
