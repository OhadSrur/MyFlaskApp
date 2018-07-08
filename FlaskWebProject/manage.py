from Web_App import create_app
from flask_script import Manager
from Web_App.models import db
from waitress import serve

app = create_app()

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

if __name__ == "__main__":
    #manager.run()
    serve(manager.run(),host="0.0.0.0",port=5000)