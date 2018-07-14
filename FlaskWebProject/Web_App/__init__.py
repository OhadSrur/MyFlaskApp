"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask, send_from_directory
import os
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from Web_App.config import Config

bootstrap = Bootstrap()
login_manager = LoginManager()
db = SQLAlchemy()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'

def create_app(config_object):
    # initialization
    app = Flask(__name__)
    app.config.from_object(config_object)
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Make the WSGI interface available at the top level so wfastcgi can get it.
    wsgi_app = app.wsgi_app
    
    from Web_App.controllers.main import main_blueprint
    app.register_blueprint(main_blueprint)
    
    from Web_App.controllers.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from Web_App.controllers.call import call_blueprint
    app.register_blueprint(call_blueprint)
    
    from Web_App.controllers.put import put_blueprint
    app.register_blueprint(put_blueprint)
    
    from Web_App.controllers.graph import graph_blueprint
    app.register_blueprint(graph_blueprint)
    
    from Web_App.controllers.account import account_blueprint
    app.register_blueprint(account_blueprint)

    @app.route('/favicon.ico') 
    def favicon(): 
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
    return app