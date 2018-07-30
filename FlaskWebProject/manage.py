from Web_App import create_app
from flask_script import Manager
from Web_App import db
from waitress import serve
import pytest

app = create_app('Web_App.config.DevConfig')

manager = Manager(app)

@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, db=db)
#def make_shell_context():
#    return dict(app=app, db=db)
#manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def test():
    """Runs the tests.
    Adding -s to the pytest command lets pytest print to the console any print statements that you use in your tests, not just the ones from failing tests.
    """
    pytest.main(["-s", "Web_App/tests"])

if __name__ == "__main__":
    #manager.run()
    serve(manager.run(), url_scheme='https')
    #waitress.serve(myapp.wsgifunc, port=8041, url_scheme='https')
    #from wsgiref.simple_server import make_server

    #httpd = make_server('localhost', manager.run())
    #httpd.serve_forever()