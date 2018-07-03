from flask import render_template, Blueprint, session
import pandas as pd
from Web_App.controllers.account import getAccountID
from Web_App.controllers.main import getLastTradingDate
from Web_App.sqlConnection import get_connections
from Web_App.models import StockPicks
from flask_login import login_user, logout_user, login_required, current_user
from jinja2 import TemplateNotFound

call_blueprint = Blueprint(
    'call',
    __name__,
    template_folder='../templates/app/call')

# CoveredCallsResults
@call_blueprint.route('/CoveredCallsResults')
@login_required
def CoveredCallsResults():
    #Getting DB connection
    connection_string, engine, connection = get_connections()
    #Getting Account
    accountID = getAccountID(session['username'])
    lastTradingDate = getLastTradingDate()
    
    #Stocks Picks
    query = "EXEC spCoveredCallResults @AccountID= ?, @TradingDate= ?, @StockID=NULL"
    results = pd.read_sql_query(query,connection,params=(str(accountID),lastTradingDate.values[0][0]))

    return render_template('CoveredCallsResults.html',StockPicks=results.values)

# CoveredCallsResults
@call_blueprint.route('/CoveredCallsResults/<string:StockID>')
@login_required
def CoveredCallsResultsStock(StockID):
    #Getting DB connection
    connection_string, engine, connection = get_connections()
    #Getting Account
    accountID = getAccountID(session['username'])
    lastTradingDate = getLastTradingDate()
    
    #Stocks Picks
    query = "EXEC spCoveredCallResults @AccountID= ?, @TradingDate= ?, @StockID= ? "
    results = pd.read_sql_query(query,connection,params=(str(accountID),lastTradingDate.values[0][0],StockID))

    return render_template('CoveredCallsResults.html',StockPicks=results.values)

