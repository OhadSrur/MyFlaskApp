from flask import render_template
from . import call_blueprint
import pandas as pd
from Web_App.controllers.account.account import getAccountID
from Web_App.controllers.main.main import getLastTradingDate
from Web_App.sqlConnection import get_connections
from Web_App.models import StockPicks
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

# CoveredCallsResults
@call_blueprint.route('/CoveredCallsResults')
@login_required
def CoveredCallsResults():
    #Getting DB connection
    connection_string, engine, connection = get_connections()
    #Getting Account
    accountID = current_user.get_id()
    lastTradingDate = getLastTradingDate()
    
    #Stocks Picks
    query = "EXEC spCoveredCallResults @AccountID= ?, @TradingDate= ?, @StockID=NULL"
    results = pd.read_sql_query(query,connection,params=(str(accountID),lastTradingDate.values[0][0]))

    return render_template('app/call/CoveredCallsResults.html',StockPicks=results.values)

# CoveredCallsResults
@call_blueprint.route('/CoveredCallsResults/<string:StockID>')
@login_required
def CoveredCallsResultsStock(StockID):
    #Getting DB connection
    connection_string, engine, connection = get_connections()
    #Getting Account
    accountID = current_user.get_id()
    lastTradingDate = getLastTradingDate()
    
    #Stocks Picks
    query = "EXEC spCoveredCallResults @AccountID= ?, @TradingDate= ?, @StockID= ? "
    results = pd.read_sql_query(query,connection,params=(str(accountID),lastTradingDate.values[0][0],StockID))

    stockQueryDetail = "exec spStockDetails @StockID= %s" %StockID
    resultsStockQuery = pd.read_sql_query(stockQueryDetail,connection)

    return render_template('app/call/CoveredCallsResults.html',StockPicks=results.values, stockQueryResult=resultsStockQuery.values)

# CoveredCallsResults
@call_blueprint.route('/NextCoveredCall')
@login_required
def NextCoveredCall():
    #Getting DB connection
    connection_string, engine, connection = get_connections()
    #Getting Account
    accountID = current_user.get_id()
    
    #Stocks Picks
    query = "exec spNextCall @AccountID= ?, @StockID=NULL"
    results = pd.read_sql_query(query,connection,params=(str(accountID)))

    return render_template('app/call/NextCoveredCallPosition.html',NextPicks=results.values)

# CoveredCallsResults
@call_blueprint.route('/NextCoveredCall/<string:StockID>')
@login_required
def NextCoveredCallStock(StockID):
    #Getting DB connection
    connection_string, engine, connection = get_connections()
    #Getting Account
    accountID = current_user.get_id()
    
    #Stocks Picks
    query = "exec spNextCall @AccountID= %s, @StockID= %s " %(accountID,StockID)
    results = pd.read_sql_query(query,connection)

    return render_template('app/call/NextCoveredCallPosition.html',NextPicks=results.values)