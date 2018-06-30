from flask import render_template, Blueprint, session
import pandas as pd
from Web_App.controllers.account import getAccountID
from Web_App.controllers.main import getLastTradingDate
from Web_App.sqlConnection import get_all_sql_connection
from Web_App.models import StockPicks
from Web_App.controllers.auth import is_logged_in

call_blueprint = Blueprint(
    'call',
    __name__,
    template_folder='../templates/app/call')

# CoveredCallsResults
@call_blueprint.route('/CoveredCallsResults')
@is_logged_in
def CoveredCallsResults():
    #Getting DB connection
    connection_string, engine, connection = get_all_sql_connection(svr=CC_SVR,db=CC_DB,user=CC_USER,psw=CC_PSW)
    #Getting Account
    accountID = getAccountID(session['username'])
    lastTradingDate = getLastTradingDate()
    
    #Stocks Picks
    query = "EXEC spCoveredCallResults @AccountID= ?, @TradingDate= ?, @StockID=NULL"
    results = pd.read_sql_query(query,connection,params=(str(accountID),lastTradingDate.values[0][0]))

    return render_template('CoveredCallsResults.html',StockPicks=results.values)

# CoveredCallsResults
@call_blueprint.route('/CoveredCallsResults/<string:StockID>')
@is_logged_in
def CoveredCallsResultsStock(StockID):
    #Getting DB connection
    connection_string, engine, connection = get_all_sql_connection(svr=CC_SVR,db=CC_DB,user=CC_USER,psw=CC_PSW)
    #Getting Account
    accountID = getAccountID(session['username'])
    lastTradingDate = getLastTradingDate()
    
    #Stocks Picks
    query = "EXEC spCoveredCallResults @AccountID= ?, @TradingDate= ?, @StockID= ? "
    results = pd.read_sql_query(query,connection,params=(str(accountID),lastTradingDate.values[0][0],StockID))

    return render_template('CoveredCallsResults.html',StockPicks=results.values)

