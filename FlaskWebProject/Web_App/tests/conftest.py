import pytest
from Web_App import create_app
from Web_App.models import UserAccount


@pytest.fixture()
def app():
    app = create_app()
    #app.config.from_object(config_object)
    return app

@pytest.fixture()
def app_ctx(app):
    app.config.from_object('Web_App.config.DevConfig')
    app_context = app.app_context()
    app_context.push()
    yield app_context

@pytest.fixture()
def user(app_ctx):
    user = UserAccount.query.filter_by(username='jonedoe').first()
    return user