from flask import render_template, Blueprint, session
import pandas as pd
from Web_App.controllers.account import getAccountID
from Web_App.sqlConnection import get_connections
from Web_App.models import StockPicks
from flask_login import login_user, logout_user, login_required, current_user
from jinja2 import TemplateNotFound

put_blueprint = Blueprint(
    'put',
    __name__,
    template_folder='../templates/app/put')

@put_blueprint.route('/putResults')
@login_required
def putResults():
     #Getting DB connection
    connection_string, engine, connection = get_connections()
    #Getting Account
    accountID = getAccountID(session['username'])

    #Stocks Picks
    query = "exec spViewPutResuls @AccountID= ?, @StockID= ? "
    results = pd.read_sql_query(query,connection,params=(str(accountID),None))

    return render_template('putResults.html',StockPicks=results.values)

@put_blueprint.route('/putResults/<string:StockID>')
@login_required
def putResultsStock(StockID):
     #Getting DB connection
    connection_string, engine, connection = get_connections()
    #Getting Account
    accountID = getAccountID(session['username'])

    #Stocks Picks
    query = "exec spViewPutResuls @AccountID= ?, @StockID= ? "
    results = pd.read_sql_query(query,connection,params=(str(accountID),StockID))

    return render_template('putResults.html',StockPicks=results.values)

