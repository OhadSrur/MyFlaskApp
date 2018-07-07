"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask, send_from_directory
import os
#from jinja2 import TemplateNotFound
from Web_App.models import db
from Web_App.controllers.main import main_blueprint
from Web_App.controllers.auth import auth_blueprint
from Web_App.controllers.account import account_blueprint
from Web_App.controllers.register import registerAccount_blueprint
from Web_App.controllers.call import call_blueprint
from Web_App.controllers.put import put_blueprint
from Web_App.controllers.graph import graph_blueprint
from Web_App.sqlConnection import get_sql_connection_string 
#from flask_bootstrap import Bootstrap

def create_app():
    # initialization
    app = Flask(__name__)
    #app.config.from_object(config_object)
    #bootstrap = Bootstrap(app)
    app.secret_key=os.environ.get('CC_APP_SECRET')
    app.config['SQLALCHEMY_DATABASE_URI'] = get_sql_connection_string(svr=os.environ.get('CC_SVR'),db=os.environ.get('CC_SVR'),user=os.environ.get('CC_USER'),psw=os.environ.get('CC_PSW'))
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Make the WSGI interface available at the top level so wfastcgi can get it.
    wsgi_app = app.wsgi_app

    app.register_blueprint(registerAccount_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(call_blueprint)
    app.register_blueprint(put_blueprint)
    app.register_blueprint(graph_blueprint)
    app.register_blueprint(account_blueprint)

    @app.route('/favicon.ico') 
    def favicon(): 
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
    return app.run()