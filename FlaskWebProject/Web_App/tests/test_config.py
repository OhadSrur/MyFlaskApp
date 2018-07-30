import os
#from Web_App import create_app

def test_development_config(app):
    #app = create_app('Web_App.config.DevConfig')
    app.config.from_object('Web_App.config.DevConfig')
    assert app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SECRET_KEY'] == os.environ.get('CC_APP_SECRET')
   # assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL')


def test_testing_config(app):
    #app = create_app('Web_App.config.TestingConfig')
    app.config.from_object('Web_App.config.TestingConfig')
    assert app.config['DEBUG']
    assert app.config['TESTING']
    #assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_TEST_URL')


def test_production_config(app):
    #app = create_app('Web_App.config.ProdConfig')
    app.config.from_object('Web_App.config.ProdConfig')
    assert not app.config['DEBUG']
    assert not app.config['TESTING']
    #assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL')
