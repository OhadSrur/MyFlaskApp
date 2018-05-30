"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import os
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField, DecimalField, BooleanField
from passlib.hash import sha256_crypt
from functools import wraps
from sqlConnection import get_sql_connection_string, get_all_sql_connection
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, select
import pandas as pd
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

app = Flask(__name__)

# initialization
app = Flask(__name__)

#Secrets from environment
app.secret_key=os.environ.get('CC_APP_SECRET')
CC_SVR = CC_DB = os.environ.get('CC_SVR')
CC_USER = os.environ.get('CC_USER')
CC_PSW = os.environ.get('CC_PSW')

app.config['SQLALCHEMY_DATABASE_URI'] = get_sql_connection_string(svr=CC_SVR,db=CC_DB,user=CC_USER,psw=CC_PSW)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# extensions
db = SQLAlchemy(app)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def index():
    return render_template('index.html')

class UserAccount(db.Model):
    __tablename__ = 'UserAccount'
    UserID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    title = db.Column(db.String(5), unique=True, nullable=False)
    firstName = db.Column(db.String(50), unique=False, nullable=False)
    surName = db.Column(db.String(50), unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=False, nullable=True)
    password = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<UserAccount %r>' % self.username

class Account(db.Model):
    __tablename__ = 'Account'
    UserID = db.Column(db.Integer, primary_key=True)
    AccountID = db.Column(db.Integer, primary_key=True)
    AccountName = db.Column(db.String(50), unique=False, nullable=False)
    StockCommission = db.Column(db.Float(precision='4,2'),  nullable=False)
    StockCommissionPerSher = db.Column(db.Float(precision='3,3'),  nullable=True)
    OptionCommission = db.Column(db.Float(precision='4,2'),  nullable=False)
    OptionCommPerSher = db.Column(db.Float(precision='3,3'),  nullable=True)
    TaxRate = db.Column(db.Float(precision='5,2'),  nullable=False)
    USD = db.Column(db.Float(precision='9,2'),  nullable=False)
    AUD = db.Column(db.Float(precision='9,2'),  nullable=False)
    MinPerc = db.Column(db.Float(precision='5,5'),  nullable=True)
    RequiredPerc = db.Column(db.Float(precision='5,5'),  nullable=True)

    def __repr__(self):
        return '<Account %r>' % self.AccountID
# Register Form Class
class RegisterForm(Form):
    title = StringField('Title', [validators.Length(min=2, max=6)])
    firstName = StringField('First Name', [validators.Length(min=2, max=20)])
    surName = StringField('Surname', [validators.Length(min=2, max=20)])
    username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, ''numbers, dots or underscores')])
    email = StringField('Email', validators=[Required(), Length(1, 64),Email()])
    phone = IntegerField('Phone')
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password', validators=[Required()])

    def validate_email(self, field):
        if UserAccount.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if UserAccount.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class StockPicks(db.Model):
    #Return Stock Pick Results
    __tablename__ = 'StockPickScanResults'
    __table_args__ = {"schema": "Stage"}
    UserID = db.Column(db.Integer, primary_key=True)
    StockID = db.Column(db.String(20), unique=False, nullable=False)
    CompanyName = db.Column(db.String(50), unique=False, nullable=False)
    Industry = db.Column(db.String(50), unique=False, nullable=False)
    CurrentStockPrice = db.Column(db.String(50), unique=False, nullable=False)
    CallExpiryDays = db.Column(db.String(50), unique=False, nullable=False)
    StrikePrice = db.Column(db.String(50), unique=False, nullable=False)
    IncomeExPerc = db.Column(db.String(50), unique=False, nullable=False)
    IncomeNotExPerc = db.Column(db.String(50), unique=False, nullable=False)
    ExpectedCallReturn = db.Column(db.String(50), unique=False, nullable=False)
    StockPriceDate = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return '<StockPickScanResults %r>' % self.userID

