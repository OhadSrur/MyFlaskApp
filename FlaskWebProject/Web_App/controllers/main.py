from flask import render_template, Blueprint, send_from_directory
import pandas as pd
from Web_App.sqlConnection import get_connections
import os

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

def getLastTradingDate():
    connection_string, engine, connection = get_connections()
    #Last Trading Date
    checkLastTradingDateQuery = "SELECT MarketDate FROM vLastMarketDate"
    return pd.read_sql_query(checkLastTradingDateQuery,connection)