from sqlalchemy import MetaData, Table, select
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt
from flask_login import UserMixin
from Web_App import db, login_manager

class UserAccount(UserMixin,db.Model):
    __tablename__ = 'UserAccount'
    UserID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    title = db.Column(db.String(5), unique=True, nullable=False)
    firstName = db.Column(db.String(50), unique=False, nullable=False)
    surName = db.Column(db.String(50), unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=False, nullable=True)
    password = db.Column(db.String(50), unique=True, nullable=False)

    #def password(self, password):
    #    self.password = generate_password_hash(password)

    def verify_password(self, value):
        return sha256_crypt.verify(value, self.password)

    #def verify_password(self, value):
    #    return check_password_hash(self.password, value)

    def get_UserId(self):
        return self.UserID

    def __repr__(self):
        return '<UserAccount %r>' % self.username

class Account(db.Model):
    __tablename__ = 'Account'
    UserID = db.Column(db.Integer, primary_key=True) 
    AccountID = db.Column(db.Integer, primary_key=True)
    AccountName = db.Column(db.String(50), unique=False, nullable=False)
    StockCommission = db.Column(db.Float(precision='4,2'),  nullable=False)
    StockCommPerSher = db.Column(db.Float(precision='3,3'),  nullable=True)
    OptionCommission = db.Column(db.Float(precision='4,2'),  nullable=False)
    OptionCommPerSher = db.Column(db.Float(precision='3,3'),  nullable=True)
    TaxRate = db.Column(db.Float(precision='5,2'),  nullable=False)
    USD = db.Column(db.Float(precision='9,2'),  nullable=False)
    AUD = db.Column(db.Float(precision='9,2'),  nullable=False)
    MinPerc = db.Column(db.Float(precision='5,5'),  nullable=True)
    RequiredPerc = db.Column(db.Float(precision='5,5'),  nullable=True)
    DeepInTheMoneyCheck = db.Column(db.Float(precision='4,2'),  nullable=False)
    DailyReport = db.Column(db.Boolean)
    PositionReport = db.Column(db.Boolean)

    def __repr__(self):
        return '<Account %r>' % self.AccountID

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
        return '<StockPickScanResults %r>' % self.userID459519

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

@login_manager.user_loader
def load_user(user_id):
    return UserAccount.query.get(int(user_id))