class AccountScanParameters(db.Model):
    __tablename__ = 'AccountScanParameters'
    AccountID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, primary_key=True)
    PositionType = db.Column(db.String(10), primary_key=True)
    WeeksNumForCalcProb = db.Column(db.Integer,   nullable=False)
    MaxNumberOfShares = db.Column(db.Integer,   nullable=True)
    MaxUSDInvestmentSizePerStock = db.Column(db.Integer,   nullable=True)
    MaxExpiryWeeks = db.Column(db.Integer,  nullable=False)
    MinCallProbability = db.Column(db.Float(precision='3,2'),  nullable=False)
    MaxCallProbability = db.Column(db.Float(precision='3,2'),  nullable=False)
    MinIncomeExPerc = db.Column(db.Float(precision='4,2'),  nullable=False)
    MinIncomeNotExPerc = db.Column(db.Float(precision='4,2'),  nullable=False)
    CheckDailyProbability = db.Column(db.Boolean)
    MaxNumResultsPerExpiry = db.Column(db.Integer,   nullable=False)
    MinTradingPrice = db.Column(db.Float(precision='4,2'),  nullable=False)
    MaxTradingPrice = db.Column(db.Float(precision='4,2'),  nullable=True)
    IncludePutResults = db.Column(db.Boolean)
    ExcludeExpiryDuringEventDates = db.Column(db.Boolean)
    ExcludeStocks = db.Column(db.String(2000), unique=False, nullable=True)
    ExcludeIndustry = db.Column(db.String(2000), unique=False, nullable=True)
    PutProtectionPercCheckPrice = db.Column(db.Float(precision='3,3'),  nullable=True)

    def __repr__(self):
        return '<AccountScanParameters %r>' % self.UserID
