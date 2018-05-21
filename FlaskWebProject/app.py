"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import os
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField
from passlib.hash import sha256_crypt
from functools import wraps
from sqlConnection import get_sql_connection_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# initialization
app = Flask(__name__)

app.secret_key='MySecretKey1@#$'
app.config['SQLALCHEMY_DATABASE_URI'] = get_sql_connection_string(svr='svr',db='db',user='user',psw='password!')
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

# Register Form Class
class RegisterForm(Form):
    title = StringField('title', [validators.Length(min=2, max=5)])
    firstName = StringField('firstName', [validators.Length(min=3, max=20)])
    surName = StringField('surName', [validators.Length(min=3, max=20)])
    username = StringField('Username', [validators.Length(min=4, max=30)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    phone = IntegerField('phone')
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

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
        #result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        #query = s.query(user).filter(user.username==POST_USERNAME, user.password)
        query = UserAccount.query.filter_by(username=POST_USERNAME).first()

        if query.UserID > 0:
            # Get stored hash
            password = query.password

            # Compare Passwords
            if sha256_crypt.verify(POST_PASSWORD, password):
                # Passed
                session['logged_in'] = True
                session['username'] = POST_USERNAME

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
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

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
   return render_template('dashboard.html')

if __name__ == '__main__':

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT,debug=True)
 
