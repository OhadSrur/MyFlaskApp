from flask import render_template, Blueprint, send_from_directory
import pandas as pd
from Web_App.sqlConnection import get_sql_connection_string, get_all_sql_connection

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates/main')

@main_blueprint.route('/')
def index():
    return render_template('index.html')


@main_blueprint.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

@main_blueprint.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main_blueprint.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@main_blueprint.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def getLastTradingDate():
    connection_string, engine, connection = get_all_sql_connection(svr=CC_SVR,db=CC_DB,user=CC_USER,psw=CC_PSW)
    #Last Trading Date
    checkLastTradingDateQuery = "SELECT MarketDate FROM vLastMarketDate"
    return pd.read_sql_query(checkLastTradingDateQuery,connection)