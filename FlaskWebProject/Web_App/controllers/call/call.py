from flask import render_template, session
from . import call_blueprint
import pandas as pd
from Web_App.controllers.account.account import getAccountID
from Web_App.controllers.main.main import getLastTradingDate
from Web_App.sqlConnection import get_connections
from Web_App.models import StockPicks
from flask_login import login_user, logout_user, login_required, current_user
from jinja2 import TemplateNotFound
from Web_App.controllers.auth.auth_views import is_logged_in

# CoveredCallsResults
@call_blueprint.route('/CoveredCallsResults')
@is_logged_in
def CoveredCallsResults():
    #Getting DB connection
    connection_string, engine, connection = get_connections()
    #Getting Account
    accountID = getAccountID(session['username'])
    lastTradingDate = getLastTradingDate()
    
    #Stocks Picks
    query = "EXEC spCoveredCallResults @AccountID= ?, @TradingDate= ?, @StockID=NULL"
    results = pd.read_sql_query(query,connection,params=(str(accountID),lastTradingDate.values[0][0]))

    return render_template('app/call/CoveredCallsResults.html',StockPicks=results.values)

# CoveredCallsResults
@call_blueprint.route('/CoveredCallsResults/<string:StockID>')
@is_logged_in
def CoveredCallsResultsStock(StockID):
    #Getting DB connection
    connection_string, engine, connection = get_connections()
    #Getting Account
    accountID = getAccountID(session['username'])
    lastTradingDate = getLastTradingDate()
    
    #Stocks Picks
    query = "EXEC spCoveredCallResults @AccountID= ?, @TradingDate= ?, @StockID= ? "
    results = pd.read_sql_query(query,connection,params=(str(accountID),lastTradingDate.values[0][0],StockID))

    return render_template('app/call/CoveredCallsResults.html',StockPicks=results.values)

