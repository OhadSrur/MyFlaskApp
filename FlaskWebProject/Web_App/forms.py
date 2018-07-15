from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField, DecimalField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, DataRequired
from wtforms import ValidationError
from Web_App.models import UserAccount
from flask_wtf import FlaskForm

# Register Form Class
class RegisterForm(FlaskForm):
    title = StringField('Title', [validators.Length(min=2, max=6)])
    firstName = StringField('First Name', [validators.Length(min=2, max=20)])
    surName = StringField('Surname', [validators.Length(min=2, max=20)])
    username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, ''numbers, dots or underscores')])
    email = StringField('Email', validators=[Required(), Length(1, 64),Email()])
    phone = IntegerField('Phone')
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.length(8,20),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password', validators=[Required()])

    def validate_email(self, field):
        if UserAccount.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if UserAccount.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

# Update Form Class
class UpdateAccountDetails(Form):
    title = StringField('Title', [validators.Length(min=2, max=6)])
    firstName = StringField('First Name', [validators.Length(min=2, max=20)])
    surName = StringField('Surname', [validators.Length(min=2, max=20)])
    username = StringField('Username', [validators.Length(min=4, max=30)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    phone = IntegerField('Phone')

class UpdateAccountBasic(Form):
    StockCommission = DecimalField('StockCommission',places=2)
    StockCommPerSher = DecimalField('StockCommissionPerSher',places=3)
    OptionCommission = DecimalField('OptionCommission',places=2)
    OptionCommPerSher = DecimalField('OptionCommPerSher',places=3)
    TaxRate = DecimalField('TaxRate',places=2)
    USD = IntegerField('USD')
    AUD = IntegerField('AUD')
    MinPerc = DecimalField('MinPerc',places=4)
    RequiredPerc = DecimalField('RequiredPerc',places=4)
    DeepInTheMoneyCheck = DecimalField('DeepInTheMoneyCheck',places=2)
    DailyReport = BooleanField('DailyReport', false_values=None)
    PositionReport = BooleanField('PositionReport', false_values=None)

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

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Update Password')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, ''numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')