# Update Form Class
class UpdateAccountDetails(Form):
    title = StringField('Title', [validators.Length(min=2, max=6)])
    firstName = StringField('First Name', [validators.Length(min=2, max=20)])
    surName = StringField('Surname', [validators.Length(min=2, max=20)])
    username = StringField('Username', [validators.Length(min=4, max=30)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    phone = IntegerField('Phone')

class UpdateAccountOptionParameters(Form):
    WeeksNumForCalcProb = IntegerField('WeeksNumForCalcProb')
    MaxNumberOfShares = IntegerField('MaxNumberOfShares')
    MaxUSDInvestmentSizePerStock = IntegerField('MaxUSDInvestmentSizePerStock')
    MaxExpiryWeeks = IntegerField('MaxExpiryWeeks')
    MinCallProbability = DecimalField('MinCallProbability',places=2)
    MaxCallProbability = DecimalField('MaxCallProbability',places=2)
    MinIncomeExPerc = DecimalField('MinIncomeExPerc',places=2)
    MinIncomeNotExPerc = DecimalField('MinIncomeNotExPerc',places=2)
    CheckDailyProbability = BooleanField('CheckDailyProbability', false_values=None)
    MaxNumResultsPerExpiry = IntegerField('MaxNumResultsPerExpiry')
    MinTradingPrice = DecimalField('MinTradingPrice',places=2)
    MaxTradingPrice = DecimalField('MaxTradingPrice',places=2)
    IncludePutResults = BooleanField('IncludePutResults', false_values=None)
    ExcludeExpiryDuringEventDates = BooleanField('ExcludeExpiryDuringEventDates', false_values=None)
    ExcludeStocks = StringField('ExcludeStocks', [validators.Length(max=2000)])
    ExcludeIndustry = StringField('ExcludeIndustry', [validators.Length(max=2000)])
    PutProtectionPercCheckPrice = DecimalField('PutProtectionPercCheckPrice',places=3)

# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        firstName = form.firstName.data
        surName = form.surName.data
        email = form.email.data
        phone = form.phone.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Add account
        newAccount = UserAccount(title=title,firstName=firstName,surName=surName,email=email,phone=phone,username=username,password=password)
        db.session.add(newAccount)

        # Commit to DB
        db.session.commit()

        # Close connection
        db.session.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        POST_USERNAME = request.form['username']
        POST_PASSWORD = request.form['password']

        # Get user by username
        query = UserAccount.query.filter_by(username=POST_USERNAME).first()

        if query and query.UserID > 0:
            # Get stored hash
            password = query.password

            # Compare Passwords
            if sha256_crypt.verify(POST_PASSWORD, password):
                # Passed
                session['logged_in'] = True
                session['username'] = POST_USERNAME

                flash('You are now logged in', 'success')
                return redirect(url_for('dailyResults'))
            else:
                error = 'Invalid password'
                return render_template('login.html', error=error)
            # Close connection
            db.session.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# dailyResults
@app.route('/dailyResults')
@is_logged_in
def dailyResults():
    #Getting DB connection
    connection_string, engine, connection = get_all_sql_connection(svr=CC_SVR,db=CC_DB,user=CC_USER,psw=CC_PSW)
    #Getting Account
    username = 'OhadS' #session['username']
    accountIDquery = "SELECT a.AccountID \
                 FROM Account a \
		            join \
	             UserAccount  ua on a.UserID=ua.UserID \
                 WHERE ua.UserName= %r and a.AccountName='Live'" % username
    accountID = pd.read_sql_query(accountIDquery,connection)
    accountID = accountID.values[0][0]

    #Last Trading Date
    checkLastTradingDateQuery = "SELECT  TOP 1 mc.MarketDate \
    FROM	[dbo].[MarketCalendar] mc \
    WHERE mc.MarketStatus='Open' and mc.MarketDate between  dateadd(day,-10,try_convert(date,try_convert(datetimeoffset, GETDATE()) AT TIME ZONE 'Eastern Standard Time')) \
        AND CASE WHEN try_convert(time,try_convert(datetimeoffset, GETDATE()) AT TIME ZONE 'Eastern Standard Time')>'16:30' THEN try_convert(date,try_convert(datetimeoffset, GETDATE()) AT TIME ZONE 'Eastern Standard Time') \
            ELSE dateadd(day,-1,try_convert(date,try_convert(datetimeoffset, GETDATE()) AT TIME ZONE 'Eastern Standard Time')) END \
    order by mc.MarketDate desc"
    lastTradingDate = pd.read_sql_query(checkLastTradingDateQuery,connection)
    
    #Stocks Picks
    query = "SELECT StockID, CompanyName, Industry, CurrentStockPrice, CallExpiryDays, StrikePrice, IncomeExPerc, IncomeNotExPerc,ExpectedCallReturn \
    FROM Stage.StockPickScanResults \
    WHERE AccountID= ? and StockPriceDate= ? \
    ORDER BY try_convert(int,CallExpiryDays) ASC, ExpectedCallReturn DESC"
    results = pd.read_sql_query(query,connection,params=(str(accountID),lastTradingDate.values[0][0]))

    return render_template('dailyResults.html',StockPicks=results.values)

# Account Details
@app.route('/myAccount', methods=['GET', 'POST'])
@is_logged_in
def myAccount():
    query = UserAccount.query.filter_by(username=session['username']).first()

    if query.UserID > 0:
        return render_template('myAccount.html', account=query)
    else:
        msg = 'No Account Found'
        return render_template('myAccount.html', msg=msg)

@app.route('/updateAccount', methods=['GET', 'POST'])
@is_logged_in
def updateAccount():
    query = UserAccount.query.filter_by(username=session['username']).first()
    form = UpdateAccountDetails(request.form)

    if request.method == 'POST' : #and form.validate()   
       # Update account
        UserAccount.query.filter_by(username=session['username']).update({
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

        return redirect(url_for('dailyResults'))
    return redirect(url_for('myAccount'))

@app.route('/parametersOptions', methods=['GET', 'POST'])
@is_logged_in
def parametersOptions():

    query = AccountScanParameters.query.filter_by(UserID='1', PositionType='New').first()

    if query.UserID > 0:
        return render_template('parametersOptions.html', parametersOptions=query)
    else:
        msg = 'No Account Found'
        return render_template('parameters.html', msg=msg)
    
@app.route('/updateParameters', methods=['GET', 'POST'])
@is_logged_in
def updateParameters():
    query = AccountScanParameters.query.filter_by(UserID='1', PositionType='New').first()
    form = UpdateAccountOptionParameters(request.form)

    if request.method == 'POST' : #and form.validate()   
       # Update account
        AccountScanParameters.query.filter_by(UserID='1', PositionType='New').update({
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

        return redirect(url_for('parametersOptions'))
    return redirect(url_for('parametersOptions'))

if __name__ == '__main__':

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT,debug=True)
 
