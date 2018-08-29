from flask import render_template, flash
from . import put_blueprint
import pandas as pd
from Web_App.controllers.account.account import getAccountID
from Web_App.sqlConnection import get_connections
from Web_App.models import StockPicks
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from Web_App.forms import SellPutForm

@put_blueprint.route('/putResults')
@login_required
def putResults():
     #Getting DB connection
    connection_string, engine, connection = get_connections()
    #Getting Account
    accountID = current_user.get_id()

    #Stocks Picks
    query = "exec spViewPutResuls @AccountID= ?, @StockID= ? "
    results = pd.read_sql_query(query,connection,params=(str(accountID),None))

    return render_template('app/put/putResults.html',StockPicks=results.values)

@put_blueprint.route('/putResults/<string:StockID>')
@login_required
def putResultsStock(StockID):
     #Getting DB connection
    connection_string, engine, connection = get_connections()
    #Getting Account
    accountID = current_user.get_id()

    #Stocks Picks
    query = "exec spViewPutResuls @AccountID= ?, @StockID= ? "
    results = pd.read_sql_query(query,connection,params=(str(accountID),StockID))

    stockQueryDetail = "exec spStockDetails @StockID= %s" %StockID
    resultsStockQuery = pd.read_sql_query(stockQueryDetail,connection)

    return render_template('app/put/putResults.html',StockPicks=results.values, stockQueryResult=resultsStockQuery.values)

@put_blueprint.route('/SellPut', methods=['GET', 'POST'])
@login_required
def SellPut():
    form = SellPutForm()
    if form.validate_on_submit():
        #Getting DB connection
        connection_string, engine, connection = get_connections()
        
        #Getting Account
        accountID = current_user.get_id()
        # Insert Sell Put Transaction
        insertPut = "EXEC CoveredCalls.dbo.spiCreatePutOption @AccountID= ?,@StockID= ?,@PositionID=NULL,@PutStrikePrice= ?,@PutExpiry= ?,@PutPrice= ?,@IsOptionPriceWithCommission= ?,@PutNumberOfShares= ?,@PutWriteDate= ?,@IsDemo= ?,@TranType= ?"
        connection.execute(insertPut, [accountID,form.StockID.data,form.PutStrikePrice.data,form.PutExpiry.data,form.PutPrice.data,form.IsOptionPriceWithCommission.data,form.PutNumberOfShares.data,form.PutWriteDate.data,form.IsDemo.data,form.TranType.data])

        flash('SELL put option has been inserted for Stock %s' % form.StockID.data)

    elif form.is_submitted():
        error = 'Information incorrect, please check all fields and submit again'
        flash(form.errors)
        return render_template('app/put/SellPut.html',form=form, error=error)

    return render_template('app/put/SellPut.html', form=form)