from flask import render_template, redirect, url_for, request, flash
from . import account_blueprint
import pandas as pd
from Web_App import db
from Web_App.models import UserAccount, Account, AccountScanParameters
from Web_App.forms import UpdateAccountDetails, UpdateAccountBasic, UpdateAccountOptionParameters
from Web_App.sqlConnection import get_connections
from flask_login import login_required, current_user

def getAccountID(username):
    connection_string, engine, connection = get_connections()
    #Getting Account
    accountIDquery = "EXEC spGetAccount @Username= %r ,@email=NULL,@AccountName='Live'" % username
    accountID = pd.read_sql_query(accountIDquery,connection)
    return str(accountID.values[0][0])

# Account Details
@account_blueprint.route('/myAccount', methods=['GET', 'POST'])
@login_required
def myAccount():
    query = UserAccount.query.filter_by(username=current_user.get_username()).first()

    if query.UserID > 0:
        return render_template('app/account/myAccount.html', account=query)
    else:
        msg = 'No Account Found'
        return render_template('app/account/myAccount.html', msg=msg)

# Account Details
@account_blueprint.route('/accountBasic', methods=['GET', 'POST'])
@login_required
def accountBasic():
    query = Account.query.filter_by(AccountID=current_user.get_id()).first()

    if query.UserID > 0:
        return render_template('app/account/accountBasic.html', account=query)
    else:
        msg = 'No Account Found'
        return render_template('app/account/accountBasic.html', msg=msg)

@account_blueprint.route('/updateAccount', methods=['GET', 'POST'])
@login_required
def updateAccount():
    query = UserAccount.query.filter_by(username=current_user.get_username()).first()
    form = UpdateAccountDetails(request.form)

    if request.method == 'POST' : #and form.validate()   
       # Update account
        UserAccount.query.filter_by(username=current_user.get_username()).update({
             'title': request.form['title'],
             'firstName': request.form['firstName'],
             'surName': request.form['surName'],
             'email': request.form['email'],
             'phone': request.form['phone'],
        })

        # Commit to DB
        db.session.commit()

        # Close connection
        db.session.close()

        flash('You successfully updated your account', 'success')

        return redirect(url_for('call.CoveredCallsResults'))
    return redirect(url_for('account.myAccount'))

@account_blueprint.route('/updateAccountBasic', methods=['GET', 'POST'])
@login_required
def updateAccountBasic():
    query = Account.query.filter_by(AccountID=current_user.get_id()).first()
    form = UpdateAccountBasic(request.form)

    if request.method == 'POST' : #and form.validate()   
       # Update account
        Account.query.filter_by(AccountID=current_user.get_id()).update({
             'StockCommission': request.form['StockCommission'],
             'StockCommPerSher': request.form['StockCommPerSher'],
             'OptionCommission': request.form['OptionCommission'],
             'OptionCommPerSher': request.form['OptionCommPerSher'],
             'TaxRate': request.form['TaxRate'],
             'USD': request.form['USD'],
             'AUD': request.form['AUD'],
             'MinPerc': request.form['MinPerc'],
             'RequiredPerc': request.form['RequiredPerc'],
             'DeepInTheMoneyCheck': request.form['DeepInTheMoneyCheck'],
             #'DailyReport': request.form['DailyReport'],
             #'PositionReport': request.form['PositionReport'],
        })

        # Commit to DB
        db.session.commit()

        # Close connection
        db.session.close()

        flash('You successfully updated your account basic parameters', 'success')

        return redirect(url_for('call.CoveredCallsResults'))
    return redirect(url_for('account.accountBasic'))

@account_blueprint.route('/parametersOptions', methods=['GET', 'POST'])
@login_required
def parametersOptions():
    accountID = current_user.get_id()
    query = AccountScanParameters.query.filter_by(AccountID=accountID, PositionType='New').first()

    if query.UserID > 0:
        return render_template('app/account/parametersOptions.html', parametersOptions=query)
    else:
        msg = 'No Account Found'
        return render_template('app/account/parameters.html', msg=msg)
    
@account_blueprint.route('/updateParameters', methods=['GET', 'POST'])
@login_required
def updateParameters():
    accountID = current_user.get_id()
    query = AccountScanParameters.query.filter_by(AccountID=accountID, PositionType='New').first()
    form = UpdateAccountOptionParameters(request.form)

    if request.method == 'POST' : #and form.validate()   
       # Update account
        AccountScanParameters.query.filter_by(AccountID=accountID, PositionType='New').update({
            'WeeksNumForCalcProb': request.form['WeeksNumForCalcProb'],
            'MaxNumberOfShares' : request.form['MaxNumberOfShares'],
            'MaxUSDInvestmentSizePerStock' : request.form['MaxUSDInvestmentSizePerStock'],
            'MaxExpiryWeeks' : request.form['MaxExpiryWeeks'],
            'MinCallProbability' : request.form['MinCallProbability'],
            'MaxCallProbability' : request.form['MaxCallProbability'],
            'MinIncomeExPerc' : request.form['MinIncomeExPerc'],
            'MinIncomeNotExPerc' : request.form['MinIncomeNotExPerc'],
            #'CheckDailyProbability' : request.form['CheckDailyProbability'],
            'MaxNumResultsPerExpiry' : request.form['MaxNumResultsPerExpiry'],
            'MinTradingPrice' : request.form['MinTradingPrice'],
            'MaxTradingPrice' : request.form['MaxTradingPrice'],
            #'IncludePutResults' : request.form['IncludePutResults'],
            #'ExcludeExpiryDuringEventDates' : request.form['ExcludeExpiryDuringEventDates'],
            'ExcludeStocks' : request.form['ExcludeStocks'],
            'ExcludeIndustry' : request.form['ExcludeIndustry'],
            'PutProtectionPercCheckPrice' : request.form['PutProtectionPercCheckPrice'],
        })

        # Commit to DB
        db.session.commit()

        # Close connection
        db.session.close()

        flash('You successfully updated your Optionn Parameters', 'success')

        return redirect(url_for('account.parametersOptions'))
    return redirect(url_for('account.parametersOptions'))

# Account Portfolio
@account_blueprint.route('/Portfolio', methods=['GET', 'POST'])
@login_required
def Portfolio():
    #Getting DB connection
    connection_string, engine, connection = get_connections()
    #Getting Account
    accountID = current_user.get_id()

    #Stocks Picks
    query = "SELECT StockID, AvgStockPurchasePriceAfterComm,StockPurchaseDate , BreakEvenNet, TotalNumOfShares, TotalStockInvestment FROM [CoveredCalls].[dbo].[vStockPurchasePortfolio] where HoldingStock=1 and AccountID= %s;" %accountID
    results = pd.read_sql_query(query,connection)

    return render_template('app/account/Portfolio.html',StockPicks=results.